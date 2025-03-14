import time
import requests
import base64
import json
import urllib3
import logging
import argparse
import sys
from collections import Counter
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# === CLI ARGS ===
parser = argparse.ArgumentParser(
    description="Stress-test APC Redfish outlet control",
    formatter_class=argparse.RawTextHelpFormatter
)

parser.add_argument('--pdu-ip', required=False, help="IP address of the PDU")
parser.add_argument('--username', required=False, help="Username for Redfish login")
parser.add_argument('--password', required=False, help="Password for Redfish login")
parser.add_argument('--port', type=int, default=443, help="Redfish HTTPS port (default: 443)")
parser.add_argument('--outlet', type=int, default=1, help="Outlet number to control")
parser.add_argument('--duration', type=int, default=60, help="Test duration in seconds (default: 60)")
parser.add_argument('--interval', type=int, default=2, help="Interval between toggles in seconds (default: 2)")
parser.add_argument('--verify', action='store_true', help="Enable SSL certificate verification (default: off)")
parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose logging")

args = parser.parse_args()

# === If no required args given, show help and examples ===
if not (args.pdu_ip and args.username and args.password):
    parser.print_help()
    print("\nExamples:")
    print("  python stress_test.py --pdu-ip 10.15.1.50 --username admin --password pass123")
    print("  python stress_test.py --pdu-ip 192.168.1.100 --username root --password secret --outlet 2")
    print("  python stress_test.py --pdu-ip 10.0.0.50 --username test --password 1234 --duration 120 --interval 5 -v")
    print("  python stress_test.py --pdu-ip 10.0.0.50 --username test --password 1234 --verify")
    sys.exit(1)

# === CONFIG FROM ARGS ===
PDU_IP = args.pdu_ip
USERNAME = args.username
PASSWORD = args.password
PDU_PORT = args.port
OUTLET_NUMBER = args.outlet
DURATION_SECONDS = args.duration
INTERVAL_SECONDS = args.interval
VERIFY_SSL = args.verify

LOG_FILE = f"pdu_stress_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

# === LOGGING SETUP ===
logger = logging.getLogger("pdu_stress_test")
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG if args.verbose else logging.INFO)

formatter = logging.Formatter('[%(levelname)s] %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

if not VERIFY_SSL:
    logger.warning("SSL verification is disabled (default behavior).")

# === URLS & AUTH ===
SESSION_URL = f"https://{PDU_IP}:{PDU_PORT}/redfish/v1/SessionService/Sessions"
CONTROL_URL = f"https://{PDU_IP}:{PDU_PORT}/redfish/v1/PowerEquipment/RackPDUs/1/Outlets/OUTLET{OUTLET_NUMBER}/Outlet.PowerControl"

auth_str = f"{USERNAME}:{PASSWORD}"
auth_b64 = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")
auth_header = {
    "Authorization": f"Basic {auth_b64}",
    "Content-Type": "application/json"
}
auth_body = json.dumps({"username": USERNAME, "password": PASSWORD})

logger.info(f"Target PDU: {PDU_IP}")
logger.info(f"Outlet Number: {OUTLET_NUMBER}")
logger.debug(f"Redfish Session URL: {SESSION_URL}")
logger.debug(f"Outlet Control URL: {CONTROL_URL}")
logger.debug(f"Basic Auth (base64): {auth_b64}")
logger.debug(f"Auth JSON Body: {auth_body}")

# === STATS ===
stats = {
    "total_requests": 0,
    "success": 0,
    "fail": 0,
    "errors": Counter()
}

def attempt_auth(session):
    try:
        logger.info("Attempting Redfish session authentication...")
        login = session.post(SESSION_URL, headers=auth_header, data=auth_body, verify=VERIFY_SSL)
        logger.debug(f"Auth Response Code: {login.status_code}")
        logger.debug(f"Auth Response Headers:\n{dict(login.headers)}")
        logger.debug(f"Auth Response Body:\n{login.text}")

        if login.status_code != 201:
            raise Exception(f"Auth failed with code {login.status_code}")
        token = login.headers.get("X-Auth-Token")
        if not token:
            raise Exception("No X-Auth-Token received")
        return {
            "X-Auth-Token": token,
            "Content-Type": "application/json"
        }
    except Exception as e:
        stats["fail"] += 1
        stats["errors"][f"Auth Error: {str(e)}"] += 1
        logger.error(f"[AUTH ERROR] {e}")
        return None

def send_toggle(session, headers, state):
    payload = {
        "OutletNumber": OUTLET_NUMBER,
        "StartupState": "off",
        "Outletname": f"PDU1OUTLET{OUTLET_NUMBER}",
        "OnDelay": 0,
        "OffDelay": 0,
        "RebootDelay": 5,
        "OutletStatus": state
    }

    logger.info(f"Sending outlet control request to set state: {state.upper()}")
    logger.debug(f"Request Headers:\n{headers}")
    logger.debug(f"Request Payload:\n{json.dumps(payload, indent=2)}")

    stats["total_requests"] += 1

    try:
        response = session.post(CONTROL_URL, headers=headers, json=payload, verify=VERIFY_SSL)
        logger.debug(f"Response Code: {response.status_code}")
        logger.debug(f"Response Headers:\n{dict(response.headers)}")
        logger.debug(f"Response Body:\n{response.text}")

        if response.status_code in [200, 202, 204]:
            stats["success"] += 1
        else:
            stats["fail"] += 1
            stats["errors"][f"{response.status_code}: {response.text.strip()}"] += 1
            logger.error(f"Failed response: {response.status_code} {response.text.strip()}")
    except Exception as e:
        stats["fail"] += 1
        stats["errors"][str(e)] += 1
        logger.error(f"[TOGGLE ERROR] {e}")

# === MAIN LOOP ===
session = requests.Session()
headers = None
state = "on"
start_time = time.time()

while time.time() - start_time < DURATION_SECONDS:
    if not headers:
        headers = attempt_auth(session)
    if headers:
        send_toggle(session, headers, state)
        state = "off" if state == "on" else "on"
    else:
        logger.warning("Skipping toggle due to failed auth.")
    time.sleep(INTERVAL_SECONDS)

logger.info("Test complete. Closing session.")
session.close()

# === SUMMARY ===
logger.info("=" * 60)
logger.info("SUMMARY")
logger.info(f"Total Requests Sent : {stats['total_requests']}")
logger.info(f"Successful Responses: {stats['success']}")
logger.info(f"Failed Responses    : {stats['fail']}")
logger.info("\nError Summary:")
for err, count in stats["errors"].items():
    logger.info(f"- {count}x {err}")
logger.info("=" * 60)
logger.info(f"Log written to {LOG_FILE}")
