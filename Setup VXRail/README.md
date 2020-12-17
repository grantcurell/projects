# VXRail Setup

## Networking

I followed [the vCenter Server Planning Guide](https://www.delltechnologies.com/resources/en-us/asset/technical-guides-support-information/products/converged-infrastructure/vxrail-vcenter-server-planning-guide.pdf) to set up the network.

**WARNING**: The discovery process for VXRail uses IPv6 multicast to discover itself. Dell switches come with MLD snooping globally enabled, but **do not** have the MLD querier enabled! This will cause the nodes to flap! Servers will discover themselves and then disappear. You must enable MLD snooping **and** the mld querier on the correct vlans with `interface vlan #` and then `ipv6 mld snooping querier`.

### What does MLD Querying Do and Why Can it Break VXRail Discovery

By default, switches are not multicast aware so they will broadcast any multicast traffic on all ports assigned to a VLAN.

For bandwidth optimization the switch will block any multicast messages to a segment it thinks does not have a device which wants those multicast messages. It discovers if there is an interested host by using MLD general queries or group specific queries. Enabling the querier will allow the switch to use these messages to discover interested hosts and subsequently ensure those hosts receive the appropriate IPv6 messages.

## RASR Process

There is an IDSDM module on the box with the factor image on the box. To perform the RASR process you'll boot from that and it will copy over all necessary files to the internal BOSS drive. Just follow the prompts.

**WARNING** RASRing a node blows away absolutely everything on all drives! **DO NOT RUN ON A PRODUCTION CLUSTER**

## Set up the Manager for Discovery

- [David Ring's Install Notes](https://davidring.ie/2019/06/10/vxrail-4-7-install-notes/) are helpful
- [David Ring's notes](https://davidring.ie/2019/11/13/vxrail-4-7-ipv6-node-discovery-test/) on how host discovery works are also helpful

        Loudmouth requires IPv6 multicast in order for VxRail Manager to perform a successful VxRail node discovery. IPv6 multicast is required only on the ‘Private Management Network’, this is an isolated management network solely for auto-discovery of the VxRail nodes during install or expansion. The default VLAN ID for the private network is 3939, which is configured on each VxRail node from the factory, this VLAN needs to be configured on the TOR switches and remains isolated on the TORs. If you wish to deviate from the default of VLAN 3939 then each node will need to be modified onsite otherwise node discovery will fail.

1. Turn on the VXRail manager. `vxrail-primary --setup --vxrail-address 192.168.2.100  --vxrail-netmask 255.255.255.0 --vxrail-gateway 192.168.2.1`. The IP you assign is **not** used for discovery. It is for reaching the VXRail appliance. Give it an IP on whatever network/vlan you plan on using for management. Details below in step 3.
   1. Make sure vmk0 of all ESXi hosts is on VLAN 3939 or whatever VLAN you're using for discovery.
   2. On each ESXi host make sure *Private Management Network* and *Private VM Network* are both on VLAN 3939.

    ![](images/2020-12-15-13-42-40.png)

   3. The VXRail manager has two virtual NICs - eth0 and eth1. Eth1 is the NIC used for discovery. Make sure eth1 of the VXRail manager is on VLAN 3939. The first NIC (eth0) should be on whatever VLAN you are using for management. You will get to the VXRail manager webgui through eth0.
2. At this point you should have full IPv6 connectivity between vmk0 on all ESXi instances and the VXRail appliance. You can test this with the following:
   1. Go to the ESXi console, press ALT+F1 and Pull the IPv6 address for vmk0 on ESXi with: `esxcfg-vmknic -l | grep vmk0`
   2. On the ESXi host with the VXRail appliance, give another (not vmk0) VM kernel NIC you have access to an IP address with the `esxcli network ip interface ipv4 set` command. For dhcp use the `--type dhcp` option. See [Helpful Commands](#helpful-commands) for how to list out the different portgroups and VMs
   3. Once you know all the IPv6 addresses for the various vmk0 nics, get on the VXRail appliance and use `ping6 -l eth1 <ipv6 address>` to test your IPv6 ping. This should work against all devices. If it doesn't you probably have a networking problem.
   4. You can also test the full server discovery process manually from the command line with:

      ![](images/2020-12-16-09-13-40.png)

   5. For further troubleshooting check the Marvin log

## Install



## Helpful Commands

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
