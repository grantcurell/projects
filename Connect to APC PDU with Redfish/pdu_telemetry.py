import requests
import urllib3
from tabulate import tabulate
from datetime import datetime

# === Configuration ===
PDU_HOST = "<YOUR_IP>"
PDU_PORT = 443
USERNAME = "admin"
PASSWORD = "<YOUR_PASSWORD>"
VERIFY_SSL = False

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

BASE_URL = f"https://{PDU_HOST}:{PDU_PORT}/redfish/v1/PowerEquipment/RackPDUs/1"
HEADERS = {"Content-Type": "application/json"}

def get_json(path):
    url = f"{BASE_URL}{path}"
    r = requests.get(url, headers=HEADERS, verify=VERIFY_SSL, auth=(USERNAME, PASSWORD))
    r.raise_for_status()
    return r.json()

def print_header(title):
    print(f"\n### {title} ###\n")

def print_table(title, data, headers):
    print_header(title)
    print(tabulate(data, headers=headers, tablefmt="fancy_grid"))

def print_metrics():
    metrics = get_json("/Metrics")
    power = metrics.get("PowerWatts", {})
    energy = metrics.get("EnergykWh", {}).get("Reading", "N/A")
    table = [[
        power.get("Reading", "N/A"),
        power.get("ApparentVA", "N/A"),
        power.get("ReactiveVAR", "N/A"),
        power.get("PowerFactor", "N/A"),
        energy
    ]]
    headers = ["Power (W)", "Apparent (VA)", "Reactive (VAR)", "Power Factor", "Energy (kWh)"]
    print_table("PDU Summary Metrics", table, headers)

def print_outlet_summary(outlet_index):
    path = f"/Outlets/OUTLET{outlet_index}"
    try:
        outlet = get_json(path)
    except Exception as e:
        print(f"[ERROR] Could not get outlet {outlet_index}: {e}")
        return
    data = [[
        outlet.get("Id", "N/A"),
        outlet.get("Name", "N/A"),
        outlet["Status"].get("Health", "N/A"),
        outlet["Status"].get("State", "N/A"),
        outlet.get("PowerState", "N/A"),
        outlet.get("PowerEnabled", "N/A"),
        outlet.get("RatedCurrentAmps", "N/A"),
        outlet.get("NominalVoltage", "N/A"),
        outlet.get("Voltage", {}).get("Reading", "N/A"),
        outlet.get("CurrentAmps", {}).get("Reading", "N/A"),
        outlet.get("PowerWatts", {}).get("Reading", "N/A"),
        outlet.get("EnergykWh", {}).get("Reading", "N/A")
    ]]
    headers = [
        "ID", "Name", "Health", "State", "Power", "Enabled",
        "Rated Amps", "Nominal V", "V (Actual)", "Amps", "Watts", "kWh"
    ]
    print_table(f"Outlet {outlet_index} Status", data, headers)

def main():
    print_header(f"PDU Telemetry Report - {datetime.now().isoformat()}")
    print_metrics()

    for i in range(1, 5):  # Just the first 4 outlets for demo
        print_outlet_summary(i)

if __name__ == "__main__":
    main()
