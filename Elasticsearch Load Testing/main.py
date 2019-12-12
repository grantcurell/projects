from argparse import ArgumentParser
from time import time, sleep
from random import randint
from selenium import webdriver
import logging
from multiprocessing.pool import Pool

__author__ = "Grant Curell"
__copyright__ = "Do what you want with it"
__license__ = "GPLv3"


class BrowserWorker:

    browser = webdriver
    refresh_rate = int
    jitter = int

    def __init__(self, refresh_rate, jitter):
        self.refresh_rate = refresh_rate
        self.jitter = jitter
        self.browser = webdriver.Chrome()

    def run(self, duration, url):

        stop_time = time() + duration

        while time() + self.refresh_rate < stop_time:
            self.browser.get(url)

            """
            
            Taken from: https://www.lambdatest.com/blog/how-to-measure-page-load-times-with-selenium/
            
            navigation_start – This attribute returns the time spent after the user agent completes unloading the 
            previous page/document. If there was no document prior to loading the new page, navigationStart returns the
             same value as fetchStart.
            
            responseStart – This attribute returns the time as soon as the user-agent receives the first byte from the 
            server or from the local sources/application cache.
            
            domComplete – This attribute returns the time just before the current document/page readiness is set to 
            ‘complete’. document.readyState status as ‘complete’ indicates that the parsing of the page/document is 
            complete & all the resources required for the page are downloaded. We will have a look an example of 
            domComplete in subsequent section.
            
            """

            # Use Navigation Timing  API to calculate the timings that matter the most
            navigation_start = self.browser.execute_script("return window.performance.timing.navigationStart")
            response_start = self.browser.execute_script("return window.performance.timing.responseStart")
            dom_complete = self.browser.execute_script("return window.performance.timing.domComplete")

            # Calculate the performance
            backend_performance_calc = response_start - navigation_start
            frontend_performance_calc = dom_complete - response_start

            # TODO I NEED TO UPDATE THIS FOR AVERAGES
            print("Back End: %s" % backend_performance_calc)
            print("Front End: %s" % frontend_performance_calc)

            jitter = randint(0, self.jitter)

            # If less than 50 we will make the jitter negative, otherwise it will be positive.
            plus_minus = randint(0, 100)

            next_refresh = self.refresh_rate

            if plus_minus < 50:
                if self.refresh_rate - jitter < 1:
                    logging.debug("Jitter would be less than 1. Setting the jitter to 1.")
                    next_refresh = 1
                else:
                    next_refresh = self.refresh_rate - jitter
            else:
                if time() + self.refresh_rate + jitter > stop_time:
                    logging.debug("Refresh rate plus jitter would exceed the stop time. Truncating jitter to launch "
                                  "next refresh at stop time.")
                    jitter = stop_time - time() - self.refresh_rate
                next_refresh = self.refresh_rate + jitter

            sleep(next_refresh)

            self.browser.refresh()

        self.browser.quit()


def main():
    parser = ArgumentParser(description="Used to test multiple people connecting to a Kibana dashboard and the load it "
                                        "places on Elasticsearch.")
    parser.add_argument('--url', metavar='URL', dest="url", type=str, required=True,
                        help='The url you would like the worker threads to browse to.')
    parser.add_argument('--browsers', metavar='num_browsers', dest="number_of_browsers", type=int, required=False,
                        default=10, help='The number of browsers you want to use to test the Kibana dashboard.')
    parser.add_argument('--refresh-rate', metavar='seconds', dest="refresh_rate", type=int, required=False, default=20,
                        help='How often the browsers will refresh themselves after being opened.')
    parser.add_argument('--jitter', metavar='seconds', dest="jitter", type=int, required=False, default=10,
                        help='Controls randomness in the refresh rate up or down. For example if your refresh rate is '
                             '20 seconds and jitter is five, the refreshes will happen in between 15 and 25 seconds at '
                             'random. The default is 10 seconds. Set to 0 to remove jitter.')
    parser.add_argument('--duration', metavar='seconds', dest="duration", type=int, required=False, default=60,
                        help='The test duration measured in seconds. The default is 60.')
    parser.add_argument('--log-level', metavar='log_level', dest="log_level", required=False, type=str, default="info",
                        choices=['debug', 'info', 'warning', 'error', 'critical'],
                        help='Set the log level used by the program.')
    parser.add_argument('--print-usage', dest="print_usage", required=False, action='store_true',
                        help='Show example usage.')

    args = parser.parse_args()

    if not args.number_of_browsers and not args.print_usage:
        parser.print_help()
        exit(0)

    if args.print_usage:
        print('TODO: Put usage here.')
        exit(0)

    if args.refresh_rate <= 0:
        logging.critical("Refresh rate must be set to a positive value.")
        exit(0)

    if args.jitter < 0:
        logging.critical("Jitter cannot be less than 0.")
        exit(0)

    if args.duration <= 0:
        logging.critical("Duration must be set to a positive value.")
        exit(0)

    if args.log_level:
        if args.log_level == "debug":
            logging.basicConfig(level=logging.DEBUG)
        elif args.log_level == "info":
            logging.basicConfig(level=logging.INFO)
        elif args.log_level == "warning":
            logging.basicConfig(level=logging.WARNING)
        elif args.log_level == "error":
            logging.basicConfig(level=logging.ERROR)
        elif args.log_level == "critical":
            logging.basicConfig(level=logging.CRITICAL)
    else:
        logging.basicConfig(level=logging.INFO)

    # Begin main program execution
    browsers = []

    logging.info("Creating browsers we will use to connect to the target URL.")
    for i in range(args.number_of_browsers):

        logging.debug("Created browser # " + str(i))
        browsers.append(BrowserWorker(args.refresh_rate, args.jitter))

    logging.info("Beginning test.")
    logging.debug("Creating multithreaded pool to which we will issue jobs.")
    with Pool(processes=args.number_of_browsers) as pool:
        for i in range(args.number_of_browsers):
            logging.info("Starting job on browser #" + str(i))
            pool.apply(browsers[i].run, args=(args.duration, args.url))


if __name__ == '__main__':
    main()
