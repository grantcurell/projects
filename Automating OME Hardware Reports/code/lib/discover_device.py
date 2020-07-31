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

"""
SYNOPSIS:
   Script to discover devices managed by OM Enterprise
DESCRIPTION:
   This script exercises the OME REST API to discover devices.
   For authentication X-Auth is used over Basic Authentication.
   Note that the credentials entered are not stored to disk.
EXAMPLE:
   python discover_device.py --ip <ip addr> --user admin
    --password <passwd> --targetUserName <user name>
    --targetPassword <password> --deviceType <{Device_Type}>
    --targetIpAddresses <10.xx.xx.x,10.xx.xx.xx-10.yy.yy.yy,10.xx.xx.xx> or --targetIpAddrCsvFile xyz.csv
    where {Device_Type} can be server,chassis
"""
import logging
import time
import json
import requests


def get_discover_device_payload():
    """ Payload for discovering devices """
    discovery_config_details = {
        "server": {
            "DiscoveryConfigGroupName": "Server Discovery",
            "DiscoveryConfigModels": [
                {
                    "DiscoveryConfigTargets": [
                        {
                            "NetworkAddressDetail": ""
                        }],
                    "ConnectionProfile": "{\"profileName\":\"\",\"profileDescription\": \
			              \"\",\"type\":\"DISCOVERY\",\"credentials\" :[{\"type\":\
			               \"WSMAN\",\"authType\":\"Basic\",\"modified\":false,\"credentials\":\
			               {\"username\":\"\",\"password\":\"\",\"port\":443,\"retries\":3,\"timeout\":\
			               60}}]}",
                    "DeviceType": [1000]}],
            "Schedule": {
                "RunNow": True,
                "Cron": "startnow"
            }
        },
        "network_switch": {
            "DiscoveryConfigGroupName": "Network switch Discovery ",
            "DiscoveryConfigModels": [{
                "DiscoveryConfigTargets": [
                    {
                        "NetworkAddressDetail": ""
                    }],
                "ConnectionProfile": "{\"profileName\" : \"\",\"profileDescription\" :\
					  \"\",  \"type\" : \"DISCOVERY\",\"credentials\" : [ {\"type\" :\
					  \"SNMP\",\"authType\" : \"Basic\",\"modified\" : false,\"credentials\" :\
					  {\"community\" : \"public\",\"port\" : 161,\"enableV3\" :\
					  false,\"enableV1V2\" : true,\"retries\" : 3,\"timeout\" : 60}} ]}",
                "DeviceType": [7000]}],
            "Schedule": {
                "RunNow": True,
                "Cron": "startnow"
            }
        },
        "dell_storage": {
            "DiscoveryConfigGroupName": "Storage Discovery",
            "DiscoveryConfigModels": [{
                "DiscoveryConfigTargets": [
                    {
                        "NetworkAddressDetail": ""
                    }],
                "ConnectionProfile": "{\"profileName\" : \"\",\"profileDescription\" : \
					  \"\",  \"type\" : \"DISCOVERY\",\"credentials\" : [ {\"type\" : \
					  \"SNMP\",\"authType\" : \"Basic\",\"modified\" : false,\"credentials\" : \
					  {\"community\" : \"public\",\"port\" : 161,\"enableV3\" : \
					  false,\"enableV1V2\" : true,\"retries\" : 3,\"timeout\" : 60}} ]}",
                "DeviceType": [5000]}],
            "Schedule": {
                "RunNow": True,
                "Cron": "startnow"
            }
        },
        "chassis": {
            "DiscoveryConfigGroupName": "Chassis Discovery",
            "DiscoveryConfigModels": [{
                "DiscoveryConfigTargets": [
                    {
                        "NetworkAddressDetail": ""
                    }],
                "ConnectionProfile": "{\"profileName\":\"\",\"profileDescription\":\
			 \"\",\"type\":\"DISCOVERY\",\"credentials\" :[{\"type\":\
			 \"WSMAN\",\"authType\":\"Basic\",\"modified\":false,\"credentials\":\
			 {\"username\":\"\",\"password\":\"\",\"port\":443,\"retries\":3,\"timeout\":\
			 60}}]}",
                "DeviceType": [2000]}],
            "Schedule": {
                "RunNow": True,
                "Cron": "startnow"}
        }
    }
    return discovery_config_details


def discover_device(ip_address, headers, discover_user_name, discover_password, list_of_ip, device_type):
    """ Discover devices """
    discover_payloads = get_discover_device_payload()
    discover_payload = discover_payloads.get(device_type)
    discover_payload["DiscoveryConfigModels"][0]["DiscoveryConfigTargets"][:] = []
    for ip_adds in list_of_ip:
        if ip_adds != ' ':
            discover_payload["DiscoveryConfigModels"][0]["DiscoveryConfigTargets"].append(
                {"NetworkAddressDetail": ip_adds})
    if device_type in ('server', 'chassis'):
        connection_profile = json.loads(discover_payload["DiscoveryConfigModels"][0]["ConnectionProfile"])
        connection_profile['credentials'][0]['credentials']['username'] = discover_user_name
        connection_profile['credentials'][0]['credentials']['password'] = discover_password
        discover_payload["DiscoveryConfigModels"][0]["ConnectionProfile"] = json.dumps(connection_profile)
    logging.debug(discover_payload)
    url = 'https://%s/api/DiscoveryConfigService/DiscoveryConfigGroups' % (ip_address)
    discover_resp = requests.post(url, headers=headers,
                                  data=json.dumps(discover_payload), verify=False)
    return discover_resp


def get_job_id(ip_address, headers, discovery_config_group_id):
    """ Get job id """
    job_id = -1
    url = 'https://%s/api/DiscoveryConfigService/Jobs' % (ip_address)
    job_resp = requests.get(url, headers=headers, verify=False)
    if job_resp.status_code == 200:
        job_resp_object = job_resp.json()
        if job_resp_object['@odata.count'] > 0:
            for value_object in job_resp_object['value']:
                if value_object['DiscoveryConfigGroupId'] == discovery_config_group_id:
                    job_id = value_object['JobId']
                    break
        else:
            logging.error("unable to get job id " + job_resp_object)
    else:
        logging.error("unable to get job id.Status code:  " + job_resp.status_code)
    return job_id


def track_job_to_completion(ip_address, headers, job_id):
    """ Tracks the  job to completion / error """
    job_status_map = {
        "2020": "Scheduled",
        "2030": "Queued",
        "2040": "Starting",
        "2050": "Running",
        "2060": "Completed",
        "2070": "Failed",
        "2090": "Warning",
        "2080": "New",
        "2100": "Aborted",
        "2101": "Paused",
        "2102": "Stopped",
        "2103": "Canceled"
    }

    max_retries = 20
    sleep_interval = 30
    failed_job_status = [2070, 2090, 2100, 2101, 2102, 2103]
    job_url = 'https://%s/api/JobService/Jobs(%s)' % (ip_address, job_id)
    loop_ctr = 0
    job_incomplete = True
    logging.info("Polling %s to completion ..." % job_id)
    while loop_ctr < max_retries:
        loop_ctr += 1
        time.sleep(sleep_interval)
        job_resp = requests.get(job_url, headers=headers, verify=False)
        if job_resp.status_code == 200:
            job_status = str((job_resp.json())['LastRunStatus']['Id'])
            job_status_str = job_status_map[job_status]
            logging.info("Iteration %s: Status of %s is %s" % (loop_ctr, job_id, job_status_str))
            if int(job_status) == 2060:
                job_incomplete = False
                logging.info("Completed discovering of devices successfully ... Exiting")
                break
            elif int(job_status) in failed_job_status:
                job_incomplete = False
                if job_status_str == "Warning":
                    logging.warning("Completed with errors")
                else:
                    logging.error("discovering of device failed ... ")
                job_hist_url = str(job_url) + "/ExecutionHistories"
                job_hist_resp = requests.get(job_hist_url, headers=headers, verify=False)
                if job_hist_resp.status_code == 200:
                    get_execution_detail(job_hist_resp, headers, job_hist_url)
                break
        else:
            logging.error("Unable to poll status of %s - Iteration %s " % (job_id, loop_ctr))
    if job_incomplete:
        logging.warning("Job %s incomplete after polling %s times...Check status" % (job_id, max_retries))


def get_execution_detail(job_hist_resp, headers, job_hist_url):
    """ Get execution details """
    job_history_id = str((job_hist_resp.json())['value'][0]['Id'])
    execution_hist_detail = "(" + job_history_id + ")/ExecutionHistoryDetails"
    job_hist_det_url = str(job_hist_url) + execution_hist_detail
    job_hist_det_resp = requests.get(job_hist_det_url,
                                     headers=headers,
                                     verify=False)
    if job_hist_det_resp.status_code == 200:
        logging.debug(job_hist_det_resp.text)
    else:
        logging.error("Unable to parse job execution history .. Exiting")
