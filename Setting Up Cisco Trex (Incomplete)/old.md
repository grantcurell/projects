
## Optional - Install VMWare Tools

I like using VMWare tools when I have a GUI because it makes the experience a bit
smoother.

Install by doing the following:

1. `yum install -y kernel-devel`
2. Make sure your host has a CD drive
3. Mount the VMWare tools disk image in the vSphere client
4. Run `mount /dev/cdrom /mount`
5. Copy the vmware tools installation file somewhere
6. Extract it
7. Run the installer file

## Configuration of VM Networking

I used a dedicated physical interface connected directly to a virtual switch
with all security settings disabled and fed that directly into NIC2 of my packet
generator.

## Install Required Packages

    yum install -y gcc numactl-devel kernel-devel pciutils elfutils-libelf-devel make libpcap python3 tar vim wget tmux vim mlocate hwloc

Note: I didn't go through those packages to figure out exactly which ones were necessary.
Those are the packages I used to get DPDK's toolkit up and running.

## Installation of Cisco Trex

    mkdir -p /opt/trex
    cd /opt/trex
    wget --no-cache https://trex-tgn.cisco.com/trex/release/latest
    tar -xzvf latest

# Configure Cisco Trex

## Configure Interfaces

Run:

    cp  cfg/simple_cfg.yaml /etc/trex_cfg.yaml

Get a list of your available ports with:

    ./dpdk_setup_ports.py -s
    [root@trafficgenerator v2.65]# ./dpdk_setup_ports.py -s

    Network devices using DPDK-compatible driver
    ============================================
    <none>

    Network devices using kernel driver
    ===================================
    0000:04:00.0 'VMXNET3 Ethernet Controller' if=ens161 drv=vmxnet3 unused=igb_uio,vfio-pci,uio_pci_generic
    0000:0b:00.0 'VMXNET3 Ethernet Controller' if=ens192 drv=vmxnet3 unused=igb_uio,vfio-pci,uio_pci_generic *Active*
    0000:13:00.0 'VMXNET3 Ethernet Controller' if=ens224 drv=vmxnet3 unused=igb_uio,vfio-pci,uio_pci_generic
    0000:1b:00.0 'VMXNET3 Ethernet Controller' if=ens256 drv=vmxnet3 unused=igb_uio,vfio-pci,uio_pci_generic

    Other network devices
    =====================
    <none>

Since we are running Trex as a traffic generator we now need to add a dummy interface.
Dummy interfaces in Trex can solve two problems:

    Odd number of interfaces. For example, TRex with only one interface.
    Performance degradation when adjacent interfaces belong to different NUMAs.


You can tailor the basic configuration file to your need by running:

    ./dpdk_setup_ports.py -i

Alternatively you can edit the configuration file yourself with:

    vim /etc/trex_cfg.yaml

There is also a command line mode of the script you can run with -t.

## Configure Threads

I find the script [cpu_layout.py](./cpu_layout.py) from the DPDK toolkit helpful
here. It will give you an exact layout of the cpu cores. In the config file at `/etc/trex_cfg.yaml`
you can adjust what cores the code will run on.