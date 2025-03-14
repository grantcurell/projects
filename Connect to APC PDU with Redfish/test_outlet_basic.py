import requests
import base64
import json
import urllib3
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# CONFIG
PDU_IP = "10.15.1.50"
OUTLET_NUMBER = 1
USERNAME = "admin"
PASSWORD = "HPC1234!@#$"
VERIFY_SSL = False

SESSION_URL = f"https://{PDU_IP}/redfish/v1/SessionService/Sessions"
CONTROL_URL = f"https://{PDU_IP}/redfish/v1/PowerEquipment/RackPDUs/1/Outlets/OUTLET{OUTLET_NUMBER}/Outlet.PowerControl"

print(f"[INFO] Target PDU: {PDU_IP}")
print(f"[INFO] Target Outlet: {OUTLET_NUMBER}")
print(f"[INFO] Redfish Session URL: {SESSION_URL}")
print(f"[INFO] Outlet Control URL: {CONTROL_URL}")
print("")

# Encode Basic Auth
auth_str = f"{USERNAME}:{PASSWORD}"
auth_b64 = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
print(f"[DEBUG] Basic Auth (base64): {auth_b64}")

auth_header = {
    "Authorization": f"Basic {auth_b64}",
    "Content-Type": "application/json"
}

auth_body = json.dumps({
    "username": USERNAME,
    "password": PASSWORD
})
print(f"[DEBUG] Auth JSON Body:\n{auth_body}\n")

# Start session
print("[INFO] Sending session authentication request...")
session = requests.Session()
login = session.post(SESSION_URL, headers=auth_header, data=auth_body, verify=VERIFY_SSL)

print(f"[DEBUG] Login Response Code: {login.status_code}")
print(f"[DEBUG] Login Response Headers:\n{login.headers}")
print(f"[DEBUG] Login Response Body:\n{login.text}\n")

if login.status_code != 201:
    print(f"[ERROR] Auth failed: {login.status_code}")
    exit(1)

token = login.headers.get("X-Auth-Token")
if not token:
    print("[ERROR] No X-Auth-Token received!")
    exit(2)

print(f"[INFO] X-Auth-Token acquired: {token}\n")

session_headers = {
    "X-Auth-Token": token,
    "Content-Type": "application/json"
}

def set_outlet(state):
    payload = {
        "OutletNumber": OUTLET_NUMBER,
        "StartupState": "off",
        "Outletname": f"PDU1OUTLET{OUTLET_NUMBER}",
        "OnDelay": 0,
        "OffDelay": 0,
        "RebootDelay": 5,
        "OutletStatus": state
    }

    print(f"[INFO] Sending outlet control request to set state: {state.upper()}")
    print(f"[DEBUG] Request Headers:\n{session_headers}")
    print(f"[DEBUG] Request Payload:\n{json.dumps(payload, indent=2)}\n")

    response = session.post(CONTROL_URL, headers=session_headers, json=payload, verify=VERIFY_SSL)

    print(f"[{state.upper()}] Response Code: {response.status_code}")
    print(f"[{state.upper()}] Response Headers:\n{response.headers}")
    print(f"[{state.upper()}] Response Body:\n{response.text}\n")

# Control sequence
set_outlet("on")
time.sleep(5)
set_outlet("off")

# Cleanup
print("[INFO] Closing session")
session.close()
