import requests
import yaml
import time
import logging
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings for self-signed Redfish endpoints
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

METRICS_FILE = "metrics.prom"

def load_devices():
    try:
        with open("devices.yaml") as f:
            devices = yaml.safe_load(f)["devices"]
            logging.info(f"Loaded {len(devices)} devices from devices.yaml")
            return devices
    except Exception as e:
        logging.error(f"Failed to load devices.yaml: {e}")
        return []

def fetch_metrics(device):
    try:
        url = f"https://{device['ip']}/redfish/v1/Chassis/System.Embedded.1/Thermal"
        logging.info(f"Polling {device['name']} at {device['ip']}")

        resp = requests.get(url, auth=(device["username"], device["password"]), verify=False, timeout=5)
        data = resp.json()

        metrics = []
        for sensor in data.get("Temperatures", []):
            name = sensor.get("Name", "unknown").replace(" ", "_")
            temp = sensor.get("ReadingCelsius")
            if temp is not None:
                metrics.append(
                    f'redfish_temperature_celsius{{device="{device["name"]}",sensor="{name}"}} {temp}'
                )

        logging.info(f"Collected {len(metrics)} temperature metrics from {device['name']}")
        return "\n".join(metrics)

    except Exception as e:
        logging.error(f"Error fetching metrics from {device['name']} ({device['ip']}): {e}")
        return f'# error fetching from {device["name"]}: {e}'

def main_loop():
    while True:
        devices = load_devices()
        if not devices:
            logging.warning("No devices loaded. Skipping this cycle.")
            time.sleep(15)
            continue

        all_metrics = []
        for device in devices:
            result = fetch_metrics(device)
            all_metrics.append(result)

        metrics_blob = "\n".join(all_metrics)

        try:
            with open(METRICS_FILE, "w") as f:
                f.write(metrics_blob)
            logging.info(f"Wrote metrics to {METRICS_FILE}")
        except Exception as e:
            logging.error(f"Failed to write metrics file: {e}")

        time.sleep(15)

if __name__ == "__main__":
    main_loop()
