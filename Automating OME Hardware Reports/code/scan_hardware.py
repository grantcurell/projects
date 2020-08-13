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
import sys
from datetime import datetime
import os
import pickle
from lib.discover_device import discover_device, get_job_id, track_job_to_completion
from lib.ome import get_device_ids_by_idrac_ip, get_device_list
from lib.create_static_group import create_static_group
from lib.power_cycle_servers import power_control_servers
import lib.ome
from urllib3 import disable_warnings
import pylightxl as xl
import json
import logging
import time
import requests
import subprocess
import socket

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


def discover(target_ips: list, ome_ip: str, ome_username: str, ome_password: str, discover_username: str,
             discover_password: str, device_type: str = "server") -> dict:
    """
    Discovers a list of devices based on input

    Example curl:

    curl -XPUT -d '{"target_ips": "192.168.1.10", "ome_ip_address": "192.168.1.18", "user_name": "admin",
    "password": "password", "discover_user_name": "root", "discover_password": "password",
    "device_type": "server"}' 127.0.0.1:5000/api/discover -H "Content-Type: application/json"
    """

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
        return None

    logging.info("Getting list of IDs by idrac IP")
    device_ids_by_idrac = get_device_ids_by_idrac_ip(ome_ip, ome_username, ome_password)

    device_list = get_device_list(ome_ip, headers)

    # Create id - service tag index to avoid O(n) lookups on each search
    # This is relevant when operating on hundreds of devices
    id_service_tag_dict = {}
    for device in device_list:
        id_service_tag_dict[str(device["Id"])] = device["DeviceServiceTag"]

    servers["id_list"] = []
    servers["id_to_ip"] = {}

    for ip_address in target_ips:
        server_id = str(device_ids_by_idrac[ip_address])
        if server_id != "":
            servers[ip_address] = server_id
            servers[server_id] = id_service_tag_dict[server_id]
            servers["id_list"].append(server_id)
            servers["id_to_ip"][server_id] = ip_address
        else:
            logging.warning("Error: couldn't resolve the name " + str(ip_address) + " to a device ID. This might mean "
                            "there was a login failure during discovery. Check the OME discovery logs for details.")
            return None

    auth_success, headers = lib.ome.authenticate_with_ome(ome_ip, ome_username, ome_password)
    discovery_path = os.path.join(os.getcwd(), "discovery_scans")
    if not os.path.exists(discovery_path):
        os.mkdir(discovery_path)
    dtstring = datetime.now().strftime("%d-%b-%Y-%H%M")
    servers["GROUP_NAME"] = dtstring
    with open(os.path.join(discovery_path, dtstring + ".bin"), 'wb') as database:
        pickle.dump(servers, database)
    with open(os.path.join(discovery_path, "latest_discovery.bin"), 'wb') as database:
        pickle.dump(servers, database)

    # I abused types here which I shouldn't have done, but did. groups is either a tuple with the ID of In-Progress
    # Servers and Completed Servers in a tuple or it is an error message.
    groups, status_code = _get_default_group_ids(headers, ome_ip, ome_username, ome_password)

    if status_code == 200:
        c_return_message, c_status_code = create_static_group(ome_ip, ome_username, ome_password,
                                                              servers["GROUP_NAME"], groups[0])
        logging.info(c_return_message)
        if c_status_code != 200:
            return None
    else:
        logging.error(groups)
        return None

    lib.ome.add_device_to_static_group(ome_ip, ome_username, ome_password, servers["GROUP_NAME"],
                                       device_names=target_ips)

    logging.info("Successfully discovered all servers. Check the group " + servers["GROUP_NAME"] + " for a list.")
    return servers


def hardware_health(servers_to_check: dict, ome_ip: str, ome_username: str, ome_password: str,
                    xldatabase: xl.database = None) -> tuple:
    """
    Retrieves the hardware's health

    Example curl:
    curl -XGET -d '{"target_ips": "192.168.1.10", "ome_ip_address": "192.168.1.18", "user_name": "admin",
    "password": "password"}' 127.0.0.1:5000/api/hardware_health -H "Content-Type: application/json"
    """

    auth_success, headers = lib.ome.authenticate_with_ome(ome_ip, ome_username, ome_password)
    system_health = {}

    for device_id in servers_to_check["id_list"]:

        logging.info("Getting the health for " + servers_to_check[device_id])
        url = 'https://%s/api/DeviceService/Devices(%s)/SubSystemHealth' % (ome_ip, device_id)
        response = requests.get(url, headers=headers, verify=False)
        if response.status_code != 200:
            logging.error("Failed to retrieve health. Error received " + str(json.loads(response.content)))
            return None
        else:
            content = json.loads(response.content)
            if content["@odata.count"] > 0:
                system_health[device_id] = {}
                for item in content['value']:
                    if item["@odata.type"] == "#DeviceService.SubSystemHealthFaultModel":
                        system_health[device_id]["errors"] = {}
                        if "FaultList" in item:
                            for index, error in enumerate(item["FaultList"]):
                                system_health[device_id]["errors"][index] = {}
                                if "Fqdd" in error:
                                    system_health[device_id]["errors"][index]["location"] = error["Fqdd"]
                                if "MessageId" in error:
                                    system_health[device_id]["errors"][index]["messageid"] = error["MessageId"]
                                if "Message" in error:
                                    system_health[device_id]["errors"][index]["message"] = error["Message"]
                                if "Severity" in error:
                                    system_health[device_id]["errors"][index]["severity"] = \
                                        health_mapping[error["Severity"]]
                                if "SubSystem" in error:
                                    system_health[device_id]["errors"][index]["subsystem"] = error["SubSystem"]
                                if "RecommendedAction" in error:
                                    system_health[device_id]["errors"][index]["recommended_action"] = error[
                                        "RecommendedAction"]
                        system_health[device_id]["health"] = health_mapping[item["RollupStatus"]]
                        break
            else:
                logging.error("We successfully retrieved the server health, but there were no values. "
                              "We aren't sure why this would happen.")
                return None
            logging.info("Retrieved health for " + servers_to_check[device_id])

    logging.info("Generating Excel spreadsheet for hardware health.")
    if not xldatabase:
        xldatabase = xl.Database()
    xldatabase.add_ws("Hardware Errors",
                      {'A1': {'v': "Service Tag", 'f': '', 's': ''},
                       'B1': {'v': "System idrac IP", 'f': '', 's': ''},
                       'C1': {'v': "OME System Identifier", 'f': '', 's': ''},
                       'D1': {'v': "Location", 'f': '', 's': ''},
                       'E1': {'v': "Message ID", 'f': '', 's': ''},
                       'F1': {'v': "Message", 'f': '', 's': ''},
                       'G1': {'v': "Severity", 'f': '', 's': ''},
                       'H1': {'v': "Subsystem", 'f': '', 's': ''},
                       'I1': {'v': "Recommended Action", 'f': '', 's': ''}})
    y = 2
    for device_id, health in system_health.items():
        logging.info("Processing " + device_id)
        for error in health["errors"].values():
            xldatabase.ws("Hardware Errors").update_index(row=y, col=1, val=servers_to_check[device_id])
            xldatabase.ws("Hardware Errors").update_index(row=y, col=2, val=servers_to_check["id_to_ip"][device_id])
            xldatabase.ws("Hardware Errors").update_index(row=y, col=3, val=device_id)
            if "location" in error:
                xldatabase.ws("Hardware Errors").update_index(row=y, col=4, val=error["location"])
            if "messageid" in error:
                xldatabase.ws("Hardware Errors").update_index(row=y, col=5, val=error["messageid"])
            if "message" in error:
                xldatabase.ws("Hardware Errors").update_index(row=y, col=6, val=error["message"])
            if "severity" in error:
                xldatabase.ws("Hardware Errors").update_index(row=y, col=7, val=error["severity"])
            if "subsystem" in error:
                xldatabase.ws("Hardware Errors").update_index(row=y, col=8, val=error["subsystem"])
            if "recommended_action" in error:
                xldatabase.ws("Hardware Errors").update_index(row=y, col=9, val=error["recommended_action"])
            y = y + 1

    return system_health, xldatabase


def hardware_inventory(servers_to_retrieve: dict, ome_ip: str, ome_username: str, ome_password: str,
                       default_inventory_name: str = "last_inventory.bin") -> tuple:
    """
    Retrieves the hardware inventory for a specified target

    curl -XGET -d '{"target_ips": "192.168.1.10", "ome_ip_address": "192.168.1.18", "user_name": "admin",
    "password": "password"}' 127.0.0.1:5000/api/hardware_inventory -H "Content-Type: application/json"
    """

    def _handle_keys(ome_field, ome_device, dict_field, dict_device):
        if ome_field in ome_device:
            device_inventories[device_id][dict_device][index][dict_field] = ome_device[ome_field]
        else:
            logging.warning(ome_field + " was not in OpenManage's database for device with sub ID " +
                            str(device_inventories[device_id][dict_device][index]["ID"]) + ". The device type was "
                            + dict_device + ". The host has idrac IP " + servers_to_retrieve["id_to_ip"][device_id] +
                            " and service tag " + servers_to_retrieve[device_id] +
                            ". We are skipping the field. It will not be used for comparison.")
            device_inventories[device_id][dict_device][index][dict_field] = "None"

    inventory_type = None

    auth_success, headers = lib.ome.authenticate_with_ome(ome_ip, ome_username, ome_password)

    device_inventories = {}

    inventory_types = {
        "cpus": "serverProcessors",
        "os": "serverOperatingSystems",
        "disks": "serverArrayDisks",
        "controllers": "serverRaidControllers",
        "memory": "serverMemoryDevices"}

    for device_id in servers_to_retrieve["id_list"]:

        logging.info("Processing inventory for " + device_id)

        inventory_url = "https://%s/api/DeviceService/Devices(%s)/InventoryDetails" % (ome_ip, device_id)
        if inventory_type:
            inventory_url = "https://%s/api/DeviceService/Devices(%s)/InventoryDetails(\'%s\')" \
                            % (ome_ip, str(device_id), inventory_types[inventory_type])
        inven_resp = requests.get(inventory_url, headers=headers, verify=False)
        if inven_resp.status_code == 200:
            logging.info("\n*** Inventory for device (%s) ***" % device_id)
            content = json.loads(inven_resp.content)
            if content["@odata.count"] > 0:
                device_inventories[device_id] = {"idrac IP": servers_to_retrieve["id_to_ip"][device_id]}
                for item in content['value']:
                    if item["InventoryType"] == "serverDeviceCards":
                        logging.debug("Processing PCI cards for " + device_id)
                        device_inventories[device_id]["PCI Cards"] = {}
                        index = 0
                        for card in item["InventoryInfo"]:
                            # Skip disks. Those are covered below.
                            if "Disk.Bay" in card["SlotNumber"] or "pci" not in card["SlotType"].lower():
                                continue
                            device_inventories[device_id]["PCI Cards"][index] = {}
                            _handle_keys("Id", card, "ID", "PCI Cards")
                            _handle_keys("SlotNumber", card, "Slot Number", "PCI Cards")
                            _handle_keys("Manufacturer", card, "Manufacturer", "PCI Cards")
                            _handle_keys("Description", card, "Description", "PCI Cards")
                            _handle_keys("DatabusWidth", card, "Databus Width", "PCI Cards")
                            _handle_keys("SlotLength", card, "Slot Length", "PCI Cards")
                            _handle_keys("SlotType", card, "Slot Type", "PCI Cards")
                            index = index + 1
                    elif item["InventoryType"] == "serverProcessors":
                        logging.debug("Processing processors (haha) for " + device_id)
                        device_inventories[device_id]["Processors"] = {}
                        for index, processor in enumerate(item["InventoryInfo"]):
                            device_inventories[device_id]["Processors"][index] = {}
                            _handle_keys("Id", processor, "ID", "Processors")
                            _handle_keys("Family", processor, "Family", "Processors")
                            _handle_keys("MaxSpeed", processor, "Max Speed", "Processors")
                            _handle_keys("SlotNumber", processor, "Slot Number", "Processors")
                            _handle_keys("NumberOfCores", processor, "Number of Cores", "Processors")
                            _handle_keys("BrandName", processor, "Brand Name", "Processors")
                            _handle_keys("ModelName", processor, "Model Name", "Processors")
                    elif item["InventoryType"] == "serverPowerSupplies":
                        logging.debug("Processing power supplies for " + device_id)
                        device_inventories[device_id]["Power Supplies"] = {}
                        for index, power_supply in enumerate(item["InventoryInfo"]):
                            device_inventories[device_id]["Power Supplies"][index] = {}
                            _handle_keys("Id", power_supply, "ID", "Power Supplies")
                            _handle_keys("Location", power_supply, "Location", "Power Supplies")
                            _handle_keys("OutputWatts", power_supply, "Output Watts", "Power Supplies")
                            _handle_keys("FirmwareVersion", power_supply, "Firmware Version", "Power Supplies")
                            _handle_keys("Model", power_supply, "Model", "Power Supplies")
                            _handle_keys("SerialNumber", power_supply, "Serial Number", "Power Supplies")
                    elif item["InventoryType"] == "serverArrayDisks":
                        logging.debug("Processing disks for " + device_id)
                        device_inventories[device_id]["Disks"] = {}
                        for index, disk in enumerate(item["InventoryInfo"]):
                            device_inventories[device_id]["Disks"][index] = {}
                            _handle_keys("Id", disk, "ID", "Disks")
                            _handle_keys("SerialNumber", disk, "Serial Number", "Disks")
                            _handle_keys("ModelNumber", disk, "Model Number", "Disks")
                            _handle_keys("EnclosureId", disk, "Enclosure ID", "Disks")
                            _handle_keys("Size", disk, "Size", "Disks")
                            _handle_keys("BusType", disk, "Bus Type", "Disks")
                            _handle_keys("MediaType", disk, "Media Type", "Disks")
                    elif item["InventoryType"] == "serverMemoryDevices":
                        logging.debug("Processing memory for " + device_id)
                        device_inventories[device_id]["Memory"] = {}
                        for index, memory in enumerate(item["InventoryInfo"]):
                            device_inventories[device_id]["Memory"][index] = {}
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
                        logging.debug("Processing RAID controllers for " + device_id)
                        device_inventories[device_id]["RAID Controllers"] = {}
                        for index, raid_controller in enumerate(item["InventoryInfo"]):
                            device_inventories[device_id]["RAID Controllers"][index] = {}
                            _handle_keys("Id", raid_controller, "ID", "RAID Controllers")
                            _handle_keys("Name", raid_controller, "Name", "RAID Controllers")
                            _handle_keys("DeviceDescription", raid_controller, "Device Description",
                                         "RAID Controllers")
                            _handle_keys("FirmwareVersion", raid_controller, "Firmware Version", "RAID Controllers")
                            _handle_keys("PciSlot", raid_controller, "PCI Slot", "RAID Controllers")

                    logging.debug("Finished device loop.")

            elif inven_resp.status_code == 400:
                logging.warning("Inventory type %s not applicable for device with ID %s" % (inventory_type,
                                                                                            str(device_id)))
                return None
            else:
                logging.error("Unable to retrieve inventory for device %s due to status code %s"
                              % (str(device_id), inven_resp.status_code))
                return None

    logging.info("Writing pickle database for inventory.")
    db = xl.Database()
    for device_id, inventory in device_inventories.items():
        logging.info("Processing " + str(device_id))
        sheet_name = servers_to_retrieve[device_id] + " - Inventory"
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

    inventory_path = os.path.join(os.getcwd(), "inventories")
    if not os.path.exists(inventory_path):
        os.mkdir(inventory_path)
    dtstring = datetime.now().strftime("%d-%b-%Y-%H%M")
    xl.writexl(db, dtstring + ".xlsx")
    os.replace(dtstring + ".xlsx", os.path.join(inventory_path, dtstring + ".xlsx"))
    if not os.path.exists(inventory_path):
        os.mkdir(inventory_path)
    dtstring = datetime.now().strftime("%d-%b-%Y-%H%M")
    with open(os.path.join(inventory_path, dtstring + ".bin"), 'wb') as inventories_to_write:
        pickle.dump(device_inventories, inventories_to_write)
    with open(os.path.join(inventory_path, default_inventory_name), 'wb') as inventories_to_write:
        pickle.dump(device_inventories, inventories_to_write)
    return device_inventories, db


def compare_inventories(device_inventory_1: dict, device_inventory_2: dict,
                        xldatabase: xl.database = None) -> xl.Database:
    """
    Compare two inventories and produce an excel sheet with the results

    curl -XGET -d '{"inventory1": "04-Aug-2020-1325.bin", "inventory2": "04-Aug-2020-1325.bin"}'
    127.0.0.1:5000/api/compare_inventories -H "Content-Type: application/json"
    """

    if not xldatabase:
        xldatabase = xl.Database()

    """
    device_inventory_2["13128"]["PCI Cards"][1]["Manufacturer"] = "New Manufacturer"
    device_inventory_2["13128"]["PCI Cards"][1]["Slot Number"] = "AHCI.Slot.2-2"
    device_inventory_2["13128"]["PCI Cards"][1]["Databus Width"] = "8x or x 8"
    device_inventory_2["13128"]["PCI Cards"][2]["Manufacturer"] = "New Manufacturer"
    device_inventory_2["13128"]["PCI Cards"][2]["Slot Number"] = "AHCI.Slot.2-2"
    device_inventory_2["13128"]["PCI Cards"][2]["Databus Width"] = "8x or x 8"
    device_inventory_2["13136"]["Processors"].pop(2)
    device_inventory_2["13136"]["Power Supplies"][2] = {"ID": 984, "Location": "PSU.Slot.3", "Output Watts": 9000,
                                                        "Firmware Version": "00.3D.67",
                                                        "Model": 'PWR SPLY,1600W,RDNT,DELTA', "Serial Number": "Stuff"}
    """
    device_inventory_2["13136"]["Power Supplies"][2] = {"ID": 984, "Location": "PSU.Slot.3", "Output Watts": 9000,
                                                        "Firmware Version": "00.3D.67",
                                                        "Model": 'PWR SPLY,1600W,RDNT,DELTA', "Serial Number": "Stuff"}
    device_inventory_2["13136"]["Memory"][24] = {"ID": 8556, "Name": "DIMM.Socket.Q1", "Size": 8192, "Manufacturer":
                                                "Hynix Semiconductor", "Part Number": "HMA81GR7CJR8N-VK", "Serial Number":
                                                "GRANT", "Speed": 2666, "Current Operating Speed": 2666,
                                                "Device Description": "DIMM Q1"}

    xldatabase.add_ws("Inventory Deltas",
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

        logging.info("Comparing inventory for device which had service tag " + servers[identifier])

        if identifier in device_inventory_2:
            for subsystem, items in inventory.items():
                if subsystem == "idrac IP":
                    continue

                logging.debug("Processing " + subsystem)
                for device, values in items.items():
                    device_found = False
                    slot_found = False
                    for comparison_device, comparison_device_values in \
                            device_inventory_2[identifier][subsystem].items():
                        try:
                            if subsystem == "PCI Cards" or subsystem == "Processors":
                                if device_inventory_2[identifier][subsystem][comparison_device]["Slot Number"] ==\
                                        values["Slot Number"]:
                                    slot_found = True
                            elif subsystem == "Power Supplies":
                                if device_inventory_2[identifier][subsystem][comparison_device]["Location"] ==\
                                        values["Location"]:
                                    slot_found = True
                            elif subsystem == "RAID Controllers":
                                if device_inventory_2[identifier][subsystem][comparison_device]["PCI Slot"] ==\
                                        values["PCI Slot"]:
                                    # This is to account for SATA controllers
                                    if values["PCI Slot"] == "Not Applicable":
                                        if device_inventory_2[identifier][subsystem][comparison_device]\
                                                             ["Device Description"] == values["Device Description"]:
                                            slot_found = True
                                    else:
                                        slot_found = True
                            elif subsystem == "Memory":
                                if device_inventory_2[identifier][subsystem][comparison_device]["Device Description"]\
                                        == values["Device Description"]:
                                    slot_found = True
                            elif subsystem == "Disks":
                                if device_inventory_2[identifier][subsystem][comparison_device]["Serial Number"] ==\
                                        values["Serial Number"]:
                                    slot_found = True
                            if slot_found:
                                logging.debug("Found match with device " + str(values["ID"]) +
                                              ". Processing comparison.")
                                device_inventory_2[identifier][subsystem][comparison_device]["FOUND"] = True
                                changed_string = ""
                                original_string = ""
                                updated_string = ""
                                change_made = False
                                for key, value in values.items():
                                    if device_inventory_2[identifier][subsystem][comparison_device][key] != value and\
                                            key != "ID":
                                        change_made = True
                                        logging.info("Difference found in subsystem " + str(subsystem) + " on device " +
                                                     str(comparison_device) + " in key " + str(key))
                                        changed_string = changed_string + key + ": " + str(value) + " --> CHANGED TO --> " \
                                                         + str(device_inventory_2[identifier][subsystem][comparison_device][key]) \
                                                         + "\n"
                                    original_string = original_string + key + ": " + str(value) + "\n"
                                    updated_string = updated_string + key + ": " + \
                                                     str(device_inventory_2[identifier][subsystem][comparison_device][key]) \
                                                     + "\n"

                                if change_made:
                                    y = y + 1
                                    xldatabase.ws("Inventory Deltas").update_index(row=y, col=1,
                                                                                   val=servers[identifier])
                                    xldatabase.ws("Inventory Deltas").update_index(row=y, col=2,
                                                                                   val=device_inventory_2[identifier][
                                                                                       "idrac IP"])
                                    xldatabase.ws("Inventory Deltas").update_index(row=y, col=3, val=identifier)
                                    xldatabase.ws("Inventory Deltas").update_index(row=y, col=4, val=subsystem)
                                    xldatabase.ws("Inventory Deltas").update_index(row=y, col=5, val="Component Updated")
                                    xldatabase.ws("Inventory Deltas").update_index(row=y, col=6, val=original_string)
                                    xldatabase.ws("Inventory Deltas").update_index(row=y, col=7, val=updated_string)
                                    xldatabase.ws("Inventory Deltas").update_index(row=y, col=8, val=changed_string)

                                break
                        except KeyError as e:
                            logging.warning("A device was missing a value critical to performing a comparison. The"
                                            " error caught was " + e + ". We are skipping this device")
                            xldatabase.ws("Inventory Deltas").update_index(row=y, col=1,
                                                                           val=servers[identifier])
                            xldatabase.ws("Inventory Deltas").update_index(row=y, col=2,
                                                                           val=device_inventory_2[identifier][
                                                                               "idrac IP"])
                            xldatabase.ws("Inventory Deltas").update_index(row=y, col=3, val=identifier)
                            xldatabase.ws("Inventory Deltas").update_index(row=y, col=4, val=subsystem)
                            xldatabase.ws("Inventory Deltas").update_index(row=y, col=5, val="Threw an error during "
                                                                                             "comparison. Check logs.")

                    if not slot_found:
                        y = y + 1
                        logging.info("A device was removed from subsystem " + str(subsystem) + " on device " + str(
                            servers[identifier]))
                        xldatabase.ws("Inventory Deltas").update_index(row=y, col=1, val=servers[identifier])
                        xldatabase.ws("Inventory Deltas").update_index(row=y, col=2,
                                                                       val=device_inventory_2[identifier]["idrac IP"])
                        xldatabase.ws("Inventory Deltas").update_index(row=y, col=3, val=identifier)
                        xldatabase.ws("Inventory Deltas").update_index(row=y, col=4, val=subsystem)
                        xldatabase.ws("Inventory Deltas").update_index(row=y, col=5, val="Component Removed")

                        string = ""
                        for key, value in values.items():
                            string = string + key + ": " + str(value) + "\n"

                        xldatabase.ws("Inventory Deltas").update_index(row=y, col=6, val=string)

        else:
            warning = "Device identifier " + str(identifier) + " was found in inventory 1, but not in inventory 2. " \
                      "This corresponds to idrac IP " + inventory["idrac IP"] + ". This probably shouldn't have " \
                      "happened. The error is not fatal, but should be investigated]."
            logging.warning(warning)
            y = y + 1
            xldatabase.ws("Inventory Deltas").update_index(row=y, col=1,
                                                           val=servers[identifier])
            xldatabase.ws("Inventory Deltas").update_index(row=y, col=2,
                                                           val=device_inventory_2[identifier][
                                                               "idrac IP"])
            xldatabase.ws("Inventory Deltas").update_index(row=y, col=3, val=identifier)
            xldatabase.ws("Inventory Deltas").update_index(row=y, col=4, val=warning)

    for identifier, inventory in device_inventory_2.items():
        if identifier in device_inventory_1:
            for subsystem, items in inventory.items():
                if subsystem == "idrac IP":
                    continue
                for device, values in items.items():
                    if "FOUND" not in values:
                        logging.info("A device was added to subsystem " + str(subsystem) + " on device " +
                                     str(servers[identifier]))
                        y = y + 1
                        xldatabase.ws("Inventory Deltas").update_index(row=y, col=1, val=servers[identifier])
                        xldatabase.ws("Inventory Deltas").update_index(row=y, col=2,
                                                                       val=device_inventory_2[identifier]["idrac IP"])
                        xldatabase.ws("Inventory Deltas").update_index(row=y, col=3, val=identifier)
                        xldatabase.ws("Inventory Deltas").update_index(row=y, col=4, val=subsystem)
                        xldatabase.ws("Inventory Deltas").update_index(row=y, col=5, val="Component Added")

                        string = ""
                        for key, value in values.items():
                            string = string + key + ": " + str(value) + "\n"

                        xldatabase.ws("Inventory Deltas").update_index(row=y, col=6, val=string)

        else:
            warning = "Device identifier " + str(
                identifier) + " was found in inventory 2, but not in inventory 1. This " \
                              "corresponds to idrac IP " + inventory["idrac IP"] + ". This probably shouldn't have " \
                              "happened. The error is not fatal, but should be investigated]."
            logging.warning(warning)
            y = y + 1
            xldatabase.ws("Inventory Deltas").update_index(row=y, col=1,
                                                           val=servers[identifier])
            xldatabase.ws("Inventory Deltas").update_index(row=y, col=2,
                                                           val=device_inventory_2[identifier][
                                                               "idrac IP"])
            xldatabase.ws("Inventory Deltas").update_index(row=y, col=3, val=identifier)
            xldatabase.ws("Inventory Deltas").update_index(row=y, col=4, val=warning)

    return xldatabase.ws("Inventory Deltas")


class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(1)


if __name__ == "__main__":
    parser = MyParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--discoveryscan', '-d', dest="discoveryscan", required=False, type=str,
                        help='Internal debugging command. Not for end user use. Allows you to bypass the discovery'
                             ' scan and manually input a scan to use.')
    parser.add_argument('--log-level', metavar='LOG_LEVEL', dest="log_level", required=False, type=str, default="info",
                        choices=['debug', 'info', 'warning', 'error', 'critical'],
                        help='The log level at which you want to run.')
    parser.add_argument('--start-dhcp-server', dest="dhcp", required=False, action='store_true', default=False,
                        help="Starts a DHCP server in the background that is used to assign IP addresses to the servers. "
                             "If you want to update the settings for the DHCP server browse to the file "
                             "lib/dhcpserv/dhcpgui.conf and edit it there. You can also skip this step altogether and"
                             " manually add servers by using the --servers <filename> switch. If you want to see the"
                             " hosts found by the DHCP server you can check lib/dhcpserv/hosts.csv.")
    parser.add_argument("--servers", dest="servers", required=False, default=None, type=str,
                        help="If you do not want to use the DHCP server you can instead pass a file with a list of servers."
                             " The format is one server per line. Ex:\n192.168.1.1\n192.168.1.2\n192.168.1.3")
    parser.add_argument('--scan', dest="scan", required=False, type=str, default="initial",
                        choices=['initial', 'final'],
                        help='Determines which scan you want to run. This is the core of the program. The scans have the '
                             'following behavior:\n    - Initial: Collects all of the IPs in the DHCP server\'s registry, '
                             'then it runs an OME discovery scan against all of those IPs. After it finishes the discovery '
                             'scan it collects an inventory of those machines and writes it out to disk.\n    - Final: '
                             'This is the second scan. It expects a previous inventory as an argument, will load the data'
                             ' from that inventory, and then rescan those machines. This includes rechecking the inventory'
                             ' and checking the current health of the hardware. It will produce an excel spreadsheet with'
                             ' inventories for each of the servers, a comparison of the original inventory and the current,'
                             ' and the health.')
    parser.add_argument("--inventory", dest="inventory", required=False, type=str,
                        help="Optional argument for the final scan. Allows you to specify an inventory you want to use."
                             "If not provided, it will default to \'last_inventory.bin\'")
    parser.add_argument("--omeip", "-i", required=True, type=str, help="OME Appliance IP")
    parser.add_argument("--omeuser", "-u", required=False, type=str, help="Username for OME Appliance", default="admin")
    parser.add_argument("--omepass", "-p", required=True, type=str, help="Password for OME Appliance")
    parser.add_argument("--idracuser", required=False, default="root", type=str,
                        help="This command is only used for the initial scan. It is the username for the servers' idracs.")
    parser.add_argument("--idracpass", required=False, type=str,
                        help="This command is only used for the initial scan. It is the password for the servers' idracs.")

    args = parser.parse_args()

    # The servers dictionary has all servers listed by both ID->service tag and
    discovery_scan_path = os.path.join(os.getcwd(), "discovery_scans", "latest_discovery.bin")
    if os.path.isfile(discovery_scan_path):
        with open(discovery_scan_path, 'rb') as discovery_database:
            servers = pickle.load(discovery_database)
    else:
        servers = {}

    try:
        socket.inet_aton(args.omeip)
    except socket.error:
        logging.error("The OME IP address " + str(args.omeip) + " is not a valid IP address. Exiting.")
        exit(1)

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

    if args.dhcp:
        # Change the working directory to the DHCP server's directory
        os.chdir(os.path.join(os.getcwd(), "lib", "dhcpserv"))
        os.remove("hosts.csv")
        process = subprocess.Popen(["python", "dhcp.py"], stdout=subprocess.PIPE)
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                test = output
                logging.info(output.strip().decode("utf-8"))
        rc = process.poll()

    ips = None

    if args.servers:
        if os.path.isfile(args.servers):
            with open(args.servers, 'r') as ip_file:
                ips = ip_file.readlines()

                # Strip whitespace characters
                ips[:] = map(str.strip, ips)

            for ip in ips:
                try:
                    socket.inet_aton(ip)
                except socket.error:
                    logging.error(str(ip) + " is not a valid IP address. Exiting.")
                    exit(1)
        else:
            logging.error("Could not find a file at path " + args.servers + ". Are you sure that's a valid file path?")
            exit(1)

    if args.scan == "initial":

        if not args.idracuser:
            logging.error("For the initial scan you must provide the argument --idracuser.")
            exit(1)
        elif not args.idracpass:
            logging.error("For the initial scan you must provide the argument --idracpassword.")
            exit(1)

        if ips is not None:
            logging.info("--servers argument provided. Ignoring hosts assigned by DHCP server.")
        else:
            logging.info("--servers argument not provided. Using lib/dhcpserv/hosts.csv from DHCP server.")
            path = os.path.join(os.getcwd(), "lib", "dhcpserv", "hosts.csv")
            if os.path.isfile(path):
                with open(path, 'r') as ip_file:
                    ips = ip_file.readlines()

                    # Change something with the format '00:50:56:C0:00:01;192.168.173.6;precisionworkstation;1597178186'
                    # to just an IP
                    for i, ip in enumerate(ips):
                        ips[i] = ip.split(';')[1].strip()

                for ip in ips:
                    try:
                        socket.inet_aton(ip)
                    except socket.error:
                        logging.error(str(ip) + " is not a valid IP address. Exiting.")
                        exit(1)
            else:
                logging.error("It looks like you didn't provide the --servers argument and lib/dhcpserv/hosts.csv"
                              " doesn't exist. You need to either provide the argument --servers or you need to run the"
                              " dhcp server first.")
                exit(1)

        if not args.discoveryscan:
            servers = discover(ips, args.omeip, args.omeuser, args.omepass, args.idracuser, args.idracpass)

            if not servers:
                logging.error("Discovery scan failed. Exiting.")
                exit(1)
        else:
            logging.warning("--discoveryscan provided. This is a debug command. Make sure you know what you're doing.")
            if args.discoveryscan == "latest":
                args.discoveryscan = default = os.path.join(os.getcwd(), "discovery_scans", "latest_discovery.bin")
            with open(args.discoveryscan, 'rb') as discoveryscan:
                servers = pickle.load(discoveryscan)
        hardware_inventory(servers, args.omeip, args.omeuser, args.omepass)

    elif args.scan == "final":

        path = os.path.join(os.getcwd(), "inventories")
        device_inventories_global_1 = {}
        if args.inventory:
            if os.path.exists(args.inventory):
                with open(args.inventory, 'rb') as inventories:
                    device_inventories_global_1 = pickle.load(inventories)
            elif os.path.exists(os.path.join(os.getcwd(), "inventories", args.inventory)):
                logging.warning("We didn't find the path you specified: " + args.inventory + ". We are using the path "
                                + os.path.join(os.getcwd(), "inventories", args.inventory) + " for you.")
                with open(os.path.join(os.getcwd(), "inventories", args.inventory), 'rb') as inventories:
                    device_inventories_global_1 = pickle.load(inventories)
            else:
                logging.error(args.inventory + " is not a valid path. Are you sure you typed it correctly?")
        elif not os.path.exists(path):
            logging.error("The path " + path + " does not exist. This is where the inventories should be stored. The"
                          " program cannot perform a final scan without an original inventory to compare against. You"
                          " can either provide your own inventory with \'--inventory <your_inventory>.bin\' or you can"                                               
                          " rerun the initial scan.")
            exit(1)
        else:
            with open(os.path.join(path, "last_inventory.bin"), 'rb') as inventories:
                device_inventories_global_1 = pickle.load(inventories)

        session_url = 'https://%s/api/SessionService/Sessions' % args.omeip
        jobs_url = "https://%s/api/JobService/Jobs" % args.omeip
        headers = {'content-type': 'application/json'}
        user_details = {'UserName': args.omeuser,
                        'Password': args.omepass,
                        'SessionType': 'API'}

        session_info = requests.post(session_url, verify=False,
                                     data=json.dumps(user_details),
                                     headers=headers)
        if session_info.status_code == 201:
            headers['X-Auth-Token'] = session_info.headers['X-Auth-Token']

            # TODO - update this for production
            #power_control_servers(servers["id_list"], headers, power_off_non_graceful=True)
            #power_control_servers(servers["id_list"], headers, power_on=True)
            power_control_servers(["13136"], headers, args.omeip, power_off_non_graceful=True)
            power_control_servers(["13136"], headers, args.omeip, power_on=True)

            logging.info("Sleeping for 1 minute to ensure that the servers turn on and are ready with a new status.")
            time.sleep(60)
            logging.info("Sleep completed. Continuing.")

            targets = []
            for id_to_refresh in servers["id_list"]:
                targets.append({
                    "Id": int(id_to_refresh),
                    "Data": "",
                    "TargetType": {
                        "Id": 1000,
                        "Name": "DEVICE"
                    }
                })

            payload = {
                "Id": 0,
                "JobName": "Refresh inventory for server hardware.",
                "JobDescription": "Refreshes the inventories for hardware in preparation for a final inventory scan.",
                "Schedule": "startnow",
                "State": "Enabled",
                "JobType": {
                    "Name": "Inventory_Task"
                },
                "Targets": targets
            }

            logging.info("Beginning inventory refresh. This is required to detect hardware changes.")
            create_resp = requests.post(jobs_url, headers=headers, verify=False, data=json.dumps(payload))

            job_id = None
            if create_resp.status_code == 201:
                job_id = json.loads(create_resp.content)["Id"]
            else:
                logging.error("Failed to refresh inventory. We aren't sure what went wrong.")
                exit(1)

            if job_id is None:
                logging.error("Received invalid job ID from OME. Exiting.")
                exit(1)

            logging.info("Waiting for the inventory refresh to complete. This could take a couple of minutes.")
            lib.discover_device.track_job_to_completion(args.omeip, headers, job_id)
            logging.info("Inventory refresh completed.")
        else:
            logging.error("Failed to establish a connection to OpenManage.")
            exit(1)

        device_inventories_global_2, output_excel = \
            hardware_inventory(servers, args.omeip, args.omeuser, args.omepass,
                               default_inventory_name="final_inventory.bin")
        server_health_dict, server_health_excel = hardware_health(servers, args.omeip, args.omeuser, args.omepass,
                                                                  output_excel)
        comparison_results = compare_inventories(device_inventories_global_1, device_inventories_global_2,
                                                 output_excel)

        output_path = os.path.join(os.getcwd(), "output")
        if not os.path.exists(output_path):
            os.mkdir(output_path)

        dtstring_global = datetime.now().strftime("%d-%b-%Y-%H%M")
        xl.writexl(output_excel, dtstring_global + ".xlsx")
        os.replace(dtstring_global + ".xlsx", os.path.join(output_path, dtstring_global + ".xlsx"))
        logging.info("Finished creating excel sheet. See " + os.path.join(output_path, dtstring_global + ".xlsx"))
