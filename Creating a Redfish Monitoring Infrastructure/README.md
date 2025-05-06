# 🔧 Redfish Monitoring Infrastructure (Prometheus-Based)

This project provides a complete, **Prometheus-based monitoring stack** for datacenter equipment using the **Redfish API**. It monitors **servers**, **PDUs (Power Distribution Units)**, **IRCs (Intelligent Rack Controllers)**, and **CDUs (Cooling Distribution Units)**, collecting real-time metrics like power usage, temperatures, fan speeds, and system health.

---

## 📐 Architecture

```text
               +------------------------+
               |       Grafana          |
               |   (Dashboards)         |
               +-----------+------------+
                           |
                           ▼
                   +---------------+
                   |  Prometheus   |
                   | (Time Series) |
                   +-------+-------+
                           ▲
                           |
                  +--------+--------+
                  |  Redfish Exporter |
                  |   (Exposes /metrics) |
                  +--------+--------+
                           ▲
                           |
           +---------------+---------------+
           |                               |
+--------------------+     +--------------------+
|  Redfish-Enabled    |     |  Redfish-Enabled    |
|   Server / PDU      |     |  IRC / CDU Device   |
+--------------------+     +--------------------+
```

---

## 🧱 Components

### 1. 🔄 Redfish Poller (Python)

* Polls a list of Redfish-enabled devices at fixed intervals
* Queries common Redfish endpoints like `/redfish/v1/Chassis`, `/Thermal`, `/Power`, `/Systems`
* Extracts metrics such as:

  * CPU and system temperatures
  * Fan speeds and health
  * Power draw and voltage
* Feeds these into the in-memory store for the Prometheus exporter

### 2. 📦 Prometheus Exporter

* Lightweight Flask or FastAPI app
* Exposes metrics at `/metrics` in Prometheus format
* Prometheus scrapes this endpoint every 15 seconds (or as configured)

### 3. ⏱ Prometheus

* Time-series database that scrapes metrics from the exporter
* Stores historical data for querying, alerting, and visualization

### 4. 📊 Grafana

* Visualizes Prometheus data through dashboards
* Includes pre-built dashboards for servers, PDUs, IRCs, and CDUs

---

## 🚀 Setup Instructions

### Prerequisites

* Python 3.9+
* Docker & Docker Compose
* Access to Redfish-enabled devices

---

### Step 1: Clone the Repository

```bash
git clone https://github.com/example/redfish-monitoring.git
cd redfish-monitoring
```

---

### Step 2: Define Redfish Targets

Edit `poller/devices.yaml`:

```yaml
devices:
  - name: server01
    ip: 10.10.10.2
    username: admin
    password: yourpassword
  - name: pdu01
    ip: 10.10.10.10
    username: admin
    password: yourpassword
```

---

### Step 3: Launch with Docker Compose

```bash
docker-compose up -d
```

---

### Step 4: Access the Stack

* **Grafana**: [http://localhost:3000](http://localhost:3000)
  Login: `admin` / `admin`
* **Prometheus**: [http://localhost:9090](http://localhost:9090)
* **Exporter metrics** (for testing): [http://localhost:8000/metrics](http://localhost:8000/metrics)

---

## 📊 Grafana Dashboards

Grafana dashboards visualize:

* System temperatures (CPU, ambient)
* Fan speeds and health
* Power usage (watts, amps, volts)
* Device availability

To import:

1. Open Grafana
2. Go to **Dashboards → Import**
3. Upload from `grafana_dashboards/` directory

---

## 🚨 Alerts

Alerts are configured in Prometheus using alerting rules. Example rule:

```yaml
groups:
  - name: redfish_alerts
    rules:
      - alert: HighTemperature
        expr: redfish_temperature_celsius > 80
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "High temperature detected on {{ $labels.instance }}"
```

To enable:

* Mount the rule file in Prometheus via `docker-compose.yml`
* Restart Prometheus

---

## 🛠 Development

To run the poller manually:

```bash
cd poller
pip install -r requirements.txt
python poller.py
```

To test metrics:

```bash
curl http://localhost:8000/metrics
```

---

## 🗃 Directory Structure

```
.
├── docker-compose.yml
├── exporter/
│   └── app.py
├── poller/
│   ├── poller.py
│   └── devices.yaml
├── grafana_dashboards/
│   └── redfish_overview.json
└── README.md
```

---

## 📎 References

* [Redfish Standard](https://www.dmtf.org/standards/redfish)
* [Prometheus](https://prometheus.io/)
* [Grafana](https://grafana.com/)
