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
from datetime import datetime
import os
import pickle

from flask import request, send_file
from flask_cors import CORS
from app import app
from lib.discover_device import discover_device, get_job_id, track_job_to_completion
from lib.create_static_group import create_static_group
from lib.get_group_list import get_group_list
from lib.ome import authenticate_with_ome, get_ips
from urllib3 import disable_warnings
import pylightxl as xl
import json
import logging
import time
import requests

CORS(app)

path = os.path.join(os.getcwd(), "discovery_scans", "latest_discovery.bin")
if os.path.isfile(path):
    with open(path, 'rb') as database:
        servers = pickle.load(database)
else:
    servers = {"192.168.1.10": "12446", "192.168.1.45": "12902"}  # TODO - this will need to be reverted

health_mapping = {
    "1000": "Healthy",
    "2000": "Unknown",
    "3000": "Warning",
    "4000": "Critical",
    "5000": "No status reported"
}

# This just stops urllib3 from complaining endlessly that we're making insecure connections. I know. I didn't set it up
# to do proper encryption. Sue me.
disable_warnings()


def _get_default_group_ids(ome_username, ome_password, ome_ip):

    groups, status_code = get_group_list(ome_ip, ome_username, ome_password, "In-Progress Servers")

    if status_code == 404:
        c_return_message, c_status_code = create_static_group(ome_ip, ome_username, ome_password, "In-Progress Servers")
        if c_status_code != 200:
            return c_return_message, c_status_code
    elif status_code != 200:
        # I abused types here. groups can also be an error message if it wasn't successful. This is probably a bad idea
        return groups, status_code

    in_progress_id = groups["Id"]

    groups, status_code = get_group_list(ome_ip, ome_username, ome_password, "Completed Servers")

    if status_code == 404:
        c_return_message, c_status_code = create_static_group(ome_ip, ome_username, ome_password, "Completed Servers")
        if c_status_code != 200:
            return c_return_message, c_status_code
    elif status_code != 200:
        # I abused types here. groups can also be an error message if it wasn't successful. This is probably a bad idea
        return groups, status_code

    completed_id = groups["Id"]

    return (in_progress_id, completed_id), 200

def _validate_ome_and_target(json_data: dict) -> bool:
    """
    Determines if well-formatted credentials were passed for OME
    """

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
            return str(json_data['value'][0]['Id'])
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
        return "Failed to validate OME and target IP information", 400
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
        server_id = str(get_device_id_by_ip(ome_ip_address, ip, headers))
        if server_id != "":
            servers[ip] = server_id
        else:
            logging.warning("Error: couldn't resolve the name " + str(ip) + " to a device ID. This might mean there "
                                                                            "was a login failure during discovery. "
                                                                            "Check the OME discovery logs for details.")
            return ("Error: couldn't resolve the name " + str(ip) + " to a device ID. This might mean there was a "
                                                                    "login failure during discovery. Check the OME "
                                                                    "discovery job logs for details.", 400)

    path = os.path.join(os.getcwd(), "discovery_scans")
    if not os.path.exists(path):
        os.mkdir(path)
    dtstring = datetime.now().strftime("%d-%b-%Y-%H%M")
    servers["GROUP_NAME"] = dtstring
    with open(os.path.join(path, dtstring + ".bin"), 'wb') as database:
        pickle.dump(servers, database)
    with open(os.path.join(path, "lastest_discovery.bin"), 'wb') as database:
        pickle.dump(servers, database)

    create_static_group(ome_ip_address, user_name, password, servers["GROUP_NAME"])

    return "Successfully discovered all servers", 200


@app.route('/api/hardware_health', methods=['GET'])
def hardware_health():
    """
    Retrieves the hardware's health

    Example curl:
    curl -XGET -d '{"target_ips": "192.168.1.10", "ome_ip_address": "192.168.1.18", "user_name": "admin",
    "password": "password"}' 127.0.0.1:5000/api/hardware_health -H "Content-Type: application/json"
    """

    json_data = request.get_json()

    if not _validate_ome_and_target(json_data):
        return "Failed to validate OME and target IP information", 400

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
                        if "FaultList" in item:
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
    """
    Retrieves the hardware inventory for a specified target

    curl -XGET -d '{"target_ips": "192.168.1.10", "ome_ip_address": "192.168.1.18", "user_name": "admin",
    "password": "password"}' 127.0.0.1:5000/api/hardware_inventory -H "Content-Type: application/json"
    """

    def _handle_keys(ome_field, ome_device, dict_field, dict_device):
        if ome_field in ome_device:
            device_inventories[identifier][dict_device][i][dict_field] = ome_device[ome_field]
        else:
            logging.warning(ome_field + " was not in OpenManage's database for device with ID " +
                            str(device_inventories[identifier][dict_device][i]["ID"]) + ". The device type was "
                            + dict_device + ". The host has idrac IP " + ip +
                            ". We are skipping the device. It will not be used for comparison.")
            device_inventories[identifier][dict_device][i][dict_field] = "None"

    json_data = request.get_json()

    if not _validate_ome_and_target(json_data):
        return "Failed to validate OME and target IP information", 400

    target_ips = get_ips(json_data["target_ips"])
    ome_ip_address = json_data["ome_ip_address"]
    user_name = json_data["user_name"]
    password = json_data["password"]
    inventory_type = None

    auth_success, headers = authenticate_with_ome(ome_ip_address, user_name, password)

    device_inventories = {}

    inventory_types = {
        "cpus": "serverProcessors",
        "os": "serverOperatingSystems",
        "disks": "serverArrayDisks",
        "controllers": "serverRaidControllers",
        "memory": "serverMemoryDevices"}

    for ip in target_ips:

        identifier = servers[ip]
        logging.info("Processing inventory for " + ip)

        inventory_url = "https://%s/api/DeviceService/Devices(%s)/InventoryDetails" % (ome_ip_address, identifier)
        if inventory_type:
            inventory_url = "https://%s/api/DeviceService/Devices(%s)/InventoryDetails(\'%s\')" \
                            % (ome_ip_address, identifier, inventory_types[inventory_type])
        inven_resp = requests.get(inventory_url, headers=headers, verify=False)
        if inven_resp.status_code == 200:
            logging.info("\n*** Inventory for device (%s) ***" % ip)
            content = json.loads(inven_resp.content)
            if content["@odata.count"] > 0:
                device_inventories[identifier] = {"idrac IP": ip}
                for item in content['value']:
                    if item["InventoryType"] == "serverDeviceCards":
                        logging.debug("Processing PCI cards for " + ip)
                        device_inventories[identifier]["PCI Cards"] = {}
                        i = 0
                        for card in item["InventoryInfo"]:
                            # Skip disks. Those are covered below.
                            if "Disk.Bay" in card["SlotNumber"] or "pci" not in card["SlotType"].lower():
                                continue
                            device_inventories[identifier]["PCI Cards"][i] = {}
                            _handle_keys("Id", card, "ID", "PCI Cards")
                            _handle_keys("SlotNumber", card, "Slot Number", "PCI Cards")
                            _handle_keys("Manufacturer", card, "Manufacturer", "PCI Cards")
                            _handle_keys("Description", card, "Description", "PCI Cards")
                            _handle_keys("DatabusWidth", card, "Databus Width", "PCI Cards")
                            _handle_keys("SlotLength", card, "Slot Length", "PCI Cards")
                            _handle_keys("SlotType", card, "Slot Type", "PCI Cards")
                            i = i + 1
                    elif item["InventoryType"] == "serverProcessors":
                        logging.debug("Processing processors (haha) for " + ip)
                        device_inventories[identifier]["Processors"] = {}
                        for i, processor in enumerate(item["InventoryInfo"]):
                            device_inventories[identifier]["Processors"][i] = {}
                            _handle_keys("Id", processor, "ID", "Processors")
                            _handle_keys("Family", processor, "Family", "Processors")
                            _handle_keys("MaxSpeed", processor, "Max Speed", "Processors")
                            _handle_keys("SlotNumber", processor, "Slot Number", "Processors")
                            _handle_keys("NumberOfCores", processor, "Number of Cores", "Processors")
                            _handle_keys("BrandName", processor, "Brand Name", "Processors")
                            _handle_keys("ModelName", processor, "Model Name", "Processors")
                    elif item["InventoryType"] == "serverPowerSupplies":
                        logging.debug("Processing power supplies for " + ip)
                        device_inventories[identifier]["Power Supplies"] = {}
                        for i, power_supply in enumerate(item["InventoryInfo"]):
                            device_inventories[identifier]["Power Supplies"][i] = {}
                            _handle_keys("Id", power_supply, "ID", "Power Supplies")
                            _handle_keys("Location", power_supply, "Location", "Power Supplies")
                            _handle_keys("OutputWatts", power_supply, "Output Watts", "Power Supplies")
                            _handle_keys("FirmwareVersion", power_supply, "Firmware Version", "Power Supplies")
                            _handle_keys("Model", power_supply, "Model", "Power Supplies")
                            _handle_keys("SerialNumber", power_supply, "Serial Number", "Power Supplies")
                    elif item["InventoryType"] == "serverArrayDisks":
                        logging.debug("Processing disks for " + ip)
                        device_inventories[identifier]["Disks"] = {}
                        for i, disk in enumerate(item["InventoryInfo"]):
                            device_inventories[identifier]["Disks"][i] = {}
                            _handle_keys("Id", disk, "ID", "Disks")
                            _handle_keys("SerialNumber", disk, "Serial Number", "Disks")
                            _handle_keys("ModelNumber", disk, "Model Number", "Disks")
                            _handle_keys("EnclosureId", disk, "Enclosure ID", "Disks")
                            _handle_keys("Size", disk, "Size", "Disks")
                            _handle_keys("BusType", disk, "Bus Type", "Disks")
                            _handle_keys("MediaType", disk, "Media Type", "Disks")
                    elif item["InventoryType"] == "serverMemoryDevices":
                        logging.debug("Processing memory for " + ip)
                        device_inventories[identifier]["Memory"] = {}
                        for i, memory in enumerate(item["InventoryInfo"]):
                            device_inventories[identifier]["Memory"][i] = {}
                            _handle_keys("Id", memory, "ID", "Memory")
                            _handle_keys("Name", memory, "Name", "Memory")
                            _handle_keys("Size", memory, "Size", "Memory")
                            _handle_keys("Manufacturer", memory, "Manufacturer", "Memory")
                            _handle_keys("PartNumber", memory, "Part Number", "Memory")
                            _handle_keys("SerialNumber", memory, "Serial Number", "Memory")
                            _handle_keys("Speed", memory, "Speed", "Memory")
                            _handle_keys("CurrentOperatingSpeed", memory, "Current Operating Speed", "Memory")
                            _handle_keys("DeviceDescription", memory, "Device Description", "Memory")
                    elif item["InventoryType"] == "serverRaidControllers":
                        logging.debug("Processing RAID controllers for " + ip)
                        device_inventories[identifier]["RAID Controllers"] = {}
                        for i, raid_controller in enumerate(item["InventoryInfo"]):
                            device_inventories[identifier]["RAID Controllers"][i] = {}
                            _handle_keys("Id", raid_controller, "ID", "RAID Controllers")
                            _handle_keys("Name", raid_controller, "Name", "RAID Controllers")
                            _handle_keys("DeviceDescription", raid_controller, "Device Description", "RAID Controllers")
                            _handle_keys("FirmwareVersion", raid_controller, "Firmware Version", "RAID Controllers")
                            _handle_keys("PciSlot", raid_controller, "PCI Slot", "RAID Controllers")

                    logging.debug("Finished device loop.")

        elif inven_resp.status_code == 400:
            logging.warning("Inventory type %s not applicable for device with ID %s" % (inventory_type, identifier))
            return "Inventory type %s not applicable for device with Id %s" % (inventory_type, identifier), 400
        else:
            logging.error("Unable to retrieve inventory for device %s due to status code %s"
                          % (identifier, inven_resp.status_code))
            return "Unable to retrieve inventory for device %s due to status code %s" \
                   % (identifier, inven_resp.status_code), 404

    logging.info("Writing excel file and pickle database for inventory.")
    db = xl.Database()
    for identifier, inventory in device_inventories.items():
        logging.info("Processing " + identifier)
        sheet_name = identifier + "-" + inventory["idrac IP"]
        db.add_ws(sheet_name, {'A1': {'v': '', 'f': '', 's': ''}})
        x = 1
        for subsystem, items in inventory.items():
            if subsystem == "idrac IP":
                continue
            y = 1
            db.ws(sheet_name).update_index(row=y, col=x, val=subsystem)
            logging.debug("Processing " + subsystem)
            for device, values in items.items():
                y = y + 1
                string = ""
                for key, value in values.items():
                    string = string + key + ": " + str(value) + "\n"
                db.ws(sheet_name).update_index(row=y, col=x, val=string)
            x = x + 1
    path = os.path.join(os.getcwd(), "inventories")
    if not os.path.exists(path):
        os.mkdir(path)
    dtstring = datetime.now().strftime("%d-%b-%Y-%H%M")
    xl.writexl(db, dtstring + ".xlsx")
    os.replace(dtstring + ".xlsx", os.path.join(path, dtstring + ".xlsx"))
    with open(os.path.join(path, dtstring + ".bin"), 'wb') as inventories:
        pickle.dump(device_inventories, inventories)
    with open(os.path.join(path, "last_inventory.bin"), 'wb') as inventories:
        pickle.dump(device_inventories, inventories)
    return send_file(os.path.join(path, dtstring + ".xlsx"), attachment_filename=dtstring + ".xlsx")


@app.route('/api/get_inventories', methods=['GET'])
def get_inventories():
    print("GET A LIST OF INVENTORIES HERE")  # TODO


@app.route('/api/compare_inventories', methods=['GET'])
def compare_inventories():
    """
    Compare two inventories and produce an excel sheet with the results

    curl -XGET -d '{"inventory1": "04-Aug-2020-1325.bin", "inventory2": "04-Aug-2020-1325.bin"}'
    127.0.0.1:5000/api/compare_inventories -H "Content-Type: application/json"
    """

    json_data = request.get_json()

    if "inventory1" in json_data:
        inventory1 = json_data["inventory1"]
    else:
        return "inventory1 missing. This is a required argument", 400

    if "inventory2" in json_data:
        inventory2 = json_data["inventory2"]
    else:
        return "inventory2 missing. This is a required argument", 400

    path = os.path.join(os.getcwd(), "inventories")

    logging.info("Reading binary database from the file \"" + str(os.path.join(path, inventory1)) + "\" from disk.")
    with open(os.path.join(path, inventory1), 'rb') as database:
        device_inventory_1 = pickle.load(database)

    logging.info("Reading binary database from the file \"" + str(os.path.join(path, inventory2)) + "\" from disk.")
    with open(os.path.join(path, inventory2), 'rb') as database:
        device_inventory_2 = pickle.load(database)

    db = xl.Database()

    device_inventory_2["12446"]["PCI Cards"][1]["Manufacturer"] = "New Manufacturer"
    device_inventory_2["12446"]["PCI Cards"][1]["Slot Number"] = "AHCI.Slot.2-2"
    device_inventory_2["12446"]["PCI Cards"][1]["Databus Width"] = "8x or x 8"
    device_inventory_2["12446"]["PCI Cards"][2]["Manufacturer"] = "New Manufacturer"
    device_inventory_2["12446"]["PCI Cards"][2]["Slot Number"] = "AHCI.Slot.2-2"
    device_inventory_2["12446"]["PCI Cards"][2]["Databus Width"] = "8x or x 8"
    device_inventory_2["12902"]["Processors"].pop(2)
    device_inventory_2["12902"]["Power Supplies"][2] = {"ID": 984, "Location": "PSU.Slot.3", "Output Watts": 9000, "Firmware Version": "00.3D.67", "Model": 'PWR SPLY,1600W,RDNT,DELTA', "Serial Number": "Stuff"}
    db.add_ws("Inventory Deltas",
              {'A1': {'v': "Service Tag", 'f': '', 's': ''},
               'B1': {'v': "System idrac IP", 'f': '', 's': ''},
               'C1': {'v': "OME System Identifier", 'f': '', 's': ''},
               'D1': {'v': "Effected Subsystem", 'f': '', 's': ''},
               'E1': {'v': "Change Made", 'f': '', 's': ''},
               'F1': {'v': "Component Details", 'f': '', 's': ''},
               'G1': {'v': "Updated Component Details", 'f': '', 's': ''},
               'H1': {'v': "Deltas", 'f': '', 's': ''}})

    y = 1

    for identifier, inventory in device_inventory_1.items():

        logging.info("Comparing inventory for device which had idrac IP of " + inventory["idrac IP"])

        if identifier in device_inventory_2:
            for subsystem, items in inventory.items():
                if subsystem == "idrac IP":
                    continue

                logging.debug("Processing " + subsystem)
                for device, values in items.items():
                    device_found = False
                    for comparison_device, comparison_device_values in device_inventory_2[identifier][subsystem].items():
                        if device_inventory_2[identifier][subsystem][comparison_device]["ID"] == values["ID"]:
                            device_found = True
                            logging.debug("Found match with device " + str(values["ID"]) + ". Processing comparison.")
                            changed_string = ""
                            original_string = ""
                            updated_string = ""
                            change_made = False
                            for key, value in values.items():
                                if device_inventory_2[identifier][subsystem][comparison_device][key] != value:
                                    change_made = True
                                    logging.info("Difference found in subsystem " + str(subsystem) + " on device " +
                                                 str(comparison_device) + " in key " + str(key))
                                    changed_string = changed_string + key + ": " + str(value) + " --> CHANGED TO --> " \
                                                     + device_inventory_2[identifier][subsystem][comparison_device][key]\
                                                     + "\n"
                                original_string = original_string + key + ": " + str(value) + "\n"
                                updated_string = updated_string + key + ": " + \
                                                 str(device_inventory_2[identifier][subsystem][comparison_device][key])\
                                                 + "\n"

                            if change_made:
                                y = y + 1
                                db.ws("Inventory Deltas").update_index(row=y, col=2,
                                                                       val=device_inventory_2[identifier]["idrac IP"])
                                db.ws("Inventory Deltas").update_index(row=y, col=3, val=identifier)
                                db.ws("Inventory Deltas").update_index(row=y, col=4, val=subsystem)
                                db.ws("Inventory Deltas").update_index(row=y, col=5, val="Component Updated")
                                db.ws("Inventory Deltas").update_index(row=y, col=6, val=original_string)
                                db.ws("Inventory Deltas").update_index(row=y, col=7, val=updated_string)
                                db.ws("Inventory Deltas").update_index(row=y, col=8, val=changed_string)

                    if not device_found:
                        y = y + 1
                        db.ws("Inventory Deltas").update_index(row=y, col=2, val=device_inventory_2[identifier]["idrac IP"])
                        db.ws("Inventory Deltas").update_index(row=y, col=3, val=identifier)
                        db.ws("Inventory Deltas").update_index(row=y, col=4, val=subsystem)
                        db.ws("Inventory Deltas").update_index(row=y, col=5, val="Component Removed")

                        string = ""
                        for key, value in values.items():
                            string = string + key + ": " + str(value) + "\n"

                        db.ws("Inventory Deltas").update_index(row=y, col=6, val=string)

        else:
            warning = "Device identifier " + identifier + " was found in inventory 1, but not in inventory 2. This " \
                      "corresponds to idrac IP " + inventory["idrac IP"] + ". This probably shouldn't have happened. " \
                      "The error is not fatal, but should be investigated]."
            logging.warning(warning)
            db.ws("Inventory Deltas").update_index(row=1, col=1, val=warning)  # TODO - fix

    for identifier, inventory in device_inventory_2.items():
        if identifier in device_inventory_1:
            for subsystem, items in inventory.items():
                if subsystem == "idrac IP":
                    continue
                for device, values in items.items():
                    device_found = False
                    for comparison_device, comparison_device_values in device_inventory_1[identifier][
                        subsystem].items():
                        if device_inventory_1[identifier][subsystem][comparison_device]["ID"] == values["ID"]:
                            device_found = True

                    if not device_found:
                        y = y + 1
                        db.ws("Inventory Deltas").update_index(row=y, col=2,
                                                               val=device_inventory_2[identifier]["idrac IP"])
                        db.ws("Inventory Deltas").update_index(row=y, col=3, val=identifier)
                        db.ws("Inventory Deltas").update_index(row=y, col=4, val=subsystem)
                        db.ws("Inventory Deltas").update_index(row=y, col=5, val="Component Added")

                        string = ""
                        for key, value in values.items():
                            string = string + key + ": " + str(value) + "\n"

                        db.ws("Inventory Deltas").update_index(row=y, col=6, val=string)

        else:
            warning = "Device identifier " + identifier + " was found in inventory 2, but not in inventory 1. This " \
                      "corresponds to idrac IP " + inventory["idrac IP"] + ". This probably shouldn't have happened. " \
                      "The error is not fatal, but should be investigated]."
            logging.warning(warning)
            db.ws("Inventory Deltas").update_index(row=1, col=1, val=warning)  # TODO - fix

    os.remove("comparison.xlsx")
    xl.writexl(db, "comparison.xlsx")
    return "Jobs done!", 200


@app.route('/api/remove_servers_from_ome', methods=['PUT'])
def remove_servers_from_ome():
    """
    Removes a set of servers from OME

    curl -XGET -d '{"target_ips": "192.168.1.45", "ome_ip_address": "192.168.1.18", "user_name": "admin",
    "password": "password"}' 127.0.0.1:5000/api/hardware_inventory -H "Content-Type: application/json"
    """

    json_data = request.get_json()

    if not _validate_ome_and_target(json_data):
        return "Failed to validate OME and target IP information", 400

    target_ips = get_ips(json_data["target_ips"])
    ome_ip_address = json_data["ome_ip_address"]
    user_name = json_data["user_name"]
    password = json_data["password"]

