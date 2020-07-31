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
import requests
from urllib3 import disable_warnings

CORS(app)

servers = {'192.168.1.10': 12446}

health_mapping = {
    "1000": "healthy",
    "2000": "unknown",
    "3000": "warning",
    "4000": "critical",
    "5000": "nostatus"
}

# This just stops urllib3 from complaining endlessly that we're making insecure connections. I know. I didn't set it up
# to do proper encryption. Sue me.
disable_warnings()

def _validate_ome_and_target(json_data: dict) -> bool:

    if "target_ips" not in json_data:
        logging.error("JSON data is missing the field \'target_ips\'")
        return False
    elif "ome_ip_address" not in json_data:
        logging.error("JSON data is missing the field \'ome_ip_address\'")
        return False
    elif "user_name" not in json_data:
        logging.error("JSON data is missing the field \'user_name\'")
        return False
    elif "password" not in json_data:
        logging.error("JSON data is missing the field \'password\'")
        return False

    return True


def get_device_id_by_ip(ome_ip_address: str, target_ip_address: str, headers: dict) -> str:

    url = "https://%s/api/DeviceService/Devices?$filter=DeviceName eq \'%s\'" % (ome_ip_address, target_ip_address)

    response = requests.get(url, headers=headers, verify=False)

    if response.status_code == 200:
        json_data = response.json()
        if json_data['@odata.count'] == 1:
            return json_data['value'][0]['Id']
        elif json_data['@odata.count'] > 1:
            logging.warning("WARNING: We found more than one name that matched " + target_ip_address + ". Returning "
                                                                                                       "the first.")
            return json_data['value'][0]['Id']
        else:
            logging.error("Not results returned for device ID look up for name " + target_ip_address)
            return ""
    else:
        return ""


@app.route('/api/discover', methods=['PUT'])
def discover():
    """
    Discovers a list of devices based on input

    Example curl:
    
    curl -XPUT -d '{"target_ips": "192.168.1.10", "ome_ip_address": "192.168.1.18", "user_name": "admin", 
    "password": "password", "discover_user_name": "root", "discover_password": "password", 
    "device_type": "server"}' 127.0.0.1:5000/api/discover -H "Content-Type: application/json"
    """

    json_data = request.get_json()

    if not _validate_ome_and_target(json_data):
        return 400
    elif "discover_user_name" not in json_data:
        logging.error("JSON data is missing the field \'discover_user_name\'")
        return "JSON data is missing the field \'discover_user_name\'", 400
    elif "discover_password" not in json_data:
        logging.error("JSON data is missing the field \'discover_password\'")
        return "JSON data is missing the field \'discover_password\'", 400
    elif "device_type" not in json_data:
        logging.error("JSON data is missing the field \'device_type\'")
        return "JSON data is missing the field \'device_type\'", 400

    target_ips = get_ips(json_data["target_ips"])
    ome_ip_address = json_data["ome_ip_address"]
    user_name = json_data["user_name"]
    password = json_data["password"]
    discover_user_name = json_data["discover_user_name"]
    discover_password = json_data["discover_password"]
    device_type = json_data["device_type"]

    try:
        auth_success, headers = authenticate_with_ome(ome_ip_address, user_name, password)
        if auth_success:
            discover_resp = discover_device(ome_ip_address, headers,
                                            discover_user_name, discover_password,
                                            target_ips, device_type)
            if discover_resp.status_code == 201:
                logging.info("Discovering devices.....")
                time.sleep(30)
                discovery_config_group_id = (discover_resp.json())["DiscoveryConfigGroupId"]
                job_id = get_job_id(ome_ip_address, headers, discovery_config_group_id)
                if job_id != -1:
                    track_job_to_completion(ome_ip_address, headers, job_id)
            else:
                logging.error("unable to discover devices ", discover_resp.text)
                return "unable to discover devices ", discover_resp.text, 400
        else:
            logging.warning("Failed to create a session to OpenManage. Are you sure your username and password for OME"
                            " are correct?")
            return "Failed to create a session to OpenManage. Are you sure your username and password for OME " \
                   "are correct?", 401
    except Exception as e:
        logging.error("Unexpected error:", str(e))
        return "Unexpected error:" + str(e), 500

    for ip in target_ips:
        server_id = get_device_id_by_ip(ome_ip_address, ip, headers)
        if server_id:
            servers[ip] = server_id
        else:
            logging.warning("Error: couldn't resolve the name " + ip + " to a device ID.")
            return "Error: couldn't resolve the name " + ip + " to a device ID.", 400

    return 200


@app.route('/api/hardware_health', methods=['GET'])
def hardware_health():

    json_data = request.get_json()

    if not _validate_ome_and_target(json_data):
        return 400

    target_ips = get_ips(json_data["target_ips"])
    ome_ip_address = json_data["ome_ip_address"]
    user_name = json_data["user_name"]
    password = json_data["password"]

    auth_success, headers = authenticate_with_ome(ome_ip_address, user_name, password)
    server_health = {}

    for ip in target_ips:
        logging.info("Getting the health for " + ip)
        url = 'https://%s/api/DeviceService/Devices(%s)/SubSystemHealth' % (ome_ip_address, servers[ip])
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code == 501:
            logging.error("Failed to retrieve health. Error received " + str(response.content))
            return "Failed to retrieve health. Error received " + str(response.content), 501
        else:
            content = json.loads(response.content)
            if content["@odata.count"] > 0:
                server_health[ip] = {}
                for item in content['value']:
                    if item["@odata.type"] == "#DeviceService.SubSystemHealthFaultModel":
                        server_health[ip]["errors"] = {}
                        for i, error in enumerate(item["FaultList"]):
                            server_health[ip]["errors"][i] = {}
                            if "Fqdd" in error:
                                server_health[ip]["errors"][i]["location"] = error["Fqdd"]
                            if "MessageId" in error:
                                server_health[ip]["errors"][i]["messageid"] = error["MessageId"]
                            if "Message" in error:
                                server_health[ip]["errors"][i]["message"] = error["Message"]
                            if "Severity" in error:
                                server_health[ip]["errors"][i]["severity"] = health_mapping[error["Severity"]]
                            if "SubSystem" in error:
                                server_health[ip]["errors"][i]["subsystem"] = error["SubSystem"]
                            if "RecommendedAction" in error:
                                server_health[ip]["errors"][i]["recommended_action"] = error["RecommendedAction"]
                        server_health[ip]["health"] = health_mapping[item["RollupStatus"]]
                        break
            else:
                logging.error("We successfully retrieved the server health, but there were no values. We aren't sure"
                              " why this would happen.")
                return "We successfully retrieved the server health, but there were no values. We aren't sure " \
                       "why this would happen.", 400
        logging.info("Retrieved health for " + ip)
    return json.dumps(server_health), 201, {'Content-Type': 'application/json'}


@app.route('/api/hardware_inventory', methods=['GET'])
def hardware_inventory():

    json_data = request.get_json()

    if not _validate_ome_and_target(json_data):
        return 400

    target_ips = get_ips(json_data["target_ips"])
    ome_ip_address = json_data["ome_ip_address"]
    user_name = json_data["user_name"]
    password = json_data["password"]

    auth_success, headers = authenticate_with_ome(ome_ip_address, user_name, password)
    server_health = {}

