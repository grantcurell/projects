
## Set up the Manager and Discovery

1. `vxrail-primary --setup --vxrail-address 192.168.2.100  --vxrail-netmask 255.255.255.0 --vxrail-gateway 192.168.2.1`

- According to [David Ring](https://davidring.ie/2019/11/13/vxrail-4-7-ipv6-node-discovery-test/):

        Loudmouth requires IPv6 multicast in order for VxRail Manager to perform a successful VxRail node discovery. IPv6 multicast is required only on the ‘Private Management Network’, this is an isolated management network solely for auto-discovery of the VxRail nodes during install or expansion. The default VLAN ID for the private network is 3939, which is configured on each VxRail node from the factory, this VLAN needs to be configured on the TOR switches and remains isolated on the TORs. If you wish to deviate from the default of VLAN 3939 then each node will need to be modified onsite otherwise node discovery will fail.
- You should have 5 networks total:
  - vmx0 is tied to Private Management Network which is tied to VLAN 3939. This is required for discovery. If you want to be able to externally reach the VMs you will want to configure management on vmk2 or some other interface.

![](2020-12-15-13-42-40.png)

- 

## Helpful Commands

### Set the IPv4 Address of a VMK interface

`esxcli network ip interface ipv4 set --interface-name vmk0 --type=dhcp`

### Check if VXRail is Running

`esxcli vm process list`

### Get a List of VMs

`vim-cmd vmsvc/getallvms`

### Check if VM is On

`vim-cmd vmsvc/power.getstate 1`

### Check Networking

`esxcli network vswitch standard portgroup list`

### Set the VLAN for a Switch

`esxcli network vswitch standard portgroup set -p "VM Network" -v 120`

### Get Interface IPs

`esxcli network ip interface ipv4 get`

### Get Interface List

`esxcli network ip interface list`

### Get the IPv6 Address of an ESXi Interface

`esxcfg-vmknic -l | grep vmk0`