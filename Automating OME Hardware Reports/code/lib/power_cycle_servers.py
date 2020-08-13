

import logging
import requests
import json
from lib.discover_device import track_job_to_completion


def power_control_servers(server_ids, headers, ome_ip, power_on=False, power_cycle=False, power_off_non_graceful=False,
                          master_bus_reset=False, power_off_graceful=False):
    
    power_state_mapping = {
        "Power On": "2",
        "Power Cycle": "5",
        "Power Off Non-Graceful": "8",
        "Master Bus Reset": "10",  # Performs hardware reset on the system.
        "Power Off Graceful": "12"
    }

    jobs_url = "https://%s/api/JobService/Jobs" % ome_ip

    if not power_on and not power_cycle and not power_off_non_graceful and not master_bus_reset \
            and not power_off_graceful:
        logging.error("You must pass a desired power setting.")
        exit(1)

    targets = []
    for id_to_refresh in server_ids:
        targets.append({
            "Id": int(id_to_refresh),
            "Data": "",
            "TargetType": {
                "Id": 1000,
                "Name": "DEVICE"
            }
        })

    if power_on:
        power_state = power_state_mapping["Power On"]
        logging.info("Powering on servers...")
    elif power_cycle:
        power_state = power_state_mapping["Power Cycle"]
        logging.info("Power cycling servers...")
    elif power_off_non_graceful:
        power_state = power_state_mapping["Power Off Non-Graceful"]
        logging.info("Non-gracefully shutting down servers...")
    elif master_bus_reset:
        power_state = power_state_mapping["Master Bus Reset"]
        logging.info("Performing a master bus reset on the servers...")
    elif power_off_graceful:
        power_state = power_state_mapping["Power Off Graceful"]
        logging.info("Performing a graceful shutdown on the servers...")

    payload = {
        "Id": 0,
        "JobName": "Power operation",
        "JobDescription": "Performing a power operation",
        "State": "Enabled",
        "Schedule": "startnow",
        "JobType": {
            "Name": "DeviceAction_Task"
        },
        "Targets": targets,
        "Params": [{
            "Key": "override",
            "Value": "true"
        }, {
            "Key": "powerState",
            "Value": power_state
        }, {
            "Key": "operationName",
            "Value": "POWER_CONTROL"
        }, {
            "Key": "deviceTypes",
            "Value": "1000"
        }]}

    create_resp = requests.post(jobs_url, headers=headers, verify=False, data=json.dumps(payload))

    job_id = None
    if create_resp.status_code == 201:
        job_id = json.loads(create_resp.content)["Id"]
    else:
        logging.error("Power operation failed. Error was " + str(json.loads(create_resp.content)))

    if job_id is None:
        logging.error("Received invalid job ID from OME. Exiting.")
        exit(1)

    logging.info("Waiting for the power operation to complete.")
    track_job_to_completion(ome_ip, headers, job_id, sleep_interval=15)
    logging.info("Power operation completed.")
