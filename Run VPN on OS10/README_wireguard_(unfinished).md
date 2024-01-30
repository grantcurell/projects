# Run VPN on OS10

## My Configuration

### Dell 4112F-ON

        Dell EMC Networking OS10 Enterprise
        Copyright (c) 1999-2020 by Dell Inc. All Rights Reserved.
        OS Version: 10.5.0.4
        Build Version: 10.5.0.4.638
        Build Time: 2020-01-30T21:08:56+0000
        System Type: S4112F-ON
        Architecture: x86_64
        Up Time: 2 days 03:54:07

### CentOS

        [root@centos ~]# cat /etc/*-release
        CentOS Linux release 7.6.1810 (Core)
        NAME="CentOS Linux"
        VERSION="7 (Core)"
        ID="centos"
        ID_LIKE="rhel fedora"
        VERSION_ID="7"
        PRETTY_NAME="CentOS Linux 7 (Core)"
        ANSI_COLOR="0;31"
        CPE_NAME="cpe:/o:centos:centos:7"
        HOME_URL="https://www.centos.org/"
        BUG_REPORT_URL="https://bugs.centos.org/"

        CENTOS_MANTISBT_PROJECT="CentOS-7"
        CENTOS_MANTISBT_PROJECT_VERSION="7"
        REDHAT_SUPPORT_PRODUCT="centos"
        REDHAT_SUPPORT_PRODUCT_VERSION="7"

        CentOS Linux release 7.6.1810 (Core)
        CentOS Linux release 7.6.1810 (Core)

### Physical Configuration

Interface `ethernet 1/1/12` on the 4112F-ON plugged directly into a server running ESXi. That interface was assigned as an uplink associated with a vswitch when then was tied to a portgroup running on VLAN 32. `ethernet 1/1/12` was configured as follows:

        OS10(conf-if-eth1/1/12)# show configuration
        !
        interface ethernet1/1/12
        no shutdown
        switchport mode trunk
        switchport access vlan 1
        switchport trunk allowed vlan 32
        flowcontrol receive on

`interface vlan 32` was configured as follows:

        OS10(conf-if-vl-32)# show configuration

        !
        interface vlan32
        no shutdown
        ip address 192.168.32.1/24

The full switch config [is here](TODO ADD SWITCH CONFIG)

Interface `ethernet 1/1/1` was configured as an access port in VLAN <TODO>

## Research 

### Sources

[Helpful Book](http://www.cse.bgu.ac.il/npbook/)
[Basics of Network Processor](https://www.embedded.com/the-basics-of-network-processors/)
[Packet Processing](https://en.wikipedia.org/wiki/Packet_processing)
[How Network Processors Work](https://barrgroup.com/embedded-systems/how-to/network-processors)

### NPU Problem

Explanation

## Installing WireGuard

On the 4112F-ON:

1. Enter configuration mode from user mode by running `en` and then `config <enter>`
2. Run `ip name-server 192.168.1.1` to add a name server.
3. Run `write mem` in enable mode to save your configuration changes.
4. Run `system bash`
5. If you don't have a default route on your switch, you will need to add one with `sudo ip route add 0.0.0.0/0 via 192.168.1.1`.
6. Before installing WireGuard you will need the latest kernel headers.
      1.The kernel headers on the system will work a bit differently than regular systems. I found the relevant kernel headers with `apt search linux-headers | grep $(uname -r)`
      2.You should see an entry mentioning all - something like `linux-headers-4.9.0-11-all`. You want to install that package with `sudo apt-get install -y <LINUX HEADER NAME> bc`
      3.At this point you will need to reboot. Do this by exiting the command line and in enable mode running `reload`
      4.If you do not have a permanent default route set, when you log back in you will need to run `system bash` and then readd the default route with `sudo ip route add 0.0.0.0/0 via 192.168.1.1`
7. `mkdir /opt/wireguard && cd /opt/wireguard`
8. Now you will either need to run all of the following as sudo or you will need to add a password to the root account with `sudo passwd` and then `su -` to become root.
9. After you have done the above run:

        echo "deb http://deb.debian.org/debian/ unstable main" > /etc/apt/sources.list.d/unstable-wireguard.list
        printf 'Package: *\nPin: release a=unstable\nPin-Priority: 90\n' > /etc/apt/preferences.d/limit-unstable
        apt update
        apt install wireguard

10. Generate key pairs `wg genkey | tee wg-private.key | wg pubkey > wg-public.key`
11. 

On CentOS 7

1. Make sure everything is up to date. `yum update -y && reboot`. The reboot is important because if your kernel might update. If this happens you need to reboot to load the new kernel. Wireguard requires kernel 3.10 or higher - I noticed if you haven't updated CentOS for a bit than your kernel might be to old and you'll get `RTNETLINK answers: Operation not supported`.
2. Run:

                sudo yum install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm
                sudo curl -o /etc/yum.repos.d/jdoss-wireguard-epel-7.repo https://copr.fedorainfracloud.org/coprs/jdoss/wireguard/repo/epel-7/jdoss-wireguard-epel-7.repo
                sudo yum install wireguard-dkms wireguard-tools

3. `mkdir /opt/wireguard && cd /opt/wireguard`
4. Generate key pairs `wg genkey | tee wg-private.key | wg pubkey > wg-public.key`
5. `ip link add wg0 type wireguard`
6. Set Wireguard interface IP `ip address add dev wg0 10.0.0.2/24`. This IP address is the tunnel IP address.
      1.If there are only two peers together you can do something like `ip address add dev wg0 10.0.0.2 peer 10.0.0.1`
7. wg set wg0 listen-port 51820 private-key /opt/wireguard/wg-private.key peer OQiSLUOd3YWCfEkHazJHuuaJVNc++8QOb2+sOOZl/2c= endpoint 192.168.32.1:8172
      1.listen-port: the port this host will listen on
      2.private-key: the private key for this host
      3.peer: I thought this was a bit misleading - you want the public key of the other host to which you are connecting
      4.endpoint: the other endpoint of the VPN and the port on which it is listening
8. 

## Strange Behavior

    OS10(config)# management route 192.168.1.0/24 192.168.1.1
    % Error: Overlapping route for Management interface
    OS10(config)# ip route 0.0.0.0/0 192.168.1.1 interface ethernet 1/1/1
    % Error: Network unreachable
    OS10(config)# ping 192.168.1.1
    PING 192.168.1.1 (192.168.1.1) 56(84) bytes of data.
    64 bytes from 192.168.1.1: icmp_seq=1 ttl=64 time=0.452 ms
    64 bytes from 192.168.1.1: icmp_seq=2 ttl=64 time=0.388 ms
    ^C
    --- 192.168.1.1 ping statistics ---
    2 packets transmitted, 2 received, 0% packet loss, time 1005ms
    rtt min/avg/max/mdev = 0.388/0.420/0.452/0.032 ms
    OS10(config)# do system bash
    admin@OS10:~$ su -
    Password:
    root@OS10:~# ip route
    192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.20
    192.168.4.0/24 dev br32 proto none scope link
    root@OS10:~# ip route add 0.0.0.0/0 via 192.168.1.1
    root@OS10:~# ip route
    default via 192.168.1.1 dev eth0
    192.168.1.0/24 dev eth0 proto kernel scope link src 192.168.1.20
    192.168.4.0/24 dev br32 proto none scope link
    root@OS10:~# ping google.com
    PING google.com (216.58.193.142) 56(84) bytes of data.
    64 bytes from dfw25s34-in-f14.1e100.net (216.58.193.142): icmp_seq=1 ttl=55 time=25.4 ms
    64 bytes from dfw25s34-in-f14.1e100.net (216.58.193.142): icmp_seq=2 ttl=55 time=22.9 ms
    64 bytes from dfw25s34-in-f14.1e100.net (216.58.193.142): icmp_seq=3 ttl=55 time=22.1 ms
    64 bytes from dfw25s34-in-f14.1e100.net (216.58.193.142): icmp_seq=4 ttl=55 time=22.2 ms
    ^C
    --- google.com ping statistics ---
    4 packets transmitted, 4 received, 0% packet loss, time 3002ms
    rtt min/avg/max/mdev = 22.149/23.185/25.408/1.329 ms
