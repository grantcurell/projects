# PowerScale Failed Authentication

- [PowerScale Failed Authentication](#powerscale-failed-authentication)
  - [Problem Summary](#problem-summary)
  - [Problem Details](#problem-details)
  - [Expected Behavior](#expected-behavior)
  - [Reproduction](#reproduction)
    - [Demonstration](#demonstration)
  - [Cluster Setup](#cluster-setup)
    - [Rebuild](#rebuild)
    - [Initial Setup](#initial-setup)
  - [Code for Testing Authentication Mechanisms](#code-for-testing-authentication-mechanisms)
  - [Concepts](#concepts)
    - [Super Block Quorum](#super-block-quorum)
    - [How Do Session Teardowns Work?](#how-do-session-teardowns-work)

## Problem Summary

PowerScale OneOS inaccurately reports authentication failures when the number of concurrent sessions is exceeded.

## Problem Details

If `--concurrent-session-limit=LIMIT` is set with `isi auth settings global modify --concurrent-session-limit=15` and that limit is exceeded the logs will say:

**HTTP Error Log**

```
tail -f /var/log/apache2/webui_httpd_error.log
2023-11-28T17:39:39.572651+00:00 <18.3> grantcluster-1(id1) httpd[98700]: [auth_isilon:error] [pid 98700:tid 34421640960] [client 172.16.5.155:62570] (STATUS_ACCESS_DENIED (0xC0000022) HTTP error: 401) Failed issuing a new JWT from the JWT service., referer: https://10.10.25.80:8080
2023-11-28T17:39:39.572673+00:00 <18.3> grantcluster-1(id1) httpd[98700]: [auth_isilon:error] [pid 98700:tid 34421640960] [client 172.16.5.155:62570] (401) Unable to create session., referer: https://10.10.25.80:8080
...SNIP...
2023-11-28T17:39:39.603718+00:00 <18.3> grantcluster-1(id1) httpd[98700]: [auth_isilon:error] [pid 98700:tid 34422848768] [client 172.16.5.155:62559] (STATUS_ACCESS_DENIED (0xC0000022) HTTP error: 401) Failed issuing a new JWT from the JWT service., referer: https://10.10.25.80:8080
2023-11-28T17:39:39.603728+00:00 <18.3> grantcluster-1(id1) httpd[98700]: [auth_isilon:error] [pid 98700:tid 34422848768] [client 172.16.5.155:62559] (401) Unable to create session., referer: https://10.10.25.80:8080
```

**HTTP Access Log**

```
tail -f /var/log/apache2/webui_httpd_access.log
2023-11-28T17:41:43.101276+00:00 <19.6> grantcluster-1(id1) httpd[98697]: 172.16.5.155 - - [28/Nov/2023:17:41:43 +0000] "POST /session/1/session HTTP/1.1" 401 40 "https://10.10.25.80:8080" "python-requests/2.28.1"
```

**REST API Response**

```
Total Successful Sessions: 0
Authentication Failed: Status Code 401, Error: Unable to create session.
```

While this is accurate, technically, it is extremely misleading and has lead to a substantial waste of resources investigating authentication failures when in reality the problem is that concurrent sessions was exceeded.

## Expected Behavior

The errors in [Problem Details](#problem-details) are  misleading to both technicians and users. If the number of concurrent sessions is exceeded both the logs and the API responses should reflect that the issue is that the concurrent sessions have been exceeded instead of reporting an authentication error even if generating JWT tokens is the actual product of exceeding concurrent sessions.

The error message should make it so technicians resolve the problem without having to rely on developer support.


## Reproduction

The below [Python script](https://github.com/grantcurell/grantcurell.github.io/blob/dev/docs/PowerScale%20Failed%20Authentication/multiple_sessions_test.py) will reproduce the problem. Replace the credentials with your PowerScale credentials and then run. It will generate 30 threads each of which will hold a session open for 10 seconds. If the number of concurrent sessions is below 30 it will fail.

```python
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

```

### Demonstration

Confirm concurrent sessions is fixed at 15:

```
grantcluster-1# isi auth settings global view
                            Send NTLMv2: No
                      Space Replacement:
                              Workgroup: WORKGROUP
               Provider Hostname Lookup: disabled
                          Alloc Retries: 5
                 User Object Cache Size: 47.68M
                       On Disk Identity: native
                         RPC Block Time: Now
                       RPC Max Requests: 64
                            RPC Timeout: 30s
Default LDAP TLS Revocation Check Level: none
                   System GID Threshold: 80
                   System UID Threshold: 80
                         Min Mapped Rid: 2147483648
                              Group UID: 4294967292
                               Null GID: 4294967293
                               Null UID: 4294967293
                            Unknown GID: 4294967294
                            Unknown UID: 4294967294
                Failed Login Delay Time: Now
               Concurrent Session Limit: 15
```

Now we run the above Python script:

```
C:\Users\grant\AppData\Local\Programs\Python\Python310\python.exe "C:\Users\grant\Documents\code\grantcurell.github.io\docs\PowerScale Failed Authentication\multiple_sessions_test.py" 
Total Successful Sessions: 0
Authentication Failed: Status Code 401, Error: Unable to create session.
```

Change the concurrent sessions to 31:

```
grantcluster-1# isi auth settings global modify --concurrent-session-limit=31
grantcluster-1# isi auth settings global view
                            Send NTLMv2: No
                      Space Replacement:
                              Workgroup: WORKGROUP
               Provider Hostname Lookup: disabled
                          Alloc Retries: 5
                 User Object Cache Size: 47.68M
                       On Disk Identity: native
                         RPC Block Time: Now
                       RPC Max Requests: 64
                            RPC Timeout: 30s
Default LDAP TLS Revocation Check Level: none
                   System GID Threshold: 80
                   System UID Threshold: 80
                         Min Mapped Rid: 2147483648
                              Group UID: 4294967292
                               Null GID: 4294967293
                               Null UID: 4294967293
                            Unknown GID: 4294967294
                            Unknown UID: 4294967294
                Failed Login Delay Time: Now
               Concurrent Session Limit: 31

```

Rerun the script:

```
C:\Users\grant\AppData\Local\Programs\Python\Python310\python.exe "C:\Users\grant\Documents\code\grantcurell.github.io\docs\PowerScale Failed Authentication\multiple_sessions_test.py" 
Total Successful Sessions: 30

Process finished with exit code 0
```

## Cluster Setup

### Rebuild

I hopped on an old cluster I used for testing and ran `isi_reformat_node`

### Initial Setup

These are the settings I used for my build. Since I was building this in a lab I told it to use the internal IP addresses for external as well instead of making them separate sets.

| Configuration Item      | Value                |
|-------------------------|--------------------------|
| Cluster name            | grantcluster             |
| Encoding                | utf-8                    |
| int-a netmask           | 255.255.255.0            |
| int-a IP ranges         | { 10.10.25.80-10.10.25.89 } |
| int-a IP range          | { 10.10.25.80-10.10.25.89 } |
| int-a gateway           | 10.10.25.1               |
| SmartConnect zone name  | onefs                    |
| DNS servers             | { 10.10.25.120 }         |
| Search domains          | { grant.lan, lan }       |

After I joined the nodes together I confirmed they had a quorum:

```bash
grantcluster-1# sysctl efs.gmp.has_quorum
efs.gmp.has_quorum: 1
grantcluster-1# sysctl efs.gmp.has_super_block_quorum
efs.gmp.has_super_block_quorum: 1
```

1 indicates success whereas 0 indicates that there is no quorum. Super Blocks are described [here](#super-block-quorum).

## Code for Testing Authentication Mechanisms

I used [this code](https://github.com/grantcurell/grantcurell.github.io/blob/dev/docs/PowerScale%20Failed%20Authentication/authentication_test.py) to test the different authentication mechanisms to confirm valid credentials.

## Concepts

### Super Block Quorum

Referred to as `efs.gmp.has_super_block_quorum`, is a property that ensures the file system's integrity by requiring more than half of the nodes in the cluster to be available and in agreement over the internal network. This quorum prevents data conflicts, such as conflicting versions of the same file if two groups of nodes become unsynchronized. If a node is unreachable, OneFS will separate it from the cluster, known as splitting. Operations can continue as long as a quorum of nodes remains connected. If the split nodes can reconnect and re-synchronize, they rejoin the majority group in a process known as merging. The superblock quorum status can be checked by connecting to a node via SSH and running the `sysctl efs.gmp.has_super_block_quorum` command-line tool as root.

### How Do Session Teardowns Work?

See [Session Teardown Reverse Engineering](./session_teardown_reverse_engineering.md)