from pprint import pprint
import requests
import base64
import json

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def print_response(response):
    """
    Helper function to print the response details.
    """
    print(f"Status Code: {response.status_code}")
    try:
        pprint(response.json())
    except json.JSONDecodeError:
        print(response.text)

def basic_authentication(ip_address, username, password):
    """
    Authenticate using HTTP Basic Authentication and return True if successful.
    """
    base_url = f"https://{ip_address}:8080"  # Adjust the port if necessary
    auth_header = base64.b64encode(f"{username}:{password}".encode()).decode()
    headers = {"Authorization": f"Basic {auth_header}"}
    try:
        response = requests.get(f"{base_url}/platform/14/protocols/smb/shares", headers=headers, verify=False)
        print("Basic Authentication Response:")
        print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"Error during Basic Authentication: {e}")
        return False

def get_session_details(ip_address, session_cookies):
    """
    Retrieve and print details about the current session.
    """
    base_url = f"https://{ip_address}:8080"
    session_url = f"{base_url}/session/1/session"
    try:
        response = requests.get(session_url, cookies=session_cookies, verify=False)
        print("Session Details Response:")
        print_response(response)
    except Exception as e:
        print(f"Error retrieving session details: {e}")

def session_cookie_authentication(ip_address, username, password):
    """
    Authenticate using Session Cookie and return the session cookies if successful.
    """
    base_url = f"https://{ip_address}:8080"
    session_url = f"{base_url}/session/1/session"
    credentials = {"username": username, "password": password, "services": ["platform", "namespace"]}
    headers = {"Content-Type": "application/json", "Referer": base_url}

    try:
        response = requests.post(session_url, headers=headers, json=credentials, verify=False)
        print("Session Cookie Authentication Response:")
        print_response(response)
        if response.status_code == 201 and 'isisessid' in response.cookies:
            return response.cookies
        else:
            return None
    except Exception as e:
        print(f"Error during Session Cookie Authentication: {e}")
        return None

def csrf_protected_authentication(ip_address, username, password):
    """
    Authenticate using CSRF protected mechanism.
    """
    session_cookies = session_cookie_authentication(ip_address, username, password)
    if session_cookies:
        # Assuming CSRF token is part of the session response or cookies
        csrf_token = session_cookies.get('csrf_token', '')
        headers = {"X-CSRF-Token": csrf_token, "Referer": f"https://{ip_address}:8080"}
        # Valid endpoint for CSRF token validation
        csrf_protected_endpoint = f"https://{ip_address}:8080/platform/14/auth/id"
        try:
            response = requests.get(csrf_protected_endpoint, headers=headers, cookies=session_cookies, verify=False)
            print("CSRF Protected Authentication Response:")
            print_response(response)
            return response.status_code == 200
        except Exception as e:
            print(f"Error during CSRF Protected Authentication: {e}")
            return False
    else:
        return False

# Example usage
ip_address = "10.10.25.80"  # Replace with the actual IP address of the PowerScale
username = "root"
password = "YOUR_PASSWORD"

# Test Basic Authentication
basic_auth_result = basic_authentication(ip_address, username, password)

print("--------------------------------------------------------------------------------")

# Test Session Cookie Authentication
session_cookies = session_cookie_authentication(ip_address, username, password)
if session_cookies:
    get_session_details(ip_address, session_cookies)

print("--------------------------------------------------------------------------------")

# Test CSRF Protected Authentication
csrf_auth_result = csrf_protected_authentication(ip_address, username, password)
