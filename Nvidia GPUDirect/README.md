# Nvidia GPUDirect

- [Nvidia GPUDirect](#nvidia-gpudirect)
  - [Background Research](#background-research)
  - [Helpful Links](#helpful-links)
  - [Source Code](#source-code)
  - [Description of the Problem](#description-of-the-problem)
  - [Lab Configuration](#lab-configuration)
    - [Hardware Configuration](#hardware-configuration)
    - [RHEL Version](#rhel-version)
    - [GCC Version](#gcc-version)
    - [Nvidia SMI](#nvidia-smi)
    - [CUDA Version](#cuda-version)
  - [Setting Up the Code Environment](#setting-up-the-code-environment)
    - [CUDA Development Packages](#cuda-development-packages)
    - [Prepare the Code](#prepare-the-code)
    - [Compiling and Running the App](#compiling-and-running-the-app)
  - [Debugging](#debugging)

## Background Research

See [Background Research](./background_research.md) for background information I studied before doing this.

## Helpful Links

[RDMA Aware Programming](https://docs.mellanox.com/display/RDMAAwareProgrammingv17/Key+Concepts)
[Typical Application Flow](https://docs.mellanox.com/display/RDMAAwareProgrammingv17/Typical+Application)

## Source Code

See [the test file](test_code/rdma-loopback.cpp)

## Description of the Problem

What we are doing in the below steps is playing a packet from one Mellanox card directly into another. Before playing the packet, we write to a region in GPU memory with a specific pattern and in the packet we send we have a different pattern. As a proof of concept we expect that the packet's data overwrites this memory buffer.

See [this post](https://forums.developer.nvidia.com/t/clarification-on-requirements-for-gpudirect-rdma/188114) for the original description of the problem.

1. A queue pair and its associated resources are established exactly as described in the (generic application flow)[https://docs.nvidia.com/networking/display/RDMAAwareProgrammingv17/Typical+Application]
  1. Lines 0-192 of the attached code
2. Register a region of host memory and fill it with a known pattern
      1.lines 192-195
3. ​Register a region of GPU memory 
      1.Lines 197-223
4. Send a packet containing a known pattern from one Mellanox device to another
      1.Lines 223-375
5. Copy the data from the GPU device's memory region into the host system memory which we expect to overwrite the host system memory's bit pattern with the one we just sent
      1.Line 375-380
6. Confirm that the memory patterns match. The idea being that we just sent a *new* pattern from one Mellanox device to the other and then told it to overwrite the pattern that was already in system memory with what the GPU received. The logic being that we expect the pattern which was in system memory to be overwritten by what was just sent.
      1.This happens in lines 391-396​

 At no point does the CUDA toolkit issue any errors. Everything returns as a success however, the pattern in system memory *is not* overwritten. Need to determine why this simple POC does not work in order to move forward with customer.

## Lab Configuration

### Hardware Configuration

Dell R750 with a Mellanox MLX6 as the transmitting device and a MLX5 as the receiving device. Worth noting is that at the time of writing there is no special MLX6 driver. All device names will appear is MLX5.

### RHEL Version

```
NAME="Red Hat Enterprise Linux"
VERSION="8.5 (Ootpa)"
ID="rhel"
ID_LIKE="fedora"
VERSION_ID="8.5"
PLATFORM_ID="platform:el8"
PRETTY_NAME="Red Hat Enterprise Linux 8.5 (Ootpa)"
ANSI_COLOR="0;31"
CPE_NAME="cpe:/o:redhat:enterprise_linux:8::baseos"
HOME_URL="https://www.redhat.com/"
DOCUMENTATION_URL="https://access.redhat.com/documentation/red_hat_enterprise_linux/8/"
BUG_REPORT_URL="https://bugzilla.redhat.com/"

REDHAT_BUGZILLA_PRODUCT="Red Hat Enterprise Linux 8"
REDHAT_BUGZILLA_PRODUCT_VERSION=8.5
REDHAT_SUPPORT_PRODUCT="Red Hat Enterprise Linux"
REDHAT_SUPPORT_PRODUCT_VERSION="8.5"
Red Hat Enterprise Linux release 8.5 (Ootpa)
Red Hat Enterprise Linux release 8.5 (Ootpa)

```

### GCC Version

```
[root@gputest ~]# gcc --version
gcc (GCC) 8.5.0 20210514 (Red Hat 8.5.0-4)
Copyright (C) 2018 Free Software Foundation, Inc.
This is free software; see the source for copying conditions.  There is NO
warranty; not even for MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
```

### Nvidia SMI

```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 495.29.05    Driver Version: 495.29.05    CUDA Version: 11.5     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA A100-PCI...  Off  | 00000000:CA:00.0 Off |                    0 |
| N/A   26C    P0    35W / 250W |    541MiB / 40536MiB |      0%      Default |
|                               |                      |             Disabled |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|    0   N/A  N/A      4969      G   /usr/libexec/Xorg                  26MiB |
|    0   N/A  N/A      5345      G   /usr/bin/gnome-shell               98MiB |
|    0   N/A  N/A    606994      C   /tmp/test/rdma-loopback           413MiB |
+-----------------------------------------------------------------------------+
```

### CUDA Version

```
[root@gputest ~]# nvcc --version
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2021 NVIDIA Corporation
Built on Thu_Nov_18_09:45:30_PST_2021
Cuda compilation tools, release 11.5, V11.5.119
Build cuda_11.5.r11.5/compiler.30672275_0
`

### MLX Config

See [MLX5_0](images/mlx5_0.log) and [MLX5_2](images/mlx5_2.log)

## Installation

### MLNX_OFED

1. Download MLNX_OFED drivers from https://www.mellanox.com/products/infiniband-drivers/linux/mlnx_ofed
      1.MLNX_OFED is version dependent. I suggest you use  `subscription-manager release --set=8.4` to ensure your version of RHEL stays at the version for which MLNX_OFED was compiled
2. Upload the ISO to the target box
3. Run:

```bash
dnf group install "Development Tools" -y
dnf install -y tk tcsh tcl gcc-gfortran kernel-modules-extra gcc-g++ gdb rsync ninja-build make zip
mount MLNX* /mnt
cd /mnt
./mlnxofedinstall
```

## Setting Up the Code Environment

### CUDA Development Packages

1. Make sure you have an Nvidia GPU that shows on the device with `lspci | grep -i nvidia`
2. Make sure you have the kernel dev headers for your kernel. with `rpm -qa | grep devel | grep kernel && uname -r`
3. Run the following (See [Nvidia's instructions](https://developer.nvidia.com/cuda-downloads?target_os=Linux&target_arch=x86_64&Distribution=RHEL&target_version=8&target_type=rpm_local) for details):

```bash
dnf install -y https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm
subscription-manager repos --enable=rhel-8-for-x86_64-appstream-rpms
subscription-manager repos --enable=rhel-8-for-x86_64-baseos-rpms
subscription-manager repos --enable=codeready-builder-for-rhel-8-x86_64-rpms
sudo rpm -i cuda-repo-rhel8-11-5-local-11.5.1_495.29.05-1.x86_64.rpm
sudo dnf config-manager --add-repo https://developer.download.nvidia.com/compute/cuda/repos/rhel8/x86_64/cuda-rhel8.repo
sudo dnf clean expire-cache
sudo dnf module install -y nvidia-driver:latest-dkms
sudo dnf install -y cuda
export PATH=/usr/local/cuda-11.5/bin${PATH:+:${PATH}}
echo 'export PATH=/usr/local/cuda-11.5/bin${PATH:+:${PATH}}' >> /root/.bashrc
modprobe nvidia-peermem # YOU MUST RUN THIS MANUALLY
# Below is just for debugging. You don't have to install them.
# Make sure, even though it is RHEL 8, you use the word yum here.
yum debuginfo-install libgcc-8.5.0-4.el8_5.x86_64 libibverbs-55mlnx37-1.55103.x86_64 libnl3-3.5.0-1.el8.x86_64 libstdc++-8.5.0-4.el8_5.x86_64 nvidia-driver-cuda-libs-495.29.05-1.el8.x86_64
```

**WARNING** Whenever you want to run this code you must manually load the `nvidia-peermem` module. See [Nvidia peermem](https://docs.nvidia.com/cuda/gpudirect-rdma/index.html#nvidia-peermem). Load with `modprobe nvidia-peermem`

### Prepare the Code

First we need to make some manual adjustments to some parameters in the code. For this you need the MAC addresses

My first challenge was that the system was entirely remote so I had to figure out how to determine exactly which interfaces belonged to which card. To find the MAC addresses remotely you can use `lspci -v | grep -i ethernet` and compare that with the output of `ethtool -i <interface_name>`. This will allow you to corelate the model name of the NIC to the interface/MAC using the PCIe bus number. Ex:

```
[root@gputest ~]# ip a s
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eno8303: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether b0:7b:25:f8:44:d2 brd ff:ff:ff:ff:ff:ff
    inet 172.28.1.40/24 brd 172.28.1.255 scope global dynamic noprefixroute eno8303
       valid_lft 71017sec preferred_lft 71017sec
    inet6 fe80::b27b:25ff:fef8:44d2/64 scope link noprefixroute
       valid_lft forever preferred_lft forever
3: eno8403: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc mq state DOWN group default qlen 1000
    link/ether b0:7b:25:f8:44:d3 brd ff:ff:ff:ff:ff:ff
4: eno12399: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether b4:96:91:cd:e8:ac brd ff:ff:ff:ff:ff:ff
5: eno12409: <BROADCAST,MULTICAST> mtu 1500 qdisc noop state DOWN group default qlen 1000
    link/ether b4:96:91:cd:e8:ad brd ff:ff:ff:ff:ff:ff
6: ens6f0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc mq state DOWN group default qlen 1000
    link/ether b8:ce:f6:cc:9e:dc brd ff:ff:ff:ff:ff:ff
7: ens6f1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether b8:ce:f6:cc:9e:dd brd ff:ff:ff:ff:ff:ff
8: ens5f0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc mq state UP group default qlen 1000
    link/ether 0c:42:a1:73:8d:e6 brd ff:ff:ff:ff:ff:ff
9: ens5f1: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc mq state DOWN group default qlen 1000
    link/ether 0c:42:a1:73:8d:e7 brd ff:ff:ff:ff:ff:ff
10: virbr0: <NO-CARRIER,BROADCAST,MULTICAST,UP> mtu 1500 qdisc noqueue state DOWN group default qlen 1000
    link/ether 52:54:00:b7:e9:a7 brd ff:ff:ff:ff:ff:ff
    inet 192.168.122.1/24 brd 192.168.122.255 scope global virbr0
       valid_lft forever preferred_lft forever
11: virbr0-nic: <BROADCAST,MULTICAST> mtu 1500 qdisc fq_codel master virbr0 state DOWN group default qlen 1000
    link/ether 52:54:00:b7:e9:a7 brd ff:ff:ff:ff:ff:ff
[root@gputest test_code]# lspci -v | grep -i ethernet
04:00.0 Ethernet controller: Broadcom Inc. and subsidiaries NetXtreme BCM5720 Gigabit Ethernet PCIe
04:00.1 Ethernet controller: Broadcom Inc. and subsidiaries NetXtreme BCM5720 Gigabit Ethernet PCIe
31:00.0 Ethernet controller: Intel Corporation Ethernet Controller E810-XXV for SFP (rev 02)
        Subsystem: Intel Corporation Ethernet 25G 2P E810-XXV OCP
31:00.1 Ethernet controller: Intel Corporation Ethernet Controller E810-XXV for SFP (rev 02)
        Subsystem: Intel Corporation Ethernet 25G 2P E810-XXV OCP
98:00.0 Ethernet controller: Mellanox Technologies MT2892 Family [ConnectX-6 Dx]
98:00.1 Ethernet controller: Mellanox Technologies MT2892 Family [ConnectX-6 Dx]
b1:00.0 Ethernet controller: Mellanox Technologies MT28800 Family [ConnectX-5 Ex]
b1:00.1 Ethernet controller: Mellanox Technologies MT28800 Family [ConnectX-5 Ex]
[root@gputest test_code]# ethtool -i ens6f1
driver: mlx5_core
version: 5.5-1.0.3
firmware-version: 22.31.1014 (DEL0000000027)
expansion-rom-version:
bus-info: 0000:98:00.1
supports-statistics: yes
supports-test: yes
supports-eeprom-access: no
supports-register-dump: no
supports-priv-flags: yes
[root@gputest ~]# ethtool -i ens5f0
driver: mlx5_core
version: 5.5-1.0.3
firmware-version: 16.27.6106 (DEL0000000004)
expansion-rom-version:
bus-info: 0000:b1:00.0
supports-statistics: yes
supports-test: yes
supports-eeprom-access: no
supports-register-dump: no
supports-priv-flags: yes
```

So here we can see from the bus numbers that in my case MLX6 device is ens6f0/ens6f1 and the MLX5 is ens5f0/ensf1. My transmit interface will be b8:ce:f6:cc:9e:dd/ens6f1 and my receive is 0c:42:a1:73:8d:e6/ens5f0.

Next you have to figure out the Mellanox device numbers. You can do this using mlxconfig. To get this listing run `mlxconfig -d mlx5_0 q`. In the header of each block you should see something like this:

```
Device #1:
----------

Device type:    ConnectX6DX
Name:           0F6FXM_08P2T2_Ax
Description:    Mellanox ConnectX-6 Dx Dual Port 100 GbE QSFP56 Network Adapter
Device:         mlx5_0
```

From my experimentation they are in order. So mlx5_0 is the first interface on the MLX6 device which lines up with ens6f0. This means mlx5_1 is the second interface and then mlx5_3 would be the first interface of the MLX5 device which we can confirm with `mlxconfig -d mlx5_3 q`

```
Device #1:
----------

Device type:    ConnectX5
Name:           09FTMY_071C1T_Ax
Description:    Mellanox ConnectX-5 Ex Dual Port 100 GbE QSFP Network Adapter
Device:         mlx5_3
```

### Compiling and Running the App

```bash
g++ rdma-loopback.cc -o rdma-loopback -libverbs -I/usr/local/cuda/include -L/usr/local/cuda/lib64 -lcudart
```

## Debugging

`gdb --args rdma-loopback 0`

`set print pretty on` is helpful

To get the config of the Mellanox devices run `mlxconfig -d mlx5_0 q > mlx5_0.log`. Replace mlx5 with your device name.