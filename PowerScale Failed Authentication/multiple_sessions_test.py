import requests
import threading
import time
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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
        if response.status_code == 201 and 'isisessid' in response.cookies:
            return response.cookies
        else:
            error_message = response.json().get('message', 'No detailed error message provided.')
            return f"Authentication Failed: Status Code {response.status_code}, Error: {error_message}"
    except Exception as e:
        return f"Error during Session Cookie Authentication: {e}"


def create_and_hold_session(ip_address, username, password, hold_time, results):
    """
    Create a session and hold it open for a specified duration.
    """
    session_result = session_cookie_authentication(ip_address, username, password)
    if isinstance(session_result, requests.cookies.RequestsCookieJar):
        time.sleep(hold_time)  # Hold the session
        results.append("Session created and held successfully.")
    else:
        results.append(session_result)


def main():
    ip_address = "10.10.25.80"  # Replace with the actual IP address of the PowerScale
    username = "root"
    password = "YOUR_PASSWORD"
    hold_time = 10  # Hold time in seconds
    session_threads = []
    results = []

    # Create 30 concurrent sessions
    for _ in range(30):
        thread = threading.Thread(target=create_and_hold_session, args=(ip_address, username, password, hold_time, results))
        thread.start()
        session_threads.append(thread)

    # Wait for all threads to complete
    for thread in session_threads:
        thread.join()

    # Analyze results and print summary
    success_count = results.count("Session created and held successfully.")
    print(f"Total Successful Sessions: {success_count}")
    error_messages = set([result for result in results if result != "Session created and held successfully."])
    for error in error_messages:
        print(error)


if __name__ == "__main__":
    main()
