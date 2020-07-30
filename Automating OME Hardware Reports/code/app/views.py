#
# _author_ = Grant Curell <grant_curell@Dell.com>
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

from flask import request
from flask_cors import CORS
from app import app
from lib.discover_device import discover_device, get_job_id, track_job_to_completion
from lib.ome import authenticate_with_ome, get_ips
import json
import logging
import time

CORS(app)


@app.route('/api/discover', methods=['PUT'])
def lookup():

    json_data = request.get_json()

    if "target_ip_addresses" not in json_data:
        logging.error("JSON data is missing the field \'target_ip_addresses\'")
        return app.response_class(status=400)
    elif "ome_ip_address" not in json_data:
        logging.error("JSON data is missing the field \'ome_ip_address\'")
        return app.response_class(status=400)
    elif "user_name" not in json_data:
        logging.error("JSON data is missing the field \'user_name\'")
        return app.response_class(status=400)
    elif "password" not in json_data:
        logging.error("JSON data is missing the field \'password\'")
        return app.response_class(status=400)
    elif "discover_user_name" not in json_data:
        logging.error("JSON data is missing the field \'discover_user_name\'")
        return app.response_class(status=400)
    elif "discover_password" not in json_data:
        logging.error("JSON data is missing the field \'discover_password\'")
        return app.response_class(status=400)
    elif "target_ips" not in json_data:
        logging.error("JSON data is missing the field \'target_ips\'")
        return app.response_class(status=400)
    elif "device_type" not in json_data:
        logging.error("JSON data is missing the field \'device_type\'")
        return app.response_class(status=400)

    target_ip_addresses = get_ips(json_data["target_ip_addresses"])
    ome_ip_address = json_data["ome_ip_address"]
    user_name = json_data["user_name"]
    password = json_data["password"]
    discover_user_name = json_data["discover_user_name"]
    discover_password = json_data["discover_password"]
    device_type = "device_type"

    try:
        auth_success, headers = authenticate_with_ome(ome_ip_address, user_name,
                                                      password)
        if auth_success:
            discover_resp = discover_device(ome_ip_address, headers,
                                            discover_user_name, discover_password,
                                            target_ip_addresses, device_type)
            if discover_resp.status_code == 201:
                logging.info("Discovering devices.....")
                time.sleep(30)
                discovery_config_group_id = (discover_resp.json())["DiscoveryConfigGroupId"]
                job_id = get_job_id(ome_ip_address, headers, discovery_config_group_id)
                if job_id != -1:
                    track_job_to_completion(ome_ip_address, headers, job_id)
            else:
                logging.error("unable to discover devices ", discover_resp.text)
    except Exception as e:
        logging.error("Unexpected error:", str(e))


    if len(results) > 0:
        return json.dumps(results)