# Site to Site VPN with PFSense and CentOS 8

## On PFSense

1. Go to openvpn server creation
2. Select UDP on IPv4 only with tun
3. Use a Peer to Peer (Shared Key)
4. For the shared key automatically generate it

No other special settings required.

After you create the server, save it, and then go back in and copy the shared key.

1. Open port 1194 UDP on the firewall.

## On CentOS 8

1. Make sure everything is up to date. `yum update -y && reboot`. The reboot is important because if your kernel might update. If this happens you need to reboot to load the new kernel.
2. Run `yum install -y epel-release && yum update -y && yum install -y openvpn easy-rsa chrony && systemctl enable chronyd && chronyc makestep` This is a long series of commands, but it installs openvpn and chrony. You need chrony to ensure your time is synched. **WARNING**: If the time is not synched between the server and your clients, the VPN will fail to connect!
3. `systemctl stop firewalld` - otherwise you'll have to allow everything going to and from the networks on a case by case basis.
4. Run `sysctl -w net.ipv4.ip_forward=1 && echo 1 > /proc/sys/net/ipv4/ip_forward`
5. Use the following config file:

    dev ovpnc3
    verb 6
    dev-type tun
    #dev-node /dev/tun3
    writepid /var/run/openvpn_client3.pid
    #user nobody
    #group nobody
    script-security 3
    keepalive 10 60
    ping-timer-rem
    persist-tun
    persist-key
    proto udp4
    cipher AES-128-CBC
    auth SHA256
    local <YOUR LOCAL CLIENT INTERFACE IP>
    lport 0
    management /etc/openvpn/client3.sock unix
    remote <REMOTE TARGET IP> 1194 udp4
    ifconfig <Tunnel interface IP for client> <Tunnel interface IP for server>
    route <ROUTE FOR REMOTE NETWORK - EX 192.168.1.0> <SUBNET MASK>
    compress
    resolv-retry infinite
    secret /etc/openvpn/client/secret <TODO UPDATE THIS FILE WITH THE KEY>

In my scenario the 192.168.2.0/24 was the remote site network and 192.168.1.1 was the local network.