# Setup RoCE on PowerScale

- [Setup RoCE on PowerScale](#setup-roce-on-powerscale)
  - [Verify Hardware and Software Compatibility](#verify-hardware-and-software-compatibility)
    - [PowerScale Requirements](#powerscale-requirements)
    - [R7625 Client Requirements](#r7625-client-requirements)
  - [Configure the PowerScale Cluster](#configure-the-powerscale-cluster)
    - [Enable NFS over RDMA in OneFS](#enable-nfs-over-rdma-in-onefs)
    - [Set Access Pattern on Target Directories](#set-access-pattern-on-target-directories)
    - [Disabling Deduplication for Performance Testing](#disabling-deduplication-for-performance-testing)
  - [Configure the Network](#configure-the-network)
    - [Configure MTUs](#configure-mtus)
    - [Configure IP Addresses](#configure-ip-addresses)
      - [On the Linux Side:](#on-the-linux-side)
      - [On the PowerScale Side:](#on-the-powerscale-side)
  - [Configure the Fileshare on PowerScale](#configure-the-fileshare-on-powerscale)
  - [Mount the PowerScale Export Using RDMA](#mount-the-powerscale-export-using-rdma)
    - [Make sure Correct Kernel Modules are Loaded](#make-sure-correct-kernel-modules-are-loaded)
    - [Mount](#mount)


This tutorial walks through setting up NFS over RDMA between a Dell R7625 running Linux and a PowerScale cluster running OneFS 9.2 or later.

## Verify Hardware and Software Compatibility

### PowerScale Requirements

- Must be running OneFS version 9.2 or higher
- Must have Mellanox ConnectX-3 Pro or more recent NICs. As of writing in 2025 this should be any ConnectX NIC you buy.
- RDMA must be supported on the front-end interfaces
- For this tutorial I recommend a user that has the `SystemAdmin` privilege. You can add this to a user with `isi auth roles modify SystemAdmin --add-user <user>`
  - If you want to be able to add user mappings for NFS you will need the `ISI_PRIV_AUTH` privilege. You can create a role that has it and then add it to your user with the below (as your default admin user):

      ```shell
      isi auth roles create CustomAuthRole --description "Grants ISI_PRIV_AUTH for manual ID mapping"
      isi auth roles modify CustomAuthRole --add-priv ISI_PRIV_AUTH
      isi auth roles modify CustomAuthRole --add-user <user>
      ```

Run this on PowerScale CLI:
```bash
isi network interfaces list -v
````

Look for:

```
Flags: ... SUPPORTS_RDMA_RROCE ...
```

Ex:

```shell
        IP Addresses: 10.99.99.98
                 LNN: 1
                Name: 25gige-2
            NIC Name: mce1
              Owners: groupnet0.grantsrdmasubnet.grantsrdmapool
              Status: Up
             VLAN ID: -
Default IPv4 Gateway: -
Default IPv6 Gateway: -
                 MTU: 9000
         Access Zone: System
               Flags: ACCEPT_ROUTER_ADVERT, SUPPORTS_RDMA_RRoCE
    Negotiated Speed: 25Gbps

```

### R7625 Client Requirements

* Operating System: CentOS 7.9 or RHEL 7/8/9 (known to work)
* NIC: Mellanox ConnectX-3 or higher, or ATTO FastFrame3
* BIOS settings: Set to performance mode

Check RDMA device availability:

```bash
sudo dnf install rdma-core libibverbs-utils ethtool pciutils nfs-utils -y
ibv_devinfo
```

You should see something like this:

```
[grant@aj-objsc-01 ~]$ ibv_devinfo
hca_id: irdma0
        transport:                      InfiniBand (0)
        fw_ver:                         1.72
        node_guid:                      b683:51ff:fe02:7a30
        sys_image_guid:                 b683:51ff:fe02:7a30
        vendor_id:                      0x8086
        vendor_part_id:                 5531
        hw_ver:                         0x2
        phys_port_cnt:                  1
                port:   1
                        state:                  PORT_ACTIVE (4)
                        max_mtu:                4096 (5)
                        active_mtu:             1024 (3)
                        sm_lid:                 0
                        port_lid:               1
                        port_lmc:               0x00
                        link_layer:             Ethernet

hca_id: irdma1
        transport:                      InfiniBand (0)
        fw_ver:                         1.72
        node_guid:                      b683:51ff:fe02:7a31
        sys_image_guid:                 b683:51ff:fe02:7a31
        vendor_id:                      0x8086
        vendor_part_id:                 5531
        hw_ver:                         0x2
        phys_port_cnt:                  1
                port:   1
                        state:                  PORT_ACTIVE (4)
                        max_mtu:                4096 (5)
                        active_mtu:             1024 (3)
                        sm_lid:                 0
                        port_lid:               1
                        port_lmc:               0x00
                        link_layer:             Ethernet
```

Notice, the transport is Infiniband however, the **link_layer** is Ethernet. Don't be confused by this and tell the lab manager that there are no RDMA-capable Ethernet cards in the box. Not that I would do that. This happens because the original software stack was written for Infiniband and transport is hardcoded as Infiniband.

You can also confirm by running `rdma link show`

```shell
[grant@aj-objsc-01 ~]$ rdma link show
link irdma0/1 state ACTIVE physical_state LINK_UP netdev ens6f0
link irdma1/1 state ACTIVE physical_state LINK_UP netdev ens6f1
```

## Configure the PowerScale Cluster

### Enable NFS over RDMA in OneFS

Web UI path:

```
Protocol > UNIX Sharing (NFS) > Global Settings > Enable NFS over RDMA
```

![](images/2025-05-16-13-56-16.png)

CLI equivalent:

```bash
isi nfs settings global modify --enable-rdma true
```

### Set Access Pattern on Target Directories

TODO - do I want any of this stuff

For video files:

```bash
isi filepool policies modify <policy-name> --set-access-pattern streaming
```

For image sequences:

```bash
isi filepool policies modify <policy-name> --set-access-pattern streaming
```

Enable filename-based prefetch:

```bash
isi filepool policies modify <policy-name> --enable-prefetch true
```

### Disabling Deduplication for Performance Testing

In high-throughput or latency-sensitive scenarios such as benchmarking NFS over RDMA or supporting real-time media workflows, inline deduplication can add overhead that skews performance results. To ensure accurate measurement of raw storage performance, you may want to disable deduplication.

To disable inline deduplication:

```bash
isi dedupe inline settings modify --mode disabled
```

I recommend this with workloads that are:

* Write-intensive or IOPS-bound
* Using large, unique, or pre-compressed files (e.g., video frames, genomic data)
* Focused on maximizing client-side throughput rather than storage efficiency

## Configure the Network

### Configure MTUs

On all switch ports and server NICs:

```
MTU = 9000
```

Linux side:

```bash
ip link set dev <iface> mtu 9000
```

Verify:

```bash
ip link show <iface>
```

### Configure IP Addresses

In this section, we create a **dedicated, point-to-point RDMA network link** between the Linux host and the PowerScale node using private IP addresses and a `/30` subnet. In my test scenario I hooked everything together directly to avoid complicating things with the network. Usually, you will need to work with flow control, make sure your switches can handle RDMA, etc.

This configuration assumes:

* Linux interface: `ens6f1` (adjust if using a different one)
* Linux IP: `10.99.99.97`
* PowerScale node: `node 1`, port `25gige-2`
* PowerScale IP: `10.99.99.98`
* MTU: `9000` for jumbo frames
* Subnet: `10.99.99.96/30`
* Groupnet: `groupnet0`
* Subnet name: `grantsrdmasubnet`
* Pool name: `grantsrdmapool`

Update these values as needed for your environment.

#### On the Linux Side:

```bash
# Replace 'ens6f1' with your RDMA NIC name if different
sudo nmcli connection modify ens6f1 ipv4.addresses 10.99.99.97/30
sudo nmcli connection modify ens6f1 ipv4.method manual
sudo nmcli connection modify ens6f1 ipv4.gateway ""      # no gateway for direct link
sudo nmcli connection modify ens6f1 ipv4.dns ""          # no DNS needed
sudo nmcli connection modify ens6f1 802-3-ethernet.mtu 9000

# Apply changes
sudo nmcli connection down ens6f1 && sudo nmcli connection up ens6f1

# Verify settings
ip addr show ens6f1
```

#### On the PowerScale Side:

```bash
# 1. Create a dedicated subnet (change 'grantsrdmasubnet')
isi network subnets create groupnet0.grantsrdmasubnet ipv4 30 --mtu 9000

# 2. Enable NFSv3 over RDMA globally
isi nfs settings global modify --nfsv3-rdma-enabled true

# 3. Create an RDMA-only pool with static IP (adjust node, interface, and IPs as needed)
isi network pools create groupnet0.grantsrdmasubnet.grantsrdmapool \
  --ranges 10.99.99.98-10.99.99.98 \
  --ifaces 1:25gige-2 \
  --nfsv3-rroce-only true \
  --alloc-method static \
  --description "Grant's dedicated RDMA test link"
```

## Configure the Fileshare on PowerScale

```shell
mkdir /ifs/rdma-test
chmod 755 /ifs/rdma-test
isi nfs exports create /ifs/rdma-test \
  --description "Export for R7625 RDMA testing" \
  --clients 10.99.99.97 \
  --read-write-clients 10.99.99.97 \
  --root-clients 10.99.99.97 \
  --all-dirs yes \
  --zone System
```

## Mount the PowerScale Export Using RDMA

### Make sure Correct Kernel Modules are Loaded

```bash
sudo modprobe xprtrdma
sudo modprobe rdma_ucm
sudo modprobe ib_ipoib
```

### Mount

```bash
sudo mount -t nfs -o rdma,proto=rdma,vers=3 10.99.99.98:/ifs/rdma-test /mnt/powerscale_rdma
```

**WARNING** You aren't going to be able to write anything unless the UIDs match for NFS. So whatever your UID is for your PowerScale user, that needs to match up on the Linux side. You can create a synthetic ID on Linux with:

```bash
sudo useradd -u 2010 grantcurell-mapped
sudo mkdir -p /mnt/powerscale_rdma_test
sudo mount -t nfs -o rdma,proto=rdma,vers=3 10.99.99.98:/ifs/rdma-test /mnt/powerscale_rdma_test
sudo -u grantcurell-mapped touch /mnt/powerscale_rdma_test/hello
```

This will create a user with UID 2010, mount the share, and then create a file with it. You can check your PowerScale user's ID with `isi auth users view grantcurell --zone=System`. Change the `zone` and user accordingly.

We can test if the mount is working with `sudo -u grantcurell-mapped dd if=/dev/zero of=/mnt/powerscale_rdma/testfile bs=1M count=10 oflag=direct`

```bash
[grant@aj-objsc-01 ~]$ sudo -u grantcurell-mapped dd if=/dev/zero of=/mnt/powerscale_rdma/testfile bs=1G count=100 oflag=direct
100+0 records in
100+0 records out
107374182400 bytes (107 GB, 100 GiB) copied, 96.965 s, 1.1 GB/s
```
