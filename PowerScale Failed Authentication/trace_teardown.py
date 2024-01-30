import requests
import json
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Setup for detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def session_cookie_authentication(ip_address, username, password):
    """
    Authenticate using Session Cookie and return the session cookies if successful.
    """
    base_url = f"https://{ip_address}:8080"
    session_url = f"{base_url}/session/1/session"
    credentials = {"username": username, "password": password, "services": ["platform", "namespace"]}
    headers = {"Content-Type": "application/json", "Referer": base_url}

    logger.debug("Attempting to authenticate and create a session...")
    try:
        response = requests.post(session_url, headers=headers, json=credentials, verify=False)
        logger.debug(f"Authentication response: {response.status_code}, {response.text}")

        if response.status_code == 201 and 'isisessid' in response.cookies:
            logger.debug("Session successfully created. Cookies: %s", response.cookies.get_dict())
            return response.cookies, base_url
        else:
            logger.error("Failed to authenticate. Status Code: %s, Response: %s", response.status_code, response.text)
            return None, None
    except Exception as e:
        logger.exception("Error during Session Cookie Authentication")
        return None, None


def close_session(base_url, session_cookies):
    """
    Close the session explicitly.
    """
    session_url = f"{base_url}/session/1/session"
    logger.debug("Attempting to close the session...")

    try:
        response = requests.delete(session_url, cookies=session_cookies, verify=False)
        logger.debug(f"Session closure response: {response.status_code}, {response.text}")

        if response.status_code == 204:
            logger.debug("Session successfully closed.")
        else:
            logger.error("Failed to close the session. Status Code: %s, Response: %s", response.status_code, response.text)
    except Exception as e:
        logger.exception("Error during session closure")


def main():
    ip_address = "10.10.25.80"  # Replace with the actual IP address of the PowerScale
    username = "root"
    password = "YOUR_PASSWORD"

    # Authenticate and create a session
    session_cookies, base_url = session_cookie_authentication(ip_address, username, password)

    # If session is created, proceed to close it
    if session_cookies and base_url:
        close_session(base_url, session_cookies)


if __name__ == "__main__":
    main()
