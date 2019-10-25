# Multiple Mirror Port Test

In this test case I am testing to see if we can configure a Dell 4112F-ON with
OpenSwitch to create a one to many port configuration using SPAN.

# Helpful Links

[ONIE Network Install Process Overview](https://opencomputeproject.github.io/onie/user-guide/index.html#installing-over-the-network)

[OPX Install Instructions for Dell EMC Equipment](https://github.com/open-switch/opx-docs/wiki/Install-OPX-on-Dell-EMC-ON-series-platforms)

[OPX Tools Source Code](https://github.com/open-switch/opx-tools)

[OPX Command Reference](https://github.com/open-switch/opx-docs/wiki/OPX-commands)

[OPX Docs Home](https://github.com/open-switch/opx-docs/wiki)

[List of Supported Hardware](https://github.com/open-switch/opx-docs/wiki/hardware-support)

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

## OPX Version

    OS_NAME="OPX"
    OS_VERSION="unstable"
    PLATFORM="S4112F-ON"
    ARCHITECTURE="x86_64"
    INTERNAL_BUILD_ID="OpenSwitch blueprint for Dell 1.0.0"
    BUILD_VERSION="unstable.0-stretch"
    BUILD_DATE="2019-06-21T19:04:22+0000"
    INSTALL_DATE="2019-10-23T23:16:10+00:00"
    SYSTEM_UPTIME= 1 day, 5 minutes
    SYSTEM_STATE= running
    UPGRADED_PACKAGES=no
    ALTERED_PACKAGES=yes

Wasn't sure why I got the unstable version after installation. It didn't cause any
problems for testing so I just left it as is.

## Physical Configuration

![](images/switch.jpg)

I didn't have enough target hosts to try outputting from one port to all ports so
I simulated it. The purple cable in the image is the input port from the traffic
generator (tcpreplay) and the white and yellow cables go out to the hosts listed
as host 1 and host 2 in the test results section. The ports with the white and yellow
cables were configured as mirror ports.

# Setup ONIE Prerequisites

I ran the network version of the ONIE installation using a web server. Below
is what I did to get things installed. We will host the OS installer on our
web server and then we will use ONIE to grab it. We will use a DNS record to 
control the ONIE server location.

1. Install Apache on RHEL or your favorite Linux distro.
2. Make sure you allow HTTP traffic through the firewall
3. Download Open Switch [here](http://archive.openswitch.net/).
4. Upload `PKGS_OPX-3.2.0-installer-x86_64.bin` to the root of your web server.
5. Create a symlink to the installer with `ln -s PKGS_OPX-3.2.0-installer-x86_64.bin onie-installer`. The file must have this name for the installation to work.
6. The switch will use DHCP to acquire an IP address. On the DNS server pointed to by your DHCP configuration, add a record for onie-server and point it at the host running Apache.

On a test box, run a DHCP request, ensure you pull the correct DNS server and that the host can resolve `onie-server`. After you confirm DNS is working, browse to the onie-installer file
on your Apache server and make sure you can download it without issue.

**Warning:** It must be able to resolve the hostname onie-server with the FQDN.
If `onie-server` is not immediately resolvable, the install process will not work.

# ONIE Boot the Switch

1. Connect to the switch over the console port. My configuration was:

        Baud Rate: 115200
        Data Bits: 8
        Stop Bits: 1
        Parity: None
        Flow Control: None

2. Connect the ethernet management port of the switch to the same network containing your web server. ONIE will use the management port to establish a connection to the ONIE server.
3. Once the grub menu appears, select ONIE Installer. In my case this was the top option.
4. At this point the ONIE discovery process will commence. It will print each location it attempts to search. It should find the onie-server DNS record and the installation should begin automatically. If this doesn't happen it means there is an issue with the preconfiguration above. Try swapping out the ethernet management cable with a host. Make sure that host pulls DNS/DHCP correctly and is able to download the onie-installer file.
5. Wait for the installation to finish and the switch to reboot. Login with admin/admin.

# Configure Management Interface

1. Start by running `sudo -i` to move to privileged mode. **Warning:**  I noticed the OPX command line tools won't behave correctly unless you are privileged. Ex: `opx-show-interface` won't list any interfaces.
2. I added vim to my box before continuing with `sudo apt-get install -y vim`
3. The management interface is configured like a typicaly Debian interface with `vim /etc/network/interface.d/eth0`
4. Use the following configuration modified to your needs:

        auto eth0
        allow-hotplug eth0
        iface eth0 inet static
            address 192.168.1.20
            netmask 255.255.255.0
            gateway 192.168.1.1

5. When you are finished with your configuration run `systemctl restart networking` to apply the changes.
6. Confirm the changes were applied with `ip address show dev eth0`. If you see two IP addresses because you picked one up from DHCP you can delete the other with `ip address del [IP ADDRESS] dev eth0` and then run `systemctl restart networking`

At this juncture your management interface should be up and running and you should
be able to SSH to it. I went ahead and swapped to SSH so as not to deal with the
oddities that come with running in the console port.

# My Testing

## Attempt 1 - Mirror Ports

For each port you want to mirror to run `opx-config-mirror create --src_intf e101-001-0 --dest_intf e101-005-0 --direction ingress --type span`. Substitute your source and destination ports appropriately.

### Results

#### Mirror Port Failure After 5

I was only able to get this to work on up to 5 ports. After that I received errors.
See output below:

    root@OPX:~# opx-config-mirror create --src_intf e101-001-0 --dest_intf e101-005-0 --direction ingress --type span
    root@OPX:~# ip link set e101-009-0 up
    root@OPX:~# opx-config-mirror create --src_intf e101-001-0 --dest_intf e101-009-0 --direction ingress --type span
    root@OPX:~# opx-config-mirror create --src_intf e101-001-0 --dest_intf e101-002-0 --direction ingress --type span
    root@OPX:~# opx-config-mirror create --src_intf e101-001-0 --dest_intf e101-003-0 --direction ingress --type span
    root@OPX:~# opx-config-mirror create --src_intf e101-001-0 --dest_intf e101-004-0 --direction ingress --type span
    {'data': {'base-mirror/entry/dst-intf': bytearray(b'\x0f\x00\x00\x00'), 'base-mirror/entry/type': bytearray(b'\x01\x00\x00\x00'), 'base-mirror/entry/intf': {'0': {'base-mirror/entry/intf/src': bytearray(b'\x0c\x00\x00\x00'), 'base-mirror/entry/intf/direction': bytearray(b'\x01\x00\x00\x00')}}}, 'key': '1.27.1769488.1769473.'}
    opx-config-mirror: Commit failed
    root@OPX:~# opx-config-mirror create --src_intf e101-001-0 --dest_intf e101-006-0 --direction ingress --type span
    {'data': {'base-mirror/entry/dst-intf': bytearray(b'\x11\x00\x00\x00'), 'base-mirror/entry/type': bytearray(b'\x01\x00\x00\x00'), 'base-mirror/entry/intf': {'0': {'base-mirror/entry/intf/src': bytearray(b'\x0c\x00\x00\x00'), 'base-mirror/entry/intf/direction': bytearray(b'\x01\x00\x00\x00')}}}, 'key': '1.27.1769488.1769473.'}
    opx-config-mirror: Commit failed
    root@OPX:~# opx-config-mirror create --src_intf e101-001-0 --dest_intf e101-007-0 --direction ingress --type span
    {'data': {'base-mirror/entry/dst-intf': bytearray(b'\x12\x00\x00\x00'), 'base-mirror/entry/type': bytearray(b'\x01\x00\x00\x00'), 'base-mirror/entry/intf': {'0': {'base-mirror/entry/intf/src': bytearray(b'\x0c\x00\x00\x00'), 'base-mirror/entry/intf/direction': bytearray(b'\x01\x00\x00\x00')}}}, 'key': '1.27.1769488.1769473.'}
    opx-config-mirror: Commit failed

#### Functioning Mirror Ports

Before I caught the error, I did test the first two mirror ports I made and they
worked as expected. See the below.

I used tcpreplay with some traffic I captured on my desktop to test the idea. I
just uploaded the PCAP and replayed it with `tcpreplay -i ens224 ./test_pcap.pcap --loop 500`

I then confirmed that all target ports received traffic. See screenshots below:

### Host 1
![](images/host1.png)

### Host 2
![](images/host2.png)

The host I collected the traffic on was 192.168.1.6 and as you can see from the 
images both hosts were able to see traffic from the tcpreplay session.