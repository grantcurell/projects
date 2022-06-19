# How to Get DPDK with pdump Running

The purpose of this experiment is to get Intel's DPDK framework up and running on
a server.

# Useful Materials

[How to Compile DPDK](https://doc.dpdk.org/guides/linux_gsg/build_dpdk.html#install-the-dpdk-and-browse-sources)

[Info on Linux Drivers for DPDK](https://doc.dpdk.org/guides/linux_gsg/linux_drivers.html)

[Description of the TestPMD Program](https://software.intel.com/en-us/articles/testing-dpdk-performance-and-features-with-testpmd)

# My Environment

I am running a Dell R940 with Napatech Card NT200A02

## CentOS Release Info

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

        CentOS Linux release 7.7.1908 (Core)
        CentOS Linux release 7.7.1908 (Core)

## Kernel Info

    Linux r940.lan 3.10.0-1062.4.3.el7.x86_64 #1 SMP Wed Nov 13 23:58:53 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux

## Physical Setup


# Installation NapaTech Driver

## Install Driver

1. Download the [Napatech software](https://supportportal.napatech.com/index.php?/selfhelp/view-article/Link%E2%84%A2-Capture-Software-11.9.0-release-for-Linux/580) from here
2. Run `yum groupinstall "Development Tools" && yum install -y kernel-devel gettext-devel openssl-devel perl-CPAN perl-devel zlib-devel pciutils && yum install -y https://centos7.iuscommunity.org/ius-release.rpm && yum remove -y git && yum install -y git2u-all`
3. Unzip and run `package_install_3gd.sh`

## Install DPDK

1. `export NAPATECH3_PATH=/opt/napatech3`
2. Download with `git clone https://github.com/napatech/dpdk.git`
3. Edit the security limits with `vim /etc/security/limits.conf`. After making the below edits you will need to log out and log back in for them to take effect.
   1. Add the following lines at the end of the file. This assumes you are running as root:

                root    hard   memlock           unlimited
                root    soft   memlock           unlimited

4. Run `yum install -y gcc numactl-devel kernel-devel pciutils elfutils-libelf-devel make libpcap python3 tar vim wget tmux vim mlocate hwloc libpcap-devel python36-devel`
5. Extract dpdk and cd into its directory
6. set the environment variable RTE_SDK. It is the directory in which you extracted all the DPDK files. `export RTE_SDK=<YOUR_DIR>`
7. Run `make config T=x86_64-native-linuxapp-gcc install CONFIG_RTE_LIBRTE_PMD_PCAP=y CONFIG_RTE_LIBRTE_PDUMP=y DESTDIR=install CONFIG_RTE_LIBRTE_PMD_NTACC=y` to build dpdk. Ensure your install directory exists.
8. `make -j`

**NOTE**: The option CONFIG_RTE_LIBRTE_PMD_PCAP=y enabled libpcap support in DPDK.
This is required for pdump to work.

Once an DPDK target environment directory has been created (such as x86_64-native-linux-gcc), 
it contains all libraries and header files required to build an application. When 
compiling an application in the Linux* environment on the DPDK, the following variables 
must be exported:

- RTE_TARGET - Points to the DPDK target environment directory.
<br>

        export RTE_TARGET=/opt/dpdk-19.08/x86_64-native-linux-gcc

You may want to add this variable and RTE_SDK to *~/.bash_profile*

### Update Your Bash Profile

Add:

        export RTE_SDK=/opt/dpdk
        export NAPATECH3_PATH=/opt/napatech3
        export RTE_TARGET=/opt/dpdk/x86_64-native-linuxapp-gcc
        
to `~/.bash_profile`

## Install ELF Tools

Run the following:

        pip3 install numpy
        pip3 install elftools
        pip3 install pyelftools

# Configuration

## Configure Ports

1. Move to your dpdk dir and run `./install/share/dpdk/usertools/dpdk-setup.sh`. This should give you a menu with all available DPDK options. The menu is setup in such a way that you must perform each step listed in the menu. If things have gone correctly to this point your Step 1 should look like the following:

        ----------------------------------------------------------
        Step 1: Select the DPDK environment to build
        ----------------------------------------------------------
        [1] *

2. My menu looks like this:

        ----------------------------------------------------------
        Step 1: Select the DPDK environment to build
        ----------------------------------------------------------
        [1] *

        ----------------------------------------------------------
        Step 2: Setup linux environment
        ----------------------------------------------------------
        [2] Insert IGB UIO module
        [3] Insert VFIO module
        [4] Insert KNI module
        [5] Setup hugepage mappings for non-NUMA systems
        [6] Setup hugepage mappings for NUMA systems
        [7] Display current Ethernet/Baseband/Crypto device settings
        [8] Bind Ethernet/Baseband/Crypto device to IGB UIO module
        [9] Bind Ethernet/Baseband/Crypto device to VFIO module
        [10] Setup VFIO permissions

        ----------------------------------------------------------
        Step 3: Run test application for linux environment
        ----------------------------------------------------------
        [11] Run test application ($RTE_TARGET/app/test)
        [12] Run testpmd application in interactive mode ($RTE_TARGET/app/testpmd)

        ----------------------------------------------------------
        Step 4: Other tools
        ----------------------------------------------------------
        [13] List hugepage info from /proc/meminfo

        ----------------------------------------------------------
        Step 5: Uninstall and system cleanup
        ----------------------------------------------------------
        [14] Unbind devices from IGB UIO or VFIO driver
        [15] Remove IGB UIO module
        [16] Remove VFIO module
        [17] Remove KNI module
        [18] Remove hugepage mappings

        [19] Exit Script

3. Next run option 6 to instert huge pages for NUMA systems. Notice you will be prompted to select an amount of memory on a per processor basis. This is because there are pages associated with each individual processor to increase performance via locality. I used a value of 4096 for each NUMA node.

# Performing Packet Capture

## Setup the NapaTech Card

## Initial Setup

Get the core layout with `./install/share/dpdk/usertools/cpu_layout.py`
View your port layout with `./install/share/dpdk/usertools/dpdk-devbind.py -s`

## Starting testpmd

**NOTE**: The `--` separates the argumentsn for the EAL vs TestPMD.

        ./install/bin/testpmd -l 0,4,8,12,16,20,24,28,32,36 -n 4 -- -i

After `testpmd` has started don't forget to run the `start` command on the testpmd
command line.

## pdump

        ./install/bin/dpdk-pdump -- --pdump 'device_id=0000:5b:00.0,queue=*,rx-dev=/tmp/capture.pcap'

# Helpful Tips

## NapaTech

### Detecting Installed Cards

        /opt/napatech3/bin/imgctrl -q 

### Load the Driver

        /opt/napatech3/bin/ntload.sh

### Run the ntserver

        /opt/napatech3/bin/ntstart.sh 

### Show Interface Info

        /opt/napatech3/bin/adapterinfo



## Getting CPU Info

DPDK provides a tool for seeing the CPU layout with `./install/share/dpdk/usertools/cpu_layout.py`
You can see the logical layout of the cores with `cat /proc/cpuinfo`
You can alse run `lstopo-no-graphics`

Notice that the cores alternate back and forth.

## Process Types in DPDK

DPDK runs two different types of processes. There are as follows:

- primary processes, which can initialize and which have full permissions on shared memory
- secondary processes, which cannot initialize shared memory, but can attach to pre- initialized shared memory and create objects in it.

Standalone DPDK processes are primary processes, while secondary processes can only run alongside a primary process or after a primary process has already configured the hugepage shared memory for them.

## TestPMD 

The test pmd manual is available [here](./dpdk-testpmd-application-user-guide.pdf)

### Interactive Commands

#### Starting transmit

        start

#### Get Port Info

        show port info all

### Forwarding Modes

TestPMD has different forwarding modes that can be used within the application.

- Input/output mode: This mode is generally referred to as IO mode. It is the most common forwarding mode and is the default mode when TestPMD is started. In IO mode a CPU core receives packets from one port (Rx) and transmits them to another port (Tx). The same port can be used for reception and transmission if required.
- Rx-only mode: In this mode the application polls packets from the Rx ports and frees them without transmitting them. In this way it acts as a packet sink.
- Tx-only mode: In this mode the application generates 64-byte IP packets and transmits them from the Tx ports. It doesn’t handle the reception of packets and as such acts as a packet source.
These latter two modes (Rx-only and Tx-only) are useful for checking packet reception and transmission separately.

Apart from these three modes there are other forwarding modes that are explained in the [TestPMD documentation](http://doc.dpdk.org/guides/testpmd_app_ug/testpmd_funcs.html#set-fwd).

### Port Topology Modes

In paired mode, the forwarding is between pairs of ports, for example: (0,1), (2,3), (4,5).

In chained mode, the forwarding is to the next available port in the port mask, for example:
(0,1), (1,2), (2,0).
The ordering of the ports can be changed using the portlist testpmd runtime function.

In loop mode, ingress traffic is simply transmitted back on the same interface.

### Receive Side Scaling

=Receive-Side Scaling (RSS), also known as multi-queue receive, distributes network receive processing across several hardware-based receive queues, allowing inbound network traffic to be processed by multiple CPUs. RSS can be used to relieve bottlenecks in receive interrupt processing caused by overloading a single CPU, and to reduce network latency.

To determine whether your network interface card supports RSS, check whether multiple interrupt request queues are associated with the interface in /proc/interrupts. For example, if you are interested in the p1p1 interface:

        # egrep 'CPU|p1p1' /proc/interrupts
        CPU0    CPU1    CPU2    CPU3    CPU4    CPU5
        89:   40187       0       0       0       0       0   IR-PCI-MSI-edge   p1p1-0
        90:       0     790       0       0       0       0   IR-PCI-MSI-edge   p1p1-1
        91:       0       0     959       0       0       0   IR-PCI-MSI-edge   p1p1-2
        92:       0       0       0    3310       0       0   IR-PCI-MSI-edge   p1p1-3
        93:       0       0       0       0     622       0   IR-PCI-MSI-edge   p1p1-4
        94:       0       0       0       0       0    2475   IR-PCI-MSI-edge   p1p1-5

----

huge pages https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/performance_tuning_guide/sect-red_hat_enterprise_linux-performance_tuning_guide-memory-configuring-huge-pages
