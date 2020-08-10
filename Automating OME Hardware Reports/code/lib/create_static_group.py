#
#  Python script using OME API to create a new static group
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
   Script to create a new static group

DESCRIPTION:
   This script exercises the OME REST API to create a new static
   group. The user is responsible for adding devices to the
   group once the group has been successfully created.
   For authentication X-Auth is used over Basic Authentication
   Note that the credentials entered are not stored to disk.
"""

import json
import requests
import logging


def create_static_group(ip_address: str, user_name: str, password: str, group_name: str, parent_id: int = None):
    """ Authenticate with OME and enumerate groups """
    try:
        session_url = 'https://%s/api/SessionService/Sessions' % ip_address
        group_url = "https://%s/api/GroupService/Groups?$filter=Name eq 'Static Groups'" % ip_address
        headers = {'content-type': 'application/json'}
        user_details = {'UserName': user_name,
                        'Password': password,
                        'SessionType': 'API'}

        session_info = requests.post(session_url, verify=False,
                                     data=json.dumps(user_details),
                                     headers=headers)
        if session_info.status_code == 201:
            headers['X-Auth-Token'] = session_info.headers['X-Auth-Token']
            response = requests.get(group_url, headers=headers, verify=False)
            if response.status_code == 200:
                json_data = response.json()
                if json_data['@odata.count'] > 0:
                    # Technically there should be only one result in the filter
                    group_id = json_data['value'][0]['Id']
                    if parent_id:
                        group_payload = {"GroupModel": {
                            "Name": group_name,
                            "Description": "",
                            "MembershipTypeId": 12,
                            "ParentId": parent_id}
                        }
                    else:
                        group_payload = {"GroupModel": {
                            "Name": group_name,
                            "Description": "",
                            "MembershipTypeId": 12,
                            "ParentId": int(group_id)}
                        }
                    create_url = 'https://%s/api/GroupService/Actions/GroupService.CreateGroup' % ip_address
                    create_resp = requests.post(create_url, headers=headers,
                                                verify=False,
                                                data=json.dumps(group_payload))
                    if create_resp.status_code == 200:
                        logging.info("New group created : ID = " + str(create_resp.text))
                        return ("New group created : ID =", str(create_resp.text)), 200
                    elif create_resp.status_code == 400:
                        logging.error("Group creation failed. Bad input parameters passed.")
                        return "Group creation failed. Bad input parameters passed.", 400
            else:
                logging.error("Unable to retrieve group list from %s" % ip_address)
                return ("Unable to retrieve group list from %s" % ip_address), 400
        else:
            logging.error("Unable to create a session with appliance %s" % ip_address)
            return ("Unable to create a session with appliance %s" % ip_address), 400
    except Exception as e:
        logging.error("Unexpected error:", str(e))
        return ("Unexpected error:", str(e)), 500
