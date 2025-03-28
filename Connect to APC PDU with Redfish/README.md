# Connect to APC PDU with Redfish

This repo contains a set of Python tools for interacting with an APC PDU via the Redfish API. These scripts support API discovery, telemetry monitoring, and outlet control stress testing.

## 🔧 Scripts

### `redfish_discovery.py`

Recursively crawls the Redfish API starting from the root URI and maps out all reachable endpoints. Useful for reverse engineering the API structure or validating firmware features.

- Outputs discovered paths to the terminal and saves a Markdown report for documentation.
- Automatically follows nested links and handles connection errors gracefully.

**Example:**
```bash
python redfish_discovery.py
```

> Edit the script to fill in your PDU IP, credentials, and desired SSL behavior.

---

### `pdu_telemetry.py`

Fetches live telemetry from the PDU, including total power usage and status details for individual outlets.

- Reports power, voltage, current, energy usage, and health info.
- Outputs formatted tables for clarity.
- Designed to be run periodically or integrated into monitoring tools.

**Example:**
```bash
python pdu_telemetry.py
```

> Edit the top of the script to configure your PDU IP, port (usually 8443), credentials, and SSL settings.

Example output:

```txt
C:\Users\grant\AppData\Local\Programs\Python\Python310\python.exe "C:\Users\grant\Documents\code\dell\Connect to APC PDU with Redfish\pdu_telemetry.py" 

### PDU Telemetry Report - 2025-03-28T16:39:41.764492 ###


### PDU Summary Metrics ###

╒═════════════╤═════════════════╤══════════════════╤════════════════╤════════════════╕
│   Power (W) │   Apparent (VA) │   Reactive (VAR) │   Power Factor │   Energy (kWh) │
╞═════════════╪═════════════════╪══════════════════╪════════════════╪════════════════╡
│           0 │               0 │                0 │              1 │        937.939 │
╘═════════════╧═════════════════╧══════════════════╧════════════════╧════════════════╛

### Outlet 1 Status ###

╒═════════════╤══════════════════════════════════════╤══════════╤═════════╤═════════╤═══════════╤══════════════╤═════════════╤══════════════╤════════╤═════════╤═══════╕
│ ID          │ Name                                 │ Health   │ State   │ Power   │ Enabled   │   Rated Amps │ Nominal V   │   V (Actual) │   Amps │   Watts │   kWh │
╞═════════════╪══════════════════════════════════════╪══════════╪═════════╪═════════╪═══════════╪══════════════╪═════════════╪══════════════╪════════╪═════════╪═══════╡
│ PDU1OUTLET1 │ Outlet PDU1OUTLET1, Branch Circuit A │ OK       │ Enabled │ Off     │ True      │           10 │ AC208V      │            0 │      0 │       0 │     0 │
╘═════════════╧══════════════════════════════════════╧══════════╧═════════╧═════════╧═══════════╧══════════════╧═════════════╧══════════════╧════════╧═════════╧═══════╛

### Outlet 2 Status ###

╒══════════╤═══════════════════════════════════╤══════════╤═════════╤═════════╤═══════════╤══════════════╤═════════════╤══════════════╤════════╤═════════╤═══════╕
│ ID       │ Name                              │ Health   │ State   │ Power   │ Enabled   │   Rated Amps │ Nominal V   │   V (Actual) │   Amps │   Watts │   kWh │
╞══════════╪═══════════════════════════════════╪══════════╪═════════╪═════════╪═══════════╪══════════════╪═════════════╪══════════════╪════════╪═════════╪═══════╡
│ OUTLET 2 │ Outlet OUTLET 2, Branch Circuit A │ OK       │ Enabled │ On      │ True      │           16 │ AC208V      │            0 │      0 │       0 │     0 │
╘══════════╧═══════════════════════════════════╧══════════╧═════════╧═════════╧═══════════╧══════════════╧═════════════╧══════════════╧════════╧═════════╧═══════╛

### Outlet 3 Status ###

╒══════════╤═══════════════════════════════════╤══════════╤═════════╤═════════╤═══════════╤══════════════╤═════════════╤══════════════╤════════╤═════════╤═══════╕
│ ID       │ Name                              │ Health   │ State   │ Power   │ Enabled   │   Rated Amps │ Nominal V   │   V (Actual) │   Amps │   Watts │   kWh │
╞══════════╪═══════════════════════════════════╪══════════╪═════════╪═════════╪═══════════╪══════════════╪═════════════╪══════════════╪════════╪═════════╪═══════╡
│ OUTLET 3 │ Outlet OUTLET 3, Branch Circuit A │ OK       │ Enabled │ On      │ True      │           10 │ AC208V      │            0 │      0 │       0 │     0 │
╘══════════╧═══════════════════════════════════╧══════════╧═════════╧═════════╧═══════════╧══════════════╧═════════════╧══════════════╧════════╧═════════╧═══════╛

### Outlet 4 Status ###

╒══════════╤═══════════════════════════════════╤══════════╤═════════╤═════════╤═══════════╤══════════════╤═════════════╤══════════════╤════════╤═════════╤═══════╕
│ ID       │ Name                              │ Health   │ State   │ Power   │ Enabled   │   Rated Amps │ Nominal V   │   V (Actual) │   Amps │   Watts │   kWh │
╞══════════╪═══════════════════════════════════╪══════════╪═════════╪═════════╪═══════════╪══════════════╪═════════════╪══════════════╪════════╪═════════╪═══════╡
│ OUTLET 4 │ Outlet OUTLET 4, Branch Circuit A │ OK       │ Enabled │ On      │ True      │           16 │ AC208V      │            0 │      0 │       0 │     0 │
╘══════════╧═══════════════════════════════════╧══════════╧═════════╧═════════╧═══════════╧══════════════╧═════════════╧══════════════╧════════╧═════════╧═══════╛

Process finished with exit code 0
```

---

### `stress_test_outlet.py`

Sends rapid toggle requests to a specified outlet to simulate control stress or validate firmware stability under load.

- Supports CLI options for outlet number, duration, interval, SSL, and verbosity.
- Logs each request and response to a file for auditing/debugging.
- Tracks success/failure metrics and reports errors at the end.

**Examples:**
```bash
# Basic usage
python stress_test_outlet.py --pdu-ip 192.168.1.100 --username admin --password secret

# Stress outlet 2 for 2 minutes, toggling every 5 seconds
python stress_test_outlet.py --pdu-ip 192.168.1.100 --username admin --password secret --outlet 2 --duration 120 --interval 5

# Enable verbose logging and SSL verification
python stress_test_outlet.py --pdu-ip 192.168.1.100 --username admin --password secret --verify -v
```

---

## ⚙️ Notes

- All scripts communicate with the Redfish API over HTTPS (default port: `8443`).
- These tools have been tested on APC PDUs but may work with other Redfish-compatible hardware.
- SSL verification is disabled by default — enable it for production use.
