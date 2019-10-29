# Reverse Lag Test - OS10

In this test case the goal is to create a simple packet broker using a reverse
LAG port.

# Helpful Links

[ONIE Network Install Process Overview](https://opencomputeproject.github.io/onie/user-guide/index.html#installing-over-the-network)

[Dell OS10 Manual](https://topics-cdn.dell.com/pdf/networking-s5148f-on_connectivity-guide4_en-us.pdf)

# My Configuration

## General Configuration

- ONIE host is running RHEL 8
- I am using a Dell S4112F-ON for testing
- OpenSwitch version PKGS_OPX-3.2.0-installer-x86_64
- PFSense running DNS and DHCP as services

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

## OS 10 Version

    OS10# show version
    Dell EMC Networking OS10 Enterprise
    Copyright (c) 1999-2019 by Dell Inc. All Rights Reserved.
    OS Version: 10.5.0.2
    Build Version: 10.5.0.2.468
    Build Time: 2019-10-19T00:29:00+0000
    System Type: S4112F-ON
    Architecture: x86_64
    Up Time: 00:03:39

# Setup ONIE Prerequisites

See [ONIE Install Setup](/README.md#how-to-configure-onie) for instructions.

# Configure Management Interface

See [Configure Management Interface on Dell OS10](/README.md#configure-managment-interface-on-dell-os10)

# Configure Device for Reverse LAG

## Physical Configuration

I used the following SFPs

- 1, 1Gb/s copper SFP (Ethernet 1/1/1) for input
- 2, 1Gb/s copper SFPs (Ethernet 1/1/5/Ethernet 1/1/9) and 1, 1Gb/s, fiber SFP (Ethernet 1/1/12) for output

### Input Port
![](images/input_port.JPG)

### Output Ports
![](images/output_ports.JPG)

## LAG Configuration

### Enable LAG Ports and Input Port

#### Verify All Interfaces are Running at the Same Speed

All interfaces must be the same speed in a LAG. In my case, the fiber interface
was running at 10Gb/s so I brought that down to 1Gb/s by doing the following:

    OS10(config)# interface ethernet 1/1/12
    OS10(conf-if-eth1/1/12)# speed 1000
    OS10(conf-if-eth1/1/12)# <165>1 2019-10-28T19:10:22.616888+00:00 OS10 dn_alm 669 - - Node.1-Unit.1:PRI [event], Dell EMC (OS10) %IFM_OSTATE_DN: Interface operational state is down :ethernet1/1/12
    OS10(conf-if-eth1/1/12)#
    OS10(conf-if-eth1/1/12)# <165>1 2019-10-28T19:10:29.591467+00:00 OS10 dn_alm 669 - - Node.1-Unit.1:PRI [event], Dell EMC (OS10) %IFM_OSTATE_UP: Interface operational state is up :ethernet1/1/12

#### Add Interfaces to the Port Channel Group

    OS10(config)# interface port-channel 1
    OS10(conf-if-po-1)# exit
    OS10(config)# interface ethernet 1/1/5
    OS10(conf-if-eth1/1/5)# channel-group 1 mode on
    
    OS10(conf-if-eth1/1/5)# <165>1 2019-10-28T19:17:33.746593+00:00 OS10 dn_alm 669 - - Node.1-Unit.1:PRI [event], Dell EMC (OS10) %IFM_OSTATE_UP: Interface operational state is up :port-channel1

    OS10(conf-if-eth1/1/5)# exit
    OS10(config)# interface ethernet 1/1/9
    OS10(conf-if-eth1/1/9)# channel-group 1 mode on
    OS10(conf-if-eth1/1/9)# exit
    OS10(config)# interface ethernet 1/1/12
    OS10(conf-if-eth1/1/12)# channel-group 1 mode on

#### Configure the Port Channel Hash Algorithm

We want to load balance on the standard network 5 tuple. You can configure this with

    OS10(config)# load-balancing ip-selection destination-ip source-ip protocol l4-destination-port l4-source-port

#### Configure Mirror Port Session from Source to LAG Interface

Next we need to send all the traffic from our "TAP" input interface to our port
channel to be load balanced out to all of our listening devices.

    OS10(config)# monitor session 1
    OS10(conf-mon-local-1)# source interface ethernet 1/1/1
    OS10(conf-mon-local-1)# destination interface port-channel 1
    OS10(conf-mon-local-1)# no shut

# Final Configuration

    OS10# show running-configuration
    ! Version 10.5.0.2
    ! Last configuration change at Oct  29 14:53:37 2019
    !
    ip vrf default
    !
    interface breakout 1/1/13 map 100g-1x
    interface breakout 1/1/14 map 100g-1x
    interface breakout 1/1/15 map 100g-1x
    iscsi enable
    iscsi target port 860
    iscsi target port 3260
    system-user linuxadmin password XXXXX
    username admin password XXXXX role sysadmin priv-lvl 15
    aaa authentication login default local
    aaa authentication login console local
    !
    class-map type application class-iscsi
    !
    policy-map type application policy-iscsi
    !
    interface vlan1
    no shutdown
    !
    interface port-channel1
    no shutdown
    switchport access vlan 1
    !
    interface mgmt1/1/1
    no shutdown
    no ip address dhcp
    ip address 192.168.1.20/24
    ipv6 address autoconfig
    !
    interface ethernet1/1/1
    no shutdown
    switchport access vlan 1
    flowcontrol receive on
    !
    interface ethernet1/1/2
    no shutdown
    switchport access vlan 1
    flowcontrol receive on
    !
    interface ethernet1/1/3
    no shutdown
    switchport access vlan 1
    flowcontrol receive on
    !
    interface ethernet1/1/4
    no shutdown
    switchport access vlan 1
    flowcontrol receive on
    !
    interface ethernet1/1/5
    no shutdown
    channel-group 1
    no switchport
    flowcontrol receive on
    !
    interface ethernet1/1/6
    no shutdown
    switchport access vlan 1
    flowcontrol receive on
    !
    interface ethernet1/1/7
    no shutdown
    switchport access vlan 1
    flowcontrol receive on
    !
    interface ethernet1/1/8
    no shutdown
    switchport access vlan 1
    flowcontrol receive on
    !
    interface ethernet1/1/9
    no shutdown
    channel-group 1
    no switchport
    flowcontrol receive on
    !
    interface ethernet1/1/10
    no shutdown
    switchport access vlan 1
    flowcontrol receive on
    !
    interface ethernet1/1/11
    no shutdown
    no switchport
    flowcontrol receive on
    !
    interface ethernet1/1/12
    no shutdown
    channel-group 1
    no switchport
    speed 1000
    flowcontrol receive on
    !
    interface ethernet1/1/13
    no shutdown
    switchport access vlan 1
    flowcontrol receive on
    !
    interface ethernet1/1/14
    no shutdown
    switchport access vlan 1
    flowcontrol receive on
    !
    interface ethernet1/1/15
    no shutdown
    switchport access vlan 1
    flowcontrol receive on
    !
    monitor session 1
    destination interface port-channel1
    source interface ethernet1/1/1
    no shut
    !
    snmp-server contact "Contact Support"
    !
    telemetry

