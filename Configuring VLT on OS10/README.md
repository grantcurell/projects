# Configuring VLT on OS10

## My Test Platform

    OS10# show version
    Dell EMC Networking OS10 Enterprise
    Copyright (c) 1999-2020 by Dell Inc. All Rights Reserved.
    OS Version: 10.5.1.3
    Build Version: 10.5.1.3.190
    Build Time: 2020-06-19T21:48:07+0000
    System Type: S4112F-ON
    Architecture: x86_64
    Up Time: 00:19:57

![](images/diagram.jpg)
    
## Configuration of VLT

### Device 1

    # Configure management
    configure terminal
    interface mgmt 1/1/1
    no ip address dhcp
    ip address 192.168.1.24/24
    exit
    # Configure spanning tree
    spanning-tree mode rstp
    interface range ethernet 1/1/13-1/1/14
    # Create a VLT Domain and Configure the VLT interconnect (VLTi)
    no switchport
    exit
    vlt-domain 1
    discovery-interface ethernet 1/1/13
    discovery-interface ethernet 1/1/14
    # Configure the VLT Priority, VLT MAC Address, and VLT Backup Link
    primary-priority 4096
    vlt-mac 00:11:22:33:44:55
    backup destination 192.168.1.25
    end

### Device 2

    # Configure management
    configure terminal
    interface mgmt 1/1/1
    no ip address dhcp
    ip address 192.168.1.25/24
    exit
    # Configure spanning tree
    spanning-tree mode rstp
    interface range ethernet 1/1/13-1/1/14
    # Create a VLT Domain and Configure the VLT interconnect (VLTi)
    no switchport
    exit
    vlt-domain 1
    discovery-interface ethernet 1/1/13
    discovery-interface ethernet 1/1/14
    # Configure the VLT Priority, VLT MAC Address, and VLT Backup Link
    primary-priority 8192
    vlt-mac 00:11:22:33:44:55
    backup destination 192.168.1.24
    end

## Configuration of VLANs for Test

(On both devices)

    configure terminal
    interface vlan 9
    no shut
    exit
    interface ethernet 1/1/1
    switchport mode trunk
    switchport trunk allowed vlan 9
    end

On ESXi I used two separate virtual switches each with a port group. Each port group was assigned VLAN 9.

## Test Scenario

### Objective

Ping from VM1 to VM2 to show that communication will flow over the VLT and vice versa.

![](images/working.PNG)

Works as expected.

## Useful Commands

- `show vlt 1`
- `show vlt 1 mismatch`
- `show running-configuration vlt`