#
# _author_ = Grant Curell <grant_curell@Dell.com>
#
#
# Copyright (c) 2020 Dell EMC Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
import logging
from app import app

# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--port', dest="port", required=False, type=int, default=5000,
                    help='Specify the port you want Flask to run on')
parser.add_argument('--log-level', metavar='LOG_LEVEL', dest="log_level", required=False, type=str, default="info",
                    choices=['debug', 'info', 'warning', 'error', 'critical'],
                    help='The log level at which you want to run.')

args = parser.parse_args()

if args.log_level:
    if args.log_level == "debug":
        logging.basicConfig(level=logging.DEBUG)
        app.config['DEBUG'] = True
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

app.run(host='0.0.0.0', port=args.port)

