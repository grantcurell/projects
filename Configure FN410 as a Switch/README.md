# Configure FN410 as a Switch

## Scenario

### Overview

You are running a TFX2, you have an FN410, and that FN410 is connected back to some sort of top of rack switch.
In my case I am using an 4112F-ON.

In our scenario, we want to create a LAG between the Top of Rack (TOR) switch and two of the front ports of the FN410.
On the back of the FN410, connected to the blades, you will have a trunk going to an ESXi server.

### Ports

The ports are configured in the following way:

#### 4112F-ON

      ethernet 1/1/1 - port 1 of LAG
      ethernet 1/1/2 - port 2 of LAG
      port-channel 128 - LAG port

In my setup ethernet 1/1/9 went to the CMC and ethernet 1/1/12 went to the rest of my network. There were not other
relevant ports.

#### FN410

      tengigabitethernet 0/9 - port 1 of LAG
      tengigabitethernet 0/10 - port 2 of LAG
      tengigabitethernet 0/1 - port 1 going to ESXi
      tengigabitethernet 0/2 - port 2 going to ESXi

## Useful Notes

### How the FN410 Management Interface Works

From [the manual](https://topics-cdn.dell.com/pdf/poweredge-fx2_users-guide6_en-us.pdf)

The IOM management interface has both a public IP and private IP address on the internal fabric D interface.
The public IP address is exposed to the outside world for Web GUI configurations/WSMAN and other proprietary traffic. You can statically
configure the public IP address or obtain the IP address dynamically using the dynamic host configuration protocol (DHCP).

#### What is a fabric?

A fabric is just a series of electrical connections that in this case make up a L2 switching domain.

Fabric D is the internal management fabric. The CMC basically acts as a switch on this fabric and all of the chassis
management related services are connected to it - idrac, CMC, and FN410 management functions.

## Example Configs

[4112F-ON Example Configuration](./4112F-ON_config.txt)

[FN410 Example Configuration](./FN410_config.txt)

***For the keen eyed*** I was too lazy to remove the password hashes. Spoiler it's admin/admin on the 4112 and root/calvin on the FN410.

## Configuring the FN410

### Configure FN410 as a Switch via GUI

1. Go to CMC -> Click *I/O Module Overview*
2. Click on your FN410
3. Go to setup and configure networking. The address you sit here is tied to the CMC's physical port. That is to say, you do not need to be plugged into the FN410 to reach this address. It should be on the same subnet and VLAN as the CMC.
4. Click *Launch I/O Module GUI*
      1. Once in the GUI, in mode settings, select *Full Switch Mode*
      2. Set your network settings as needed
      3. Credentials set as needed
      4. SNMP set as needed
      5. Disable Uplink Failure Detection
      6. On time I set my time zone and used *216.239.35.0* (Google's time servers - the zero isn't a type-o)
      7. At the end you will be asked to reboot. Say yes. A window will appear that says rebooting. Wait for it to go away. At the end the page will refresh and you will  get an error message on the web site saying it isn't available. This is because you put it in switch mode. This process took ~3 minutes for me.

### Configure FN410 as a Swich via Command Line

From [the manual](https://topics-cdn.dell.com/pdf/poweredge-fx2_users-guide6_en-us.pdf)

You can connect to the FN410 using one of the following:

Internal RS-232 using the chassis management controller (CMC). Telnet into CMC and do a `connect -b switch-id` to get
console access to corresponding IOM.

- External serial port with a universal serial bus (USB) connector (front panel): connect using the IOM front panel USB serial line to get
console access (Labeled as USB B).
- Telnet/others using the public IP interface on the fabric D interface.
- CMC through the private IP interface on the fabric D interface.

You will need to connect through the CMC:

1. SSH to the CMC's IP address. Use the CMC username/password to log in.
2. Run the command `connect -m switch-1` to connect to the switch.
3. My switch was in BMP mode. I had to hit `A` to cancel it.
4. Run `stack-unit 0 iom-mode full-switch` to change the switch to full switch mode
5. Run `write mem` and reboot the IOM

### Configuring Switch Management

You may have already done this in the GUI, but if not, you can do the following:

#### Configure Default Route

      management route 0.0.0.0/0 192.168.1.1

#### Configure NTP

      ntp server 216.239.35.0

#### Configure Management IP Address

      Dell(conf)#interface managementethernet 0/0
      Dell(conf-if-ma-0/0)#ip address 192.168.1.114/24

#### Configure SNMP

      snmp-server community public ro
      snmp-server enable traps snmp linkdown linkup
      snmp-server enable traps stack

### Upgrading the firmware

You can download the firmware from the [force10 website](https://www.force10networks.com/CSPortal20/Software/MSeriesDownloads.aspx)

1. Upgrade the Dell Networking OS in flash partition A: or B:. Run `upgrade system tftp://10.16.127.149/dell-FN-B B:`
2. Verify that the Dell Networking OS has been upgraded correctly in the upgraded flash partition. `show boot system stack-unit [0-5 | all]`
3. Upgrade the FN I/O Module Boot Flash and Boot Selector image (if needed).

            upgrade boot [all | bootflash-image | bootselector-image] stack-unit [0-5 | all] [booted |
            flash: | ftp: | scp: | tftp: | usbflash:] [A: | B:]

4. Change the Primary Boot Parameter of the FN I/O Module to the upgraded partition A: or B:. `boot system stack-unit [0-5 | all] primary [system A: | system B: | tftp://]`
5. Save the config: `write memory`.
6. Reload the switch so the config takes effect. `reload`
7. After boot, use `show version` and `show system stack-unit [0-5]` to check that versions have updated correctly.
   
### Configure Interfaces

1. Begin by configuring the port-channel interface:
      1. Note: Hybrid mode allows the interface to pass tagged and untagged traffic.

               Dell(conf)#interface port-channel 128
               Dell(conf-if-po-128)#portmode hybrid
               Dell(conf-if-po-128)#switchport
               Dell(conf-if-po-128)#no shutdown

2. Next you need to configure the individual interfaces:

             Dell(conf)#interface range tengigabitethernet 0/9-10
             Dell(conf-if-range-te-0/9-10)#port-channel-protocol LACP
             Dell(conf-if-range-te-0/9-10-lacp)#port-channel 128 mode active

3. Now you need to configure any VLANs you want to run:

            Dell(conf)#interface range vlan 32-37
            Dell(conf-if-range-vl-32-37)#tagged tengigabitethernet 0/1-2
            Dell(conf-if-range-vl-32-37)#tagged tengigabitethernet 0/12

4. If desired at this point you can enter into each VLAN interface and run the `ip address` command to give it an IP address.
5. Run `write memory`

## Configure 4112F-ON

1. Log into the 4112F-ON via its management interfaces. Move to configuration mode.
2. Next, configure the port channel interface:

            OS10(config)# interface port-channel 128
            OS10(conf-if-po-128)# switchport mode trunk
            OS10(conf-if-po-128)# no switchport access vlan
            OS10(conf-if-po-128)# switchport trunk allowed vlan 32
            OS10(conf-if-po-128)# no shutdown

3. Now configure the interfaces to join the port channel.

            OS10(config)# interface range ethernet 1/1/1-1/1/2
            OS10(conf-range-eth1/1/1-1/1/2)# channel-group 128 mode active
            OS10(conf-range-eth1/1/1-1/1/2)# no switchport
            OS10(conf-range-eth1/1/1-1/1/2)# switchport mode trunk

4. Run `write memory`

## Troubleshooting

### VLANs

#### On 4112F-ON

Make sure the VLANs using are all shown as active on the correct ports:

            OS10# show vlan
            Codes: * - Default VLAN, M - Management VLAN, R - Remote Port Mirroring VLANs,
                   @ – Attached to Virtual Network
            Q: A - Access (Untagged), T - Tagged
            NUM    Status    Description                     Q Ports
          * 1      Inactive                                  A Eth1/1/4-1/1/8,1/1/10,1/1/13-1/1/15
            32     Active                                    T Eth1/1/11
                                                             T Po128
                                                             A Eth1/1/9,1/1/12

##### On FN410

            Dell#show vlan

            Codes: * - Default VLAN, G - GVRP VLANs, R - Remote Port Mirroring VLANs, P - Primary, C - Community, I - Isolated
                  O - Openflow, Vx - Vxlan
            Q: U - Untagged, T - Tagged
            x - Dot1x untagged, X - Dot1x tagged
            o - OpenFlow untagged, O - OpenFlow tagged
            G - GVRP tagged, M - Vlan-stack, H - VSN tagged
            i - Internal untagged, I - Internal tagged, v - VLT untagged, V - VLT tagged

            NUM    Status    Description                     Q Ports
         *  1      Active                                    U Po128(Te 0/9-10)
                                                             U Te 0/1-2,12
            32     Active                                    T Po128(Te 0/9-10)
                                                             T Te 0/1-2,12
