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


def get_device_list(ome_ip_address: str, headers: dict) -> list:
    """
    Retrieves a list of all devices being handled by this OME server

    Args:
        ome_ip_address: The IP address of the OME server
        headers: Headers used for authentication to the OME server

    Returns: A list of all devices managed by the this OME server

    """

    logging.info("Retrieving a list of all devices...")
    next_link_url = "https://%s/api/DeviceService/Devices" % ome_ip_address
    device_data = None

    while next_link_url is not None:
        device_response = requests.get(next_link_url, headers=headers, verify=False)
        next_link_url = None
        if device_response.status_code == 200:
            data = device_response.json()
            if data['@odata.count'] <= 0:
                logging.error("No devices are managed by OME server: " + ome_ip_address + ". Exiting.")
                return []
            if '@odata.nextLink' in data:
                next_link_url = "https://%s" + data['@odata.nextLink']
            if device_data is None:
                device_data = data["value"]
            else:
                device_data += data["value"]
        else:
            logging.error("Unable to retrieve device list from %s" % ome_ip_address)
            exit(1)

    return device_data


def get_group_id_by_name(ome_ip_address: str, group_name: str, headers: dict) -> int:
    """
    Retrieves the ID of a group given its name.

    Args:
        ome_ip_address: The IP address of the OME server
        group_name: The name of the group whose ID you want to resolve.
        headers: Headers used for authentication to the OME server

    Returns: Returns the ID of the group as an integer, -1 if an error occurred, or 0 if the group was not found.

    """

    print("Searching for the requested group.")
    groups_url = "https://%s/api/GroupService/Groups?$filter=Name eq '%s'" % (ome_ip_address, group_name)

    group_response = requests.get(groups_url, headers=headers, verify=False)

    if group_response.status_code == 200:
        json_data = json.loads(group_response.content)

        if json_data['@odata.count'] > 1:
            logging.warning("WARNING: We found more than one name that matched the group name: " + group_name +
                            ". We are picking the first entry.")
        if json_data['@odata.count'] == 1 or json_data['@odata.count'] > 1:
            group_id = json_data['value'][0]['Id']
            if not isinstance(group_id, int):
                logging.error("The server did not return an integer ID. Something went wrong.")
                return -1
            return group_id
        else:
            logging.error("Error: We could not find the group " + group_name)
            return 0
    else:
        logging.error("Unable to retrieve groups.")
        return -1


def get_device_id_by_name(ome_ip_address: str, device_name: str, headers: dict) -> int:
    """
    Resolves the name of a server to an OME ID

    Args:
        ome_ip_address: IP address of the OME server
        device_name: Name of the device whose ID you want to resolve
        headers: Headers used for authentication to the OME server

    Returns:
        The ID of the server or 0 if it couldn't find it
    """

    url = "https://%s/api/DeviceService/Devices?$filter=DeviceName eq \'%s\'" % (ome_ip_address, device_name)

    response = requests.get(url, headers=headers, verify=False)
    logging.info("Getting the device ID for system with name " + device_name + "...")

    if response.status_code == 200:
        json_data = response.json()

        if json_data['@odata.count'] > 1:
            logging.warning("WARNING: We found more than one name that matched the device name: " + device_name +
                            ". We are skipping this entry.")
        elif json_data['@odata.count'] == 1:
            server_id = json_data['value'][0]['Id']
            if not isinstance(server_id, int):
                logging.error("The server did not return an integer ID. Something went wrong.")
                return -1
            return server_id
        else:
            logging.warning("WARNING: No results returned for device ID look up for name " + device_name +
                            ". Skipping it.")
            return 0
    else:
        logging.error("Connection failed with response code " + str(response.status_code) +
                      " while we were retrieving a device ID from the server.")
        return -1


def add_device_to_static_group(ome_ip_address: str, ome_username: str, ome_password: str, group_name: str,
                               device_names: list = None, device_tags: list = None):
    """
    Adds a device to an existing static group

    Args:
        ome_ip_address: IP address of the OME server
        ome_username:  Username for OME
        ome_password: OME password
        group_name: The group name to which you want to add servers
        device_names: A list of device names which you want added to the group
        device_tags: A list of device service tags which you want added to the group

    """

    try:
        session_url = 'https://%s/api/SessionService/Sessions' % ome_ip_address
        group_add_device_url = "https://%s/api/GroupService/Actions/GroupService.AddMemberDevices" % ome_ip_address
        headers = {'content-type': 'application/json'}
        user_details = {'UserName': ome_username,
                        'Password': ome_password,
                        'SessionType': 'API'}

        session_info = requests.post(session_url, verify=False,
                                     data=json.dumps(user_details),
                                     headers=headers)
        if session_info.status_code == 201:
            headers['X-Auth-Token'] = session_info.headers['X-Auth-Token']

            group_id = get_group_id_by_name(ome_ip_address, group_name, headers)

            device_ids = []
            if device_names:
                for device in device_names:
                    device_id = get_device_id_by_name(ome_ip_address, device, headers)
                    if device_id != 0:
                        device_ids.append(device_id)
            elif device_tags:
                device_list = get_device_list(ome_ip_address, headers)

                # Create id - service tag index to avoid O(n) lookups on each search
                # This is relevant when operating on hundreds of devices
                id_service_tag_dict = {}
                for device in device_list:
                    id_service_tag_dict[device["DeviceServiceTag"]] = device["Id"]

                # Check for each service tag in our index
                for device_tag in device_tags:
                    if device_tag in id_service_tag_dict:
                        device_ids.append(id_service_tag_dict[device_tag])
                    else:
                        logging.warning("WARNING: Could not find the service tag " + device_tag + ". Skipping.")

            if len(device_ids) > 0:
                # Add devices to the group
                payload = {
                    "GroupId": group_id,
                    "MemberDeviceIds": device_ids
                }
                create_resp = requests.post(group_add_device_url, headers=headers,
                                            verify=False, data=json.dumps(payload))
                if create_resp.status_code == 200 or create_resp.status_code == 204:
                    if create_resp.text != "":
                        logging.info("Finished adding devices to group. Response returned was: ", create_resp.text)
                    else:
                        logging.info("Finished adding devices to group.")
                elif create_resp.status_code == 400 \
                        and "Unable to update group members because the entered ID(s)" in \
                        json.loads(create_resp.content)["error"]["@Message.ExtendedInfo"][0]["Message"]:
                    logging.error("The IDs " +
                                  str(json.loads(create_resp.content)["error"]["@Message.ExtendedInfo"][0]
                                      ["MessageArgs"]) + " were invalid. This usually means the servers were already "
                                                         "in the requested group.")
                elif create_resp.status_code == 400:
                    logging.error("Device add failed. Error:")
                    logging.error(json.dumps(create_resp.json(), indent=4, sort_keys=False))
                else:
                    logging.error("Unknown error occurred. Received HTTP response code: "
                                  + str(create_resp.status_code) + " with error: " + create_resp.text)
    except Exception as e:
        logging.error("Unexpected error:", str(e))
