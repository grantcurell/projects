import requests
import urllib3
import json
import time
from datetime import datetime

# === CONFIGURATION ===
PDU_IP = "<YOUR_IP>"
PDU_PORT = 443
USERNAME = "admin"
PASSWORD = "<YOUR_PASS>"
VERIFY_SSL = False
MAX_DEPTH = 10
MARKDOWN_FILE = f"redfish_discovery_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"

BASE_URL = f"https://{PDU_IP}:{PDU_PORT}/redfish/v1/"
visited = set()
endpoints = {}

# === DISABLE SSL WARNINGS ===
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# === SESSION SETUP ===
session = requests.Session()
session.auth = (USERNAME, PASSWORD)
session.headers.update({"Content-Type": "application/json"})

# === HELPER FUNCTIONS ===
def fetch_json(url):
    try:
        print(f"[INFO] Fetching: {url}")
        response = session.get(url, verify=VERIFY_SSL, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return {"error": str(e)}

def crawl(url, depth=0):
    if url in visited or depth > MAX_DEPTH:
        return
    visited.add(url)

    data = fetch_json(url)
    if "error" in data:
        endpoints[url] = {"error": data["error"]}
        return

    endpoints[url] = {}
    for key, value in data.items():
        if isinstance(value, dict) and "@odata.id" in value:
            child_url = value["@odata.id"]
            full_url = f"https://{PDU_IP}:{PDU_PORT}{child_url}"
            print(f"[DISCOVERED] {key}: {child_url}")
            endpoints[url][key] = child_url
            crawl(full_url, depth + 1)
        elif isinstance(value, list):
            linked = []
            for item in value:
                if isinstance(item, dict) and "@odata.id" in item:
                    child_url = item["@odata.id"]
                    full_url = f"https://{PDU_IP}:{PDU_PORT}{child_url}"
                    print(f"[DISCOVERED] {key}[]: {child_url}")
                    linked.append(child_url)
                    crawl(full_url, depth + 1)
            if linked:
                endpoints[url][key] = linked

def write_markdown(endpoints):
    with open(MARKDOWN_FILE, "w") as f:
        f.write(f"# Redfish Endpoint Discovery Report\n")
        f.write(f"Generated: {datetime.now().isoformat()}\n\n")
        for url, content in sorted(endpoints.items()):
            f.write(f"## `{url}`\n\n")
            if "error" in content:
                f.write(f"**Error**: `{content['error']}`\n\n")
            else:
                for key, val in content.items():
                    if isinstance(val, list):
                        f.write(f"**{key}**:\n")
                        for item in val:
                            f.write(f"- `{item}`\n")
                        f.write("\n")
                    else:
                        f.write(f"**{key}**: `{val}`\n\n")
        f.write("\n---\n")
    print(f"\n[INFO] Markdown report saved to `{MARKDOWN_FILE}`")

# === EXECUTE CRAWL ===
print(f"[START] Crawling Redfish API at {BASE_URL}")
crawl(BASE_URL)

# === OUTPUT RESULTS TO TERMINAL ===
print("\n=== Discovered Redfish API Endpoints ===\n")
for url, content in sorted(endpoints.items()):
    print(f"Endpoint: {url}")
    if "error" in content:
        print(f"  ERROR: {content['error']}")
    else:
        for key, val in content.items():
            if isinstance(val, list):
                print(f"  {key}:")
                for item in val:
                    print(f"    - {item}")
            else:
                print(f"  {key}: {val}")
    print()

# === OUTPUT MARKDOWN FILE ===
write_markdown(endpoints)
