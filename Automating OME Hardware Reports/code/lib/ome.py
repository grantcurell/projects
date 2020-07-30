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

import requests
import json
import os
import csv
import logging


def authenticate_with_ome(ip_address: str, user_name: str, password: str) -> tuple:
    """
    Authenticates a session against an OME server

    Args:
        ip_address: IP address of the OME server
        user_name: Username for OME
        password: Password for the OME user

    Returns: Returns a tuple of auth_success (bool), headers (dict). Which are true if authentication succeeded
             and {'content-type': 'application/json' respectively.

    """

    """ X-auth session creation """
    auth_success = False
    session_url = "https://%s/api/SessionService/Sessions" % ip_address
    user_details = {'UserName': user_name,
                    'Password': password,
                    'SessionType': 'API'}
    headers = {'content-type': 'application/json'}
    session_info = requests.post(session_url, verify=False,
                                 data=json.dumps(user_details),
                                 headers=headers)
    if session_info.status_code == 201:
        headers['X-Auth-Token'] = session_info.headers['X-Auth-Token']
        auth_success = True
    else:
        error_msg = "Failed create of session with {0} - Status code = {1}"
        logging.error(error_msg.format(ip_address, session_info.status_code))
    return auth_success, headers


def get_ips(ip_array: str, csv_file_path: str = None, ) -> list:
    """
    Validates a list of IP addresses and parses them into a Python list.

    Args:
        csv_file_path: A CSV with a single column with IP addresses.
        ip_array: A list of IP addresses in the format ip1,ip2,ip3,etc.

    Returns: A Python list with the parsed IP addresses.

    """

    list_of_ips = []

    if ip_array:
        list_of_ips = ip_array.split(',')
    else:
        if os.path.isfile(csv_file_path):
            if os.path.getsize(csv_file_path) > 0:
                csv_file = open(csv_file_path, 'r')
                csv_data = csv.reader(csv_file)
                csv_list = list(csv_data)
                for csv_data in csv_list:
                    for ip in csv_data:
                        list_of_ips.append(ip)
            else:
                logging.error("File %s seems to be empty ... Exiting" % csv_file_path)
        else:
            raise Exception("File not found ...  Retry")

    list_of_ipaddress = []

    for ip in list_of_ips:
        if '-' in ip:
            ips = ip.split('-')
        else:
            ips = ip
        if type(ips) is list:
            for ip in ips:
                list_of_ipaddress.append(ip)
        else:
            list_of_ipaddress.append(ips)

        for ip_addr in list_of_ipaddress:
            ip_bytes = ip_addr.split('.')
            if len(ip_bytes) != 4:
                raise Exception("Invalid IP address " + ip_addr + " Example of valid ip  192.168.1.0")
            for ip_byte in ip_bytes:
                if not ip_byte.isdigit():
                    raise Exception(
                        "Invalid ip address" + ip_addr + " Only digits are allowed. Example of valid ip 192.168.1.0")
                ip = int(ip_byte)
                if ip < 0 or ip > 255:
                    raise Exception(
                        "Invalid ip address " + ip_addr + " single byte must be 0 <= byte < 256. Example of valid ip "
                                                          "192.168.1.0")

    return list_of_ips
