# Run VPN on OS10

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
3. Run `system bash`
4. `mkdir /opt/wireguard && cd /opt/wireguard`
5. Now you will either need to run all of the following as sudo or you will need to add a password to the root account with `sudo passwd` and then `su -` to become root.
6. After you have done the above run:

        echo "deb http://deb.debian.org/debian/ unstable main" > /etc/apt/sources.list.d/unstable-wireguard.list
        printf 'Package: *\nPin: release a=unstable\nPin-Priority: 90\n' > /etc/apt/preferences.d/limit-unstable
        apt update
        apt install wireguard

7. Generate key pairs `wg genkey | tee wg-private.key | wg pubkey > wg-public.key`
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
