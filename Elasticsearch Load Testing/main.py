from argparse import ArgumentParser
from selenium import webdriver
import logging
from multiprocessing.pool import Pool

__author__ = "Grant Curell"
__copyright__ = "Do what you want with it"
__license__ = "GPLv3"

from urllib2 import urlopen
from urllib import quote
from HTMLParser import HTMLParser
from .bs4 import BeautifulSoup


class BrowserWorker:

    browser = webdriver

    def __init__(self):
        chop = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(chrome_options=chop)

    def open_url(self):
        print("stuff")


def run_test():

    parser = SPAHTMLParser(self)

    # Word Reference
    self.browser.get(unidecode(u"http://www.wordreference.com/definicion/" + word))
    parser.process_wordreference(self.browser.page_source)


def main():
    parser = ArgumentParser(description="Used to test multiple people connecting to a Kibana dashboard and the load it places on Elasticsearch.")
    parser.add_argument('--browsers', metavar='BROWSERS', dest="number_of_browsers", type=int, required=False, default=10,
                        help='The number of browsers you want to use to test the Kibana dashboard. ')
    parser.add_argument('--refresh-rate', metavar='REFRESH', dest="refresh_rate", type=int, required=False, default=20,
                        help='How often the browsers will refresh themselves after being opened.')
    parser.add_argument('--log-level', metavar='LOG_LEVEL', dest="log_level", required=False, type=str, default="info",
                        choices=['debug', 'info', 'warning', 'error', 'critical'],
                        help='Set the log level used by the program.')
    parser.add_argument('--print-usage', dest="print_usage", required=False, action='store_true',
                        help='Show example usage.')

    args = parser.parse_args()  # type: argparse.Namespace

    if not args.number_of_browsers and not args.print_usage:
        parser.print_help()
        exit(0)

    if args.print_usage:
        print('TODO: Put usage here.')
        exit(0)

    

    for i in range(args.number_of_browsers):


        #logging.critical("If you want to write directly to Anki's media folder you must provide your username!")
        #exit(0)

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


if __name__ == '__main__':
    main()
