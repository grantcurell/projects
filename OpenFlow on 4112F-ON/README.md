# Reading Material

[Open Flow Switch Specification v1.3.1](./Reading_Material/openflow-spec-v1.3.1.pdf)

[OS10 Setup Instructions](./Reading_Material/force10-s3048-on_connectivity-guide4_en-us.pdf)

# Overview

# My Configuration

- Controller is running RHEL 8
- I am using a S4112F-ON
- I am using a Ryu OpenFlow controller
- OpenSwitch version PKGS_OPX-3.2.0-installer-x86_64

## RHEL Release Info

    NAME="Red Hat Enterprise Linux"
    VERSION="8.0 (Ootpa)"
    ID="rhel"
    ID_LIKE="fedora"
    VERSION_ID="8.0"
    PLATFORM_ID="platform:el8"
    PRETTY_NAME="Red Hat Enterprise Linux 8.0 (Ootpa)"
    ANSI_COLOR="0;31"
    CPE_NAME="cpe:/o:redhat:enterprise_linux:8.0:GA"
    HOME_URL="https://www.redhat.com/"
    BUG_REPORT_URL="https://bugzilla.redhat.com/"

    REDHAT_BUGZILLA_PRODUCT="Red Hat Enterprise Linux 8"
    REDHAT_BUGZILLA_PRODUCT_VERSION=8.0
    REDHAT_SUPPORT_PRODUCT="Red Hat Enterprise Linux"
    REDHAT_SUPPORT_PRODUCT_VERSION="8.0"
    Red Hat Enterprise Linux release 8.0 (Ootpa)
    Red Hat Enterprise Linux release 8.0 (Ootpa)

# Setup

## Setup Controller

### Install Prereqs

    pip-3.6 install ryu

### Setup Virtualenv

    python3.6 -m virtualenv ./app
    source bin/activate

## Setup OpenFlow on the Switch

### Enable OpenFlow

On the switch run:

    OS10# configure terminal
    OS10(config)# openflow
    OS10(config-openflow)# mode openflow-only
    Configurations not relevant to openflow mode will be removed from the startup-configuration and system will be rebooted. Do you want to proceed? [confirm yes/no]:yes

## Setup the Switch

**WARNING**: At the time of writing the documentation on OpenSwitch's site is out of date. Many of the commands listed do not work.

### ONIE Boot Switch

To find the installer, ONIE will use an automated discovery process. It will use DHCP to discover a DNS server and that DNS server must have a record called onie-server which points to a web server or TFTP server hosting the installation media. It expects the file on the web server to be called onie-installer.

1. Download [the operating system](https://archive.openswitch.net/installers/stable/Dell-EMC/PKGS_OPX-3.2.0-installer-x86_64.bin)
2. Host the file on a web server of your choosing
3. Add a symlink for the file called "onie-installer".
4. On your DNS server add a record for onie-server pointing to your web server.


### Configure Out of Band Management Interface

1. On the switch, edit the file `/etc/network/interfaces.d/eth0` as root
2. Add:

        auto eth0
        allow-hotplug eth0
        iface eth0 inet static
          address <YOUR_IP>/<YOUR_CIDR_NETMASK>
          gateway <YOUR_GATEWAY>
          nameserver <YOUR_DNS_SERVER>

3. Run `sudo systemctl restart networking`
   1. Note: One of the things I noticed is the official documentation still references `service`. On my system everything was `systemd`.

### Configure OpenFlow Controller

    OS10# configure terminal
    OS10(config)# openflow
    OS10(config-openflow)# switch of-switch-1
    OS10(config-openflow-switch)# controller ipv4 <YOUR_CONTROLLER_IP> port 6633
    OS10(config-openflow-switch)# no shutdown

# Testing the Setup

# Noted Limitations

- The Dell switches do not support the FLOOD port type which limits their functionality as a switch
- IN_PORT is not supported so you have to program around figuring out the ingress port
- The version of OS10 I have does not support the `debug openflow` command
- The version of OS10 I have does not support any OpenFlow show commands beyond `show openflow flows` and `show openflow switch`