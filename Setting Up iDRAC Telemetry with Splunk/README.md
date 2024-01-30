# Setting Up iDRAC Telemetry with Splunk

## Helpful Links

Dell API Docs: https://developer.dell.com/apis/2978/versions/5.xx/docs/0WhatsNew.md

Redfish Telemetry Whitepaper: https://www.dmtf.org/sites/default/files/standards/documents/DSP2051_1.0.0.pdf

Description of the AMQP Messaging Protocol: https://www.ionos.com/digitalguide/websites/web-development/advanced-message-queuing-protocol-amqp/

Setting Up Splunk for the First Time: https://docs.splunk.com/Documentation/Splunk/8.2.4/Installation/StartSplunkforthefirsttime

Integrate iDRAC Telemetry Data Into Splunk: [Link to PDF](integrate-idrac9-telemetry-data-into-splunk-platform.pdf)

## My Test Environment

### RHEL

```
NAME="Red Hat Enterprise Linux"
VERSION="8.5 (Ootpa)"
ID="rhel"
ID_LIKE="fedora"
VERSION_ID="8.5"
PLATFORM_ID="platform:el8"
PRETTY_NAME="Red Hat Enterprise Linux 8.5 (Ootpa)"
ANSI_COLOR="0;31"
CPE_NAME="cpe:/o:redhat:enterprise_linux:8::baseos"
HOME_URL="https://www.redhat.com/"
DOCUMENTATION_URL="https://access.redhat.com/documentation/red_hat_enterprise_linux/8/"
BUG_REPORT_URL="https://bugzilla.redhat.com/"

REDHAT_BUGZILLA_PRODUCT="Red Hat Enterprise Linux 8"
REDHAT_BUGZILLA_PRODUCT_VERSION=8.5
REDHAT_SUPPORT_PRODUCT="Red Hat Enterprise Linux"
REDHAT_SUPPORT_PRODUCT_VERSION="8.5"
Red Hat Enterprise Linux release 8.5 (Ootpa)
Red Hat Enterprise Linux release 8.5 (Ootpa)
```

## Installation

### Setup Splunk

1. Download [trial of Splunk](https://www.splunk.com/en_us/download/splunk-enterprise.html?skip_request_page=1)
2. Follow [Splunk installation instructions](https://docs.splunk.com/Documentation/Splunk/8.2.4/Installation/InstallonLinux)
3. By default it will install to /opt/splunk. Run `/opt/splunk/bin/splunk start` (I suggest you do this in tmux or another terminal emulator)
4. Run `firewall-cmd --permanent --zone public --add-port=8000/tcp && firewall-cmd --reload`
5. Make splunk start on boot with `/opt/splunk/bin/splunk enable boot-start`

#### Using Syslog

1. Following the instructions [here](https://splunk.github.io/splunk-connect-for-syslog/main/gettingstarted/)
2. Install podman with `dnf install -y podman`
3. Follow the instructions [here](https://splunk.github.io/splunk-connect-for-syslog/main/gettingstarted/podman-systemd-general/)
      1.NOTE: When adding the HTTP input in Splunk it failed out because the token weren't enabled. I had to manually edit `/opt/splunk/etc/apps/splunk_httpinput/default/inputs.conf` and set disabled to 0 then do a `systemctl restart splunk`
4.  Run `systemctl stop rsyslog && systemctl disable rsyslog`

#### Using ActiveMQ and splunkpump

1. `dnf install -y podman`
2. `mkdir -p  mkdir -p /opt/activemq/data && /opt/activemq/conf`
3. Run the following to generate default configs:

    ```bash
    podman run --user root --rm -ti -p 61616:61616 -p 8161:8161 -v /opt/activemq/conf:/mnt/conf:z -v /opt/activemq/data:/mnt/data:z rmohr/activemq /bin/sh
    chown activemq:activemq /mnt/conf
    chown activemq:activemq /mnt/data
    cp -a /opt/activemq/conf/* /mnt/conf/
    cp -a /opt/activemq/data/* /mnt/data/
    exit
    ```

4. `podman run -p 61616:61616 -p 8161:8161 -v /opt/activemq/conf:/opt/activemq/conf -v /opt/activemq/data:/opt/activemq/data rmohr/activemq`
5. 
### Configure the iDRAC

1. Download [this script](https://github.com/dell/iDRAC-Telemetry-Scripting/blob/master/ConfigurationScripts/EnableOrDisableAllTelemetryReports.py) which will enable telemetry reports.
2. Run `EnableOrDisableAllTelemetryReports.py -ip $target -u $user -p $password`
      1.This enables telemetry on the target server

#### Using ActiveMQ and splunkpump

#### Using Syslog

1. Next you will need to enable Redfish alerting which will publish the events to Splunk. Download [this script](https://github.com/dell/iDRAC-Telemetry-Scripting/blob/master/ConfigurationScripts/SubscriptionManagementREDFISH.py)
2. Run the following command `SubscriptionManagementREDFISH.py -ip $target -u $user -p $password -c y -D https://$splunkserver/services/collector/raw -E Alert -V Event`
      1.`$target` is the ip address or DNS name of the iDRAC
      2.`$user/$password` are the username and password for iDRAC
      3.`$splunkserver` is the IP address or DNS name of your Splunk HTTP event collector instance
3. On the command line (racadm)
      1.SSH to the iDRAC
      2.Run 

        ```
        racadm set idrac.telemetry.RsyslogServer1 "<splunk_ip/fqdn>"
        racadm set idrac.telemetry.RsyslogServer1port "514"
        racadm testrsyslogconnection
        ```