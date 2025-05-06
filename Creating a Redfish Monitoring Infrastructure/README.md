# 🔧 Redfish Infrastructure Monitoring Stack

This project provides a complete monitoring and observability solution for datacenter hardware using the **Redfish API**. It targets **servers**, **PDUs (Power Distribution Units)**, **IRCs (Intelligent Rack Controllers)**, and **CDUs (Cooling Distribution Units)**—enabling real-time metric collection, historical analytics, and alerting.

---

## 📐 Architecture Overview

```text
               +------------------------+
               |    Grafana             |
               |   (Dashboards)         |
               +-----------+------------+
                           |
                           ▼
                +----------------------+
                |   Time-Series DB     |
                |  (Prometheus/Influx) |
                +----------+-----------+
                           ▲
           +---------------+------------------+
           |                                  |
+----------------------+         +---------------------------+
| Redfish Exporter     |         | Custom Poller Application |
| (Prometheus format)  |<------->|  (Python, queries targets)|
+----------+-----------+         +---------------------------+
           |
           ▼
+----------------------------+
| Redfish-enabled Hardware   |
|  - Servers                 |
|  - PDUs                    |
|  - IRCs                    |
|  - CDUs                    |
+----------------------------+
```

---

## 🧱 Components

### 1. 🔄 Redfish Poller

A Python-based polling service that:

* Periodically queries each device using HTTPS Redfish endpoints
* Extracts relevant metrics (temperatures, power usage, fan speeds, power state)
* Writes data to:

  * A time-series database (InfluxDB)
  * Or exposes it to a Prometheus exporter endpoint

### 2. 📦 Exporter (Optional if using Prometheus)

If Prometheus is used, this is a small Flask or FastAPI server that:

* Exposes `/metrics` endpoint in Prometheus format
* The Poller pushes data into an internal in-memory cache
* Prometheus scrapes this endpoint on interval

### 3. ⏱ Time Series Database

Choose one:

* **Prometheus** (pull-based, easy Grafana integration)
* **InfluxDB** (push-based, good for large-scale, flexible tagging)

### 4. 📊 Grafana Dashboards

Prebuilt dashboards and custom visualizations for:

* Per-rack server temperatures
* PDU power draw
* CDU cooling flow rates
* Alerts (e.g., high temp or power threshold crossed)

### 5. 🚨 Alerting

* Prometheus Alertmanager or Grafana Alerting
* Optional integration with:

  * Slack
  * Email
  * PagerDuty
  * Webhooks to remediation tools (e.g., Ansible, StackStorm)

---

## 🚀 Setup Instructions

### Prerequisites

* Python 3.9+
* Docker / Docker Compose
* Git
* Redfish-enabled hardware with network access

---

### 🧪 Quickstart (with Docker Compose)

Clone the repo:

```bash
git clone https://github.com/example/redfish-monitoring.git
cd redfish-monitoring
```

Create `.env` with device info (or use `devices.yaml`):

```yaml
devices:
  - name: server01
    ip: 10.10.10.2
    username: admin
    password: secret
  - name: pdu01
    ip: 10.10.10.10
    username: admin
    password: secret
```

Launch the stack:

```bash
docker-compose up -d
```

Access services:

* Grafana: [http://localhost:3000](http://localhost:3000) (user: `admin`, pass: `admin`)
* Prometheus (if used): [http://localhost:9090](http://localhost:9090)

---

## 🧠 How It Works

### Redfish Poller (`poller.py`)

* Loads device list from `devices.yaml`
* Authenticates to each Redfish endpoint
* Queries:

  * `Systems` → temperature, power state, fans
  * `Chassis` → thermal, power usage
  * `PowerEquipment` → for CDUs/PDUs
* Normalizes data to metrics
* Pushes to:

  * Exporter (`POST /ingest`)
  * Or InfluxDB directly (using Telegraf or Python client)

### Exporter (`exporter.py`)

* Flask/FastAPI app exposes `/metrics`
* In-memory metrics store
* Prometheus scrapes `/metrics` on interval

---

## 🔧 Configuration

* `devices.yaml`: Define monitored hardware
* `poll_interval`: Set in `config.yaml` or `.env`
* `log_level`: `INFO`, `DEBUG`, etc.
* Exporter bind port: default `8000`

---

## 📊 Grafana Dashboards

Import dashboards:

* Navigate to [http://localhost:3000](http://localhost:3000)
* Choose `Dashboards → Import`
* Upload from `grafana_dashboards/`

Dashboards include:

* 🔥 Thermal summary (fan, CPU temp)
* ⚡ Power usage over time
* 🌡️ Environmental sensors (humidity, coolant)

---

## 🚨 Alerts

Set alerts via Grafana UI or YAML files:

* `High CPU Temp`: >80°C
* `Total PDU Load`: >80% rated
* `CDU Flow Rate`: <5 L/min

Example (Prometheus rule):

```yaml
groups:
  - name: redfish_alerts
    rules:
      - alert: HighTemperature
        expr: redfish_cpu_temp_celsius > 80
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "High temperature on {{ $labels.instance }}"
```

---

## 🔐 Security

* Use HTTPS with Redfish (TLS 1.2+)
* Store secrets with HashiCorp Vault or Ansible Vault
* Run containers with least privilege

---

## 🛠 Extendability

You can easily add:

* More devices to `devices.yaml`
* SNMP fallback via Telegraf if Redfish is unavailable
* CMDB sync (e.g., NetBox API)

---

## 🧪 Development

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python poller.py
```

To test locally:

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
├── config/
│   └── config.yaml
├── .env
└── README.md
```

---

## ❓FAQ

**Q:** What if a device doesn't support Redfish fully?
**A:** You can customize the poller logic to skip or fallback. Many legacy devices provide partial data.

**Q:** Can I use this for Dell/HP/iDRAC/iLO?
**A:** Yes. Redfish is a DMTF standard and supported by all major vendors. Check with your firmware version.

---

## 📎 References

* Redfish API Docs: [https://redfish.dmtf.org](https://redfish.dmtf.org)
* Prometheus: [https://prometheus.io](https://prometheus.io)
* Grafana: [https://grafana.com](https://grafana.com)
* InfluxDB: [https://www.influxdata.com](https://www.influxdata.com)
