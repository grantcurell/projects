#
#  Python script using OME API to get list of groups
#
# _author_ = Updated by: Grant Curell <grant_curell@dell.com>
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
"""
SYNOPSIS:
   Script to get the list of groups managed by OM Enterprise

DESCRIPTION:
   This script exercises the OME REST API to get a list of groups
   currently being managed by that instance. For authentication X-Auth
   is used over Basic Authentication
   Note that the credentials entered are not stored to disk.

EXAMPLE:
   python get_group_list.py --ip <xx> --user <username> --password <pwd>
"""
import json
import requests
import logging


def get_group_list(ip_address: str, user_name: str, password: str, group_name: str = None):
    """
    Get a list of all groups in OME or find a specific group
    """

    """ Authenticate with OME and enumerate groups """
    try:
        session_url = 'https://%s/api/SessionService/Sessions' % ip_address
        group_url = 'https://%s/api/GroupService/Groups' % ip_address
        headers = {'content-type': 'application/json'}
        user_details = {'UserName': user_name,
                        'Password': password,
                        'SessionType': 'API'}

        session_info = requests.post(session_url, verify=False,
                                     data=json.dumps(user_details),
                                     headers=headers)
        if session_info.status_code == 201:
            headers['X-Auth-Token'] = session_info.headers['X-Auth-Token']
            logging.info(headers['X-Auth-Token'])
            response = requests.get(group_url, headers=headers, verify=False)
            if response.status_code == 200:
                groups = response.json()
                if group_name:
                    for group in groups["value"]:
                        if group["Name"] == group_name:
                            return group, 200
                    return ("Could not find group" + group_name + " in the OME group list."), 404
                else:
                    return groups, 200
            else:
                logging.info("Unable to retrieve group list from %s" % ip_address)
                return ("Unable to retrieve group list from %s" % ip_address), 400
        else:
            logging.info("Unable to create a session with appliance %s" % ip_address)
            return ("Unable to create a session with appliance %s" % ip_address), 400
    except Exception as e:
        logging.info("Unexpected error:", str(e))
        return ("Unexpected error:", str(e)), 500
