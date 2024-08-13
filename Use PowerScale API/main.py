import requests
from requests.auth import HTTPBasicAuth

# Configuration
base_url = 'https://10.10.25.80:8080'
username = 'admin'
password = 'password'
session_url = f'{base_url}/session/1/session'
health_check_url = f'{base_url}/platform/1/cluster/health'

# Disable warnings about unverified HTTPS requests
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

def authenticate():
    """Authenticate to OneFS and return session cookies."""
    payload = {
        "username": username,
        "password": password,
        "services": ["platform"]
    }
    response = requests.post(session_url, json=payload, verify=False)
    if response.status_code == 201:
        print("Authentication successful.")
        session_cookies = response.cookies
        csrf_token = response.cookies.get('isicsrf')
        return session_cookies, csrf_token
    else:
        print(f"Authentication failed: {response.text}")
        return None, None

def health_check(session_cookies, csrf_token):
    """Perform a health check using the authenticated session."""
    headers = {
        'Referer': base_url,
        'X-CSRF-Token': csrf_token
    }
    response = requests.get(health_check_url, cookies=session_cookies, headers=headers, verify=False)
    if response.status_code == 200:
        print("Health check successful. Cluster is healthy.")
        print("Health check details:", response.json())
    else:
        print(f"Health check failed: {response.status_code}, {response.text}")

def main():
    session_cookies, csrf_token = authenticate()
    if session_cookies and csrf_token:
        health_check(session_cookies, csrf_token)

if __name__ == "__main__":
    main()
