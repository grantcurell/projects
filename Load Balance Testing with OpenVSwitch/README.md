# Load Balance Testing with OpenVSwitch

From tutorial [ovs-conntrack](http://docs.openvswitch.org/en/latest/tutorials/ovs-conntrack/)

Testing performed on OS10 v 

## Setup

    ip netns add left
    ip netns add right
    ip link add veth_l0 type veth peer name veth_l1
    ip link set veth_l1 netns left
    ip link add veth_r0 type veth peer name veth_r1
    ip link set veth_r1 netns right
    ovs-vsctl add-br br0
    ip a s | less
    ovs-vsctl add-port br0 veth_l0
    ovs-vsctl add-port br0 veth_r0
    ip netns exec left sudo ip link set lo up
    ip netns exec right sudo ip link set lo up

## Generate TCP segments

    ip netns exec left sudo `which scapy`
    ip netns exec right sudo `which scapy`

## Matching TCP packets

### Simple flows for port to port

    ovs-ofctl add-flow br0 "table=0, priority=10, in_port=veth_l0, actions=veth_r0"
    ovs-ofctl add-flow br0 "table=0, priority=10, in_port=veth_r0, actions=veth_l0"

### Flow matching

    ovs-ofctl add-flow br0 "table=0, priority=50, ct_state=-trk, tcp, in_port=veth_l0, actions=ct(table=0)"
    ovs-ofctl add-flow br0 "table=0, priority=50, ct_state=+trk+new, tcp, in_port=veth_l0, actions=ct(commit),veth_r0"
    ovs-ofctl add-flow br0 "table=0, priority=50, ct_state=-trk, tcp, in_port=veth_r0, actions=ct(table=0)"
    ovs-ofctl add-flow br0 "table=0, priority=50, ct_state=+trk+est, tcp, in_port=veth_r0, actions=veth_l0"
    ovs-ofctl add-flow br0 "table=0, priority=50, ct_state=+trk+est, tcp, in_port=veth_l0, actions=veth_r0"

## End result

You can do cool stuff, but it won't work/wouldn't be a great way to do this.