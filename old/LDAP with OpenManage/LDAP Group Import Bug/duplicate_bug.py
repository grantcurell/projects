#
#  Python script using OME API to create a new static group
#
# _author_ = Grant Curell <grant_curell@dell.com>
# _version_ = 0.1
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

import json
import argparse
from argparse import RawTextHelpFormatter
import urllib3
import requests
from pprint import pprint


def duplicate_bug(ome_ip_address: str, ome_username: str, ome_password: str):
    """
    Duplicates the bug
    Args:
        ome_ip_address: IP address of the OME server
        ome_username:  Username for OME
        ome_password: OME password
    """

    try:
        session_url = 'https://%s/api/SessionService/Sessions' % ome_ip_address
        import_group_url = "https://%s/core/api/Console/import-groups" % ome_ip_address
        headers = {'content-type': 'application/json'}
        user_details = {'UserName': ome_username,
                        'Password': ome_password,
                        'SessionType': 'API'}

        session_info = requests.post(session_url, verify=False,
                                     data=json.dumps(user_details),
                                     headers=headers)
        if session_info.status_code == 201:
            headers['X-Auth-Token'] = session_info.headers['X-Auth-Token']

            # TODO REPLACE WITH YOUR PAYLOAD
            test_payload = [
              {
                    "userTypeId": 2,
                    "objectGuid": 1314600001,
                    "objectSid": 1314600001,
                    "directoryServiceId": 13483,
                    "name": "grantgroup",
                    "password": "",
                    "userName": "grant",
                    "roleId": "10",
                    "locked": False,
                    "isBuiltin": False,
                    "enabled": True
              }
            ]

            create_resp = requests.post(import_group_url, headers=headers, verify=False, data=json.dumps(test_payload))

            pprint(create_resp.text)

    except Exception as e:
        print("Unexpected error:", str(e))


if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    PARSER = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=RawTextHelpFormatter)
    PARSER.add_argument("--ip", "-i", required=True, help="OME Appliance IP")
    PARSER.add_argument("--user", "-u", required=False,
                        help="Username for the OME Appliance", default="admin")
    PARSER.add_argument("--password", "-p", required=True,
                        help="Password for the OME Appliance")

    ARGS = PARSER.parse_args()
    duplicate_bug(ARGS.ip, ARGS.user, ARGS.password)

