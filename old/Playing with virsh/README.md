# Playing with virsh

## VMs

List all VMs
    virsh list --all

## Network Stuff

Get network info 
    virsh net-info <NETWORK>

Dump network info

    virsh net-dumpxml xhubnet

List all networks
    virsh net-list --all

## IPables

Heads up, `iptables -L` does not truly list all the rules. It just lists the rules
in the current table.

If you want to see the NAT rules you can run:
    iptables -t nat -L

Heads up, `iptables` will by default try to resolve names. To skip this do:
    iptables -t nat -vnL

Adding a destination NAT rule:
    iptables -t nat -A PREROUTING -p tcp --dport 8000 -j DNAT --to 10.125.120.21

Delete a rule from iptables:
    iptables -t nat -D POSTROUTING -p tcp --dport 50000 -j SNAT --to 5.136.13.37

