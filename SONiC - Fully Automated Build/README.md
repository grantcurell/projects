# SONiC Fully Automated Build

## Install the Operating System

1. Download SONiC OS for whatever manufacturer. In my case I pulled Dell's stable image.
   1. Note: My testing is on a Z9264F-ON.
2. Follow the instructions [for setting up and running ONIE](../README.md#how-to-configure-onie)

## Configure ZTP

https://infohub.delltechnologies.com/l/enterprise-sonic-distribution-by-dell-technologies-lifecycle-management/introduction-857

```json
"initial-config": {
  "plugin": {
    "name": "config-db-json"
  },
  "url": {
    "source": "http://192.168.1.1:8080/spine01_first_boot_config.json",
    "destination": "/etc/sonic/config_db.json",
    "secure": false
  }
}
```

## TODO

- First I want to get it working with a fixed file, then we'll do dynamic content
- Build out a templating system for provisioning multiple switches in Ansible