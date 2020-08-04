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
from lib.ome import authenticate_with_ome, get_ips
from urllib3 import disable_warnings
import pylightxl as xl
import json
import logging
import time
import requests

CORS(app)

servers = {"192.168.1.10": "12446", "192.168.1.45": "12902"}

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
    "password": "I.am.ghost.47"}' 127.0.0.1:5000/api/hardware_inventory -H "Content-Type: application/json"
    """

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
                            if "Id" in card:
                                device_inventories[identifier]["PCI Cards"][i]["ID"] = card["Id"]
                            else:
                                logging.warning("Id not present for this device. Skipping. "
                                                "It will not be used for comparison")
                                device_inventories[identifier]["PCI Cards"][i]["ID"] = "None"
                            if "SlotNumber" in card:
                                device_inventories[identifier]["PCI Cards"][i]["Slot Number"] = card["SlotNumber"]
                            else:
                                logging.warning("SlotNumber not present for this device. Skipping. "
                                                "It will not be used for comparison")
                                device_inventories[identifier]["PCI Cards"][i]["Slot Number"] = "None"
                            if "Manufacturer" in card:
                                device_inventories[identifier]["PCI Cards"][i]["Manufacturer"] = card["Manufacturer"]
                            else:
                                logging.warning("Manufacturer not present for this device. Skipping. "
                                                "It will not be used for comparison")
                                device_inventories[identifier]["PCI Cards"][i]["Manufacturer"] = "None"
                            if "Description" in card:
                                device_inventories[identifier]["PCI Cards"][i]["Description"] = card["Description"]
                            else:
                                logging.warning("Description not present for this device.")
                                device_inventories[identifier]["PCI Cards"][i]["Description"] = "None"
                            if "DatabusWidth":
                                device_inventories[identifier]["PCI Cards"][i]["Databus Width"] = card["DatabusWidth"]
                            else:
                                logging.warning("DatabusWidth not present for this device. Skipping. "
                                                "It will not be used for comparison")
                                device_inventories[identifier]["PCI Cards"][i]["DatabusWidth"] = "None"
                            device_inventories[identifier]["PCI Cards"][i]["Slot Length"] = card["SlotLength"]
                            device_inventories[identifier]["PCI Cards"][i]["Slot Type"] = card["SlotType"]
                            i = i + 1
                    elif item["InventoryType"] == "serverProcessors":
                        logging.debug("Processing processors (haha) for " + ip)
                        device_inventories[identifier]["Processors"] = {}
                        for i, processor in enumerate(item["InventoryInfo"]):
                            device_inventories[identifier]["Processors"][i] = {}
                            device_inventories[identifier]["Processors"][i]["ID"] = processor["Id"]
                            device_inventories[identifier]["Processors"][i]["Family"] = processor["Family"]
                            device_inventories[identifier]["Processors"][i]["Max Speed"] = processor["MaxSpeed"]
                            device_inventories[identifier]["Processors"][i]["Slot Number"] = processor["SlotNumber"]
                            device_inventories[identifier]["Processors"][i]["Number of Cores"] \
                                = processor["NumberOfCores"]
                            device_inventories[identifier]["Processors"][i]["Brand Name"] = processor["BrandName"]
                            device_inventories[identifier]["Processors"][i]["Model Name"] = processor["ModelName"]
                    elif item["InventoryType"] == "serverPowerSupplies":
                        logging.debug("Processing power supplies for " + ip)
                        device_inventories[identifier]["Power Supplies"] = {}
                        for i, power_supply in enumerate(item["InventoryInfo"]):
                            device_inventories[identifier]["Power Supplies"][i] = {}
                            device_inventories[identifier]["Power Supplies"][i]["ID"] = power_supply["Id"]
                            device_inventories[identifier]["Power Supplies"][i]["Location"] = power_supply["Location"]
                            device_inventories[identifier]["Power Supplies"][i]["Output Watts"] \
                                = power_supply["OutputWatts"]
                            device_inventories[identifier]["Power Supplies"][i]["Firmware Version"] \
                                = power_supply["FirmwareVersion"]
                            device_inventories[identifier]["Power Supplies"][i]["Model"] = power_supply["Model"]
                            device_inventories[identifier]["Power Supplies"][i]["Serial Number"] \
                                = power_supply["SerialNumber"]
                    elif item["InventoryType"] == "serverArrayDisks":
                        logging.debug("Processing disks for " + ip)
                        device_inventories[identifier]["Disks"] = {}
                        for i, disk in enumerate(item["InventoryInfo"]):
                            device_inventories[identifier]["Disks"][i] = {}
                            device_inventories[identifier]["Disks"][i]["ID"] = disk["Id"]
                            if "SerialNumber" in disk:  # TODO - need to account for this
                                device_inventories[identifier]["Disks"][i]["Serial Number"] = disk["SerialNumber"]
                            device_inventories[identifier]["Disks"][i]["Model Number"] = disk["ModelNumber"]
                            device_inventories[identifier]["Disks"][i]["Enclosure ID"] = disk["EnclosureId"]
                            device_inventories[identifier]["Disks"][i]["Size"] = disk["Size"]
                            device_inventories[identifier]["Disks"][i]["Bus Type"] = disk["BusType"]
                            device_inventories[identifier]["Disks"][i]["Media Type"] = disk["MediaType"]
                    elif item["InventoryType"] == "serverMemoryDevices":
                        logging.debug("Processing memory for " + ip)
                        device_inventories[identifier]["Memory"] = {}
                        for i, memory in enumerate(item["InventoryInfo"]):
                            device_inventories[identifier]["Memory"][i] = {}
                            device_inventories[identifier]["Memory"][i]["ID"] = memory["Id"]
                            device_inventories[identifier]["Memory"][i]["Name"] = memory["Name"]
                            device_inventories[identifier]["Memory"][i]["Size"] = memory["Size"]
                            device_inventories[identifier]["Memory"][i]["Manufacturer"] = memory["Manufacturer"]
                            device_inventories[identifier]["Memory"][i]["Part Number"] = memory["PartNumber"]
                            device_inventories[identifier]["Memory"][i]["Serial Number"] = memory["SerialNumber"]
                            device_inventories[identifier]["Memory"][i]["Speed"] = memory["Speed"]
                            device_inventories[identifier]["Memory"][i]["Current Operating Speed"] \
                                = memory["CurrentOperatingSpeed"]
                            device_inventories[identifier]["Memory"][i]["Device Description"] \
                                = memory["DeviceDescription"]
                    elif item["InventoryType"] == "serverRaidControllers":
                        logging.debug("Processing RAID controllers for " + ip)
                        device_inventories[identifier]["RAID Controllers"] = {}
                        for i, raid_controller in enumerate(item["InventoryInfo"]):
                            device_inventories[identifier]["RAID Controllers"][i] = {}
                            device_inventories[identifier]["RAID Controllers"][i]["ID"] = raid_controller["Id"]
                            device_inventories[identifier]["RAID Controllers"][i]["Name"] = raid_controller["Name"]
                            device_inventories[identifier]["RAID Controllers"][i]["Device Description"] \
                                = raid_controller["DeviceDescription"]
                            device_inventories[identifier]["RAID Controllers"][i]["Firmware Version"] \
                                = raid_controller["FirmwareVersion"]
                            device_inventories[identifier]["RAID Controllers"][i]["PCI Slot"] \
                                = raid_controller["PciSlot"]

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
        db.add_ws(sheet_name,
                  {'A1': {'v': 10, 'f': '', 's': ''}, 'A2': {'v': 20, 'f': '', 's': ''}})  # TODO - I need to fix this
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

