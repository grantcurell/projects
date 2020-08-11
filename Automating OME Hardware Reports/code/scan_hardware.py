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

import argparse
from datetime import datetime
import os
import pickle
from lib.discover_device import discover_device, get_job_id, track_job_to_completion
from lib.ome import get_device_ids_by_idrac_ip, get_device_list
from lib.create_static_group import create_static_group
import lib.ome
from urllib3 import disable_warnings
import pylightxl as xl
import json
import logging
import time
import requests

# The servers dictionary has all servers listed by both ID->service tag and
discovery_scan_path = os.path.join(os.getcwd(), "discovery_scans", "latest_discovery.bin")
if os.path.isfile(discovery_scan_path):
    with open(discovery_scan_path, 'rb') as discovery_database:
        servers = pickle.load(discovery_database)
else:
    servers = {}

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


def _get_default_group_ids(headers: dict, ome_ip: str, ome_username: str, ome_password: str) -> tuple:
    """
    This internal function does a couple of things. It checks to see if the two default groups, In-Progress Servers and
    Completed Servers, already exist. If they don't it creates them. The outcome is it either creates them and returns
    their IDs or it gets the existing IDs.

    return if successful is of format (In-Progress Servers' ID, Completed Servers' ID), 200. If failure it is
    (failure text, status code)

    """

    in_progress_id = lib.ome.get_group_id_by_name(ome_ip, "In-Progress Servers", headers)

    # TODO need to double check this - it doesn't look like we're returning IDs
    if in_progress_id == 0:
        c_return_message, c_status_code = create_static_group(ome_ip, ome_username, ome_password, "In-Progress Servers")
        if c_status_code != 200:
            return c_return_message, c_status_code
        else:
            in_progress_id = lib.ome.get_group_id_by_name(ome_ip, "In-Progress Servers", headers)
    elif in_progress_id > 0:
        logging.info("Successfully retrieved group ID for In-Progress Servers")
    else:
        logging.error("Something went wrong retrieving the default groups.")
        return "Something went wrong retrieving the default groups.", 400

    """
    # TODO - This is for future use. See
    # https://github.com/dell/OpenManage-Enterprise/issues/32
    # Before I add the completed group I want the ability to delete groups and move servers
    completed_id = lib.ome.get_group_id_by_name(ome_ip, "Completed Servers", headers)

    if completed_id == 0:
        c_return_message, c_status_code = create_static_group(ome_ip, ome_username, ome_password, "Completed Servers")
        if c_status_code != 200:
            return c_return_message, c_status_code
        else:
            completed_id = lib.ome.get_group_id_by_name(ome_ip, "Completed Servers", headers)
    elif completed_id > 0:
        logging.info("Successfully retrieved group ID for Completed Servers")
    else:
        logging.error("Something went wrong retrieving the default groups.")
        return "Something went wrong retrieving the default groups.", 400
    """
    completed_id = -1
    # if in_progress_id > 0 and completed_id > 0:
    if in_progress_id > 0:
        return (in_progress_id, completed_id), 200
    else:
        return "Something went wrong retrieving the default groups.", 400


def discover(target_ips: str, ome_ip: str, ome_username: str, ome_password: str, discover_username: str,
             discover_password: str, device_type: str = "server") -> dict:
    """
    Discovers a list of devices based on input

    Example curl:

    curl -XPUT -d '{"target_ips": "192.168.1.10", "ome_ip_address": "192.168.1.18", "user_name": "admin",
    "password": "password", "discover_user_name": "root", "discover_password": "password",
    "device_type": "server"}' 127.0.0.1:5000/api/discover -H "Content-Type: application/json"
    """

    target_ips = lib.ome.get_ips(target_ips)

    try:
        auth_success, headers = lib.ome.authenticate_with_ome(ome_ip, ome_username, ome_password)
        if auth_success:
            discover_resp = discover_device(ome_ip, headers,
                                            discover_username, discover_password,
                                            target_ips, device_type)
            if discover_resp.status_code == 201:
                logging.info("Discovering devices.....")
                time.sleep(30)
                discovery_config_group_id = (discover_resp.json())["DiscoveryConfigGroupId"]
                job_id = get_job_id(ome_ip, headers, discovery_config_group_id)
                if job_id != -1:
                    track_job_to_completion(ome_ip, headers, job_id)
            else:
                logging.error("unable to discover devices ", discover_resp.text)
                return {}
        else:
            logging.error("Failed to create a session to OpenManage. Are you sure your username and password for OME "
                          "are correct?")
            return {}
    except Exception as e:
        logging.error("Unexpected error:", str(e))
        return {}

    logging.info("Getting list of IDs by idrac IP")
    device_ids_by_idrac = get_device_ids_by_idrac_ip(ome_ip, ome_username, ome_password)

    device_list = get_device_list(ome_ip, headers)

    # Create id - service tag index to avoid O(n) lookups on each search
    # This is relevant when operating on hundreds of devices
    id_service_tag_dict = {}
    for device in device_list:
        id_service_tag_dict[device["Id"]] = device["DeviceServiceTag"]

    for ip in target_ips:
        server_id = device_ids_by_idrac[ip]
        if server_id != "":
            servers[ip] = server_id
            servers[server_id] = id_service_tag_dict[servers[ip]]
        else:
            logging.warning("Error: couldn't resolve the name " + str(ip) + " to a device ID. This might mean there "
                                                                            "was a login failure during discovery. "
                                                                            "Check the OME discovery logs for details.")
            return {}

    auth_success, headers = lib.ome.authenticate_with_ome(ome_ip, ome_username, ome_password)
    path = os.path.join(os.getcwd(), "discovery_scans")
    if not os.path.exists(path):
        os.mkdir(path)
    dtstring = datetime.now().strftime("%d-%b-%Y-%H%M")
    servers["GROUP_NAME"] = dtstring
    with open(os.path.join(path, dtstring + ".bin"), 'wb') as database:
        pickle.dump(servers, database)
    with open(os.path.join(path, "latest_discovery.bin"), 'wb') as database:
        pickle.dump(servers, database)

    # I abused types here which I shouldn't have done, but did. groups is either a tuple with the ID of In-Progress
    # Servers and Completed Servers in a tuple or it is an error message.
    groups, status_code = _get_default_group_ids(headers, ome_ip, ome_username, ome_password)

    if status_code == 200:
        c_return_message, c_status_code = create_static_group(ome_ip, ome_username, ome_password,
                                                              servers["GROUP_NAME"], groups[0])
        logging.info(c_return_message)
        if c_status_code != 200:
            return {}
    else:
        logging.error(groups)
        return {}

    lib.ome.add_device_to_static_group(ome_ip, ome_username, ome_password, servers["GROUP_NAME"],
                                       device_names=target_ips)

    logging.info("Successfully discovered all servers. Check the group " + servers["GROUP_NAME"] + " for a list.")
    return servers


def hardware_health(target_ips: str, ome_ip: str, ome_username: str, ome_password: str) -> dict:
    """
    Retrieves the hardware's health

    Example curl:
    curl -XGET -d '{"target_ips": "192.168.1.10", "ome_ip_address": "192.168.1.18", "user_name": "admin",
    "password": "password"}' 127.0.0.1:5000/api/hardware_health -H "Content-Type: application/json"
    """

    target_ips = lib.ome.get_ips(target_ips)

    auth_success, headers = lib.ome.authenticate_with_ome(ome_ip, ome_username, ome_password)
    server_health = {}

    for ip in target_ips:
        if not ip in servers:
            logging.warning("WARNING: " + str(ip) + " not in the database. Has it been discovered? We're skipping "
                                                    "its health check.")
        else:
            logging.info("Getting the health for " + ip)
            url = 'https://%s/api/DeviceService/Devices(%s)/SubSystemHealth' % (ome_ip, servers[ip])
            response = requests.get(url, headers=headers, verify=False)
            if response.status_code != 200:
                logging.error("Failed to retrieve health. Error received " + str(json.loads(response.content)))
                return {}
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
                    logging.error("We successfully retrieved the server health, but there were no values. "
                                  "We aren't sure why this would happen.")
                    return {}
                logging.info("Retrieved health for " + ip)
    return server_health


def hardware_inventory(target_ips: str, ome_ip: str, ome_username: str, ome_password: str) -> tuple:
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

    target_ips = lib.ome.get_ips(target_ips)
    inventory_type = None

    auth_success, headers = lib.ome.authenticate_with_ome(ome_ip, ome_username, ome_password)

    device_inventories = {}

    inventory_types = {
        "cpus": "serverProcessors",
        "os": "serverOperatingSystems",
        "disks": "serverArrayDisks",
        "controllers": "serverRaidControllers",
        "memory": "serverMemoryDevices"}

    for ip in target_ips:

        if ip not in servers:
            logging.warning("IP " + str(ip) + " not in the local database. Has it been previously discovered?")
        else:
            identifier = servers[ip]
            logging.info("Processing inventory for " + ip)

            inventory_url = "https://%s/api/DeviceService/Devices(%s)/InventoryDetails" % (ome_ip, identifier)
            if inventory_type:
                inventory_url = "https://%s/api/DeviceService/Devices(%s)/InventoryDetails(\'%s\')" \
                                % (ome_ip, str(identifier), inventory_types[inventory_type])
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
                                _handle_keys("DeviceDescription", raid_controller, "Device Description",
                                             "RAID Controllers")
                                _handle_keys("FirmwareVersion", raid_controller, "Firmware Version", "RAID Controllers")
                                _handle_keys("PciSlot", raid_controller, "PCI Slot", "RAID Controllers")

                        logging.debug("Finished device loop.")

            elif inven_resp.status_code == 400:
                logging.warning("Inventory type %s not applicable for device with ID %s" % (inventory_type,
                                                                                            str(identifier)))
                return None
            else:
                logging.error("Unable to retrieve inventory for device %s due to status code %s"
                              % (str(identifier), inven_resp.status_code))
                return None

    logging.info("Writing pickle database for inventory.")
    db = xl.Database()
    for identifier, inventory in device_inventories.items():
        logging.info("Processing " + str(identifier))
        sheet_name = servers[identifier] + " - Inventory"
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
    if not os.path.exists(path):
        os.mkdir(path)
    dtstring = datetime.now().strftime("%d-%b-%Y-%H%M")
    with open(os.path.join(path, dtstring + ".bin"), 'wb') as inventories:
        pickle.dump(device_inventories, inventories)
    with open(os.path.join(path, "last_inventory.bin"), 'wb') as inventories:
        pickle.dump(device_inventories, inventories)
    return device_inventories, db


def get_inventories():
    print("GET A LIST OF INVENTORIES HERE")  # TODO


def compare_inventories(device_inventory_1: dict, device_inventory_2: dict) -> xl.Database:
    """
    Compare two inventories and produce an excel sheet with the results

    curl -XGET -d '{"inventory1": "04-Aug-2020-1325.bin", "inventory2": "04-Aug-2020-1325.bin"}'
    127.0.0.1:5000/api/compare_inventories -H "Content-Type: application/json"
    """

    # TODO - This can probably get removed

    path = os.path.join(os.getcwd(), "inventories")

    """
    logging.info("Reading binary database from the file \"" + str(os.path.join(path, inventory1)) + "\" from disk.")
    with open(os.path.join(path, inventory1), 'rb') as database:
        device_inventory_1 = pickle.load(database)

    logging.info("Reading binary database from the file \"" + str(os.path.join(path, inventory2)) + "\" from disk.")
    with open(os.path.join(path, inventory2), 'rb') as database:
        device_inventory_2 = pickle.load(database)
    """

    db = xl.Database()

    device_inventory_2["12446"]["PCI Cards"][1]["Manufacturer"] = "New Manufacturer"
    device_inventory_2["12446"]["PCI Cards"][1]["Slot Number"] = "AHCI.Slot.2-2"
    device_inventory_2["12446"]["PCI Cards"][1]["Databus Width"] = "8x or x 8"
    device_inventory_2["12446"]["PCI Cards"][2]["Manufacturer"] = "New Manufacturer"
    device_inventory_2["12446"]["PCI Cards"][2]["Slot Number"] = "AHCI.Slot.2-2"
    device_inventory_2["12446"]["PCI Cards"][2]["Databus Width"] = "8x or x 8"
    device_inventory_2["12902"]["Processors"].pop(2)
    device_inventory_2["12902"]["Power Supplies"][2] = {"ID": 984, "Location": "PSU.Slot.3", "Output Watts": 9000,
                                                        "Firmware Version": "00.3D.67",
                                                        "Model": 'PWR SPLY,1600W,RDNT,DELTA', "Serial Number": "Stuff"}
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
            warning = "Device identifier " + str(identifier) + " was found in inventory 1, but not in inventory 2. This " \
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
                    for comparison_device, comparison_device_values in device_inventory_1[identifier][subsystem]\
                            .items():
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
            warning = "Device identifier " + str(identifier) + " was found in inventory 2, but not in inventory 1. This " \
                      "corresponds to idrac IP " + inventory["idrac IP"] + ". This probably shouldn't have happened. " \
                      "The error is not fatal, but should be investigated]."
            logging.warning(warning)
            db.ws("Inventory Deltas").update_index(row=1, col=1, val=warning)  # TODO - fix

    return db.ws("Inventory Deltas")


parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('--port', dest="port", required=False, type=int, default=5000,
                    help='Specify the port you want Flask to run on')
parser.add_argument('--log-level', metavar='LOG_LEVEL', dest="log_level", required=False, type=str, default="info",
                    choices=['debug', 'info', 'warning', 'error', 'critical'],
                    help='The log level at which you want to run.')

args = parser.parse_args()

if args.log_level:
    if args.log_level == "debug":
        logging.basicConfig(level=logging.DEBUG)
    elif args.log_level == "info":
        logging.basicConfig(level=logging.INFO)
    elif args.log_level == "warning":
        logging.basicConfig(level=logging.WARNING)
    elif args.log_level == "error":
        logging.basicConfig(level=logging.ERROR)
    elif args.log_level == "critical":
        logging.basicConfig(level=logging.CRITICAL)
else:
    logging.basicConfig(level=logging.INFO)

