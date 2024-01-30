# Installing DPDK with NapaTech Card

## System Info

I wrote this on CentOS 7

### Release

        CentOS Linux release 7.7.1908 (Core)
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

### Kernel

        Linux r840-1.lan 3.10.0-1062.9.1.el7.x86_64 #1 SMP Fri Dec 6 15:49:49 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux

## Helpful Documents

[NUMA Nodes and NapaTech](https://docs.napatech.com/reader/JIm9z8~DgULRfbHc76qu5A/G9HjOdvbUhb4QqP8GZpBVQ)

[Optimizing the NapaTech Card Settings](https://docs.napatech.com/reader/GHSQQPQbWLPdJUmxIkO91Q/VhLG5HF4vHVD3x4Z1Yfazg)

## Install NapaTech Driver

1. Download the [Napatech software](https://supportportal.napatech.com/index.php?/selfhelp/view-article/Link%E2%84%A2-Capture-Software-11.9.0-release-for-Linux/580) from here
2. Run `yum groupinstall "Development Tools" && yum install -y kernel-devel gettext-devel openssl-devel perl-CPAN perl-devel zlib-devel pciutils && yum install -y https://centos7.iuscommunity.org/ius-release.rpm && yum remove -y git && yum install -y git2u-all`
3. Unzip and run `package_install_3gd.sh`
4. Run `/opt/napatech3/bin/ntstop.sh && /opt/napatech3/bin/ntstart.sh` to restart the NapaTech driver which will create a default configuration file.

### Update Host Buffers

The /opt/napatech3/config/ntservice.ini contains the following settings that control the number and size of hostbuffers. To increase the number of CPUs/Cores which we can leverage with the SmartNIC, we need to increase the number of hostbuffers.

Host buffers in Napatech Software Suite are the buffers used for moving (DMA) data packets between the accelerator and the applications.

In the config file it should look like this:

        HostBuffersRx = [64,16,-1]                # [x1, x2, x3], ...
        HostBuffersTx = [64,16,-1]                # [x1, x2, x3], ...

- First number is the number of host buffers
- Second number is the size of the host buffers in MegaBytes
- Third number is the NUMA node

You have to have one set of numbers for each NUMA node. -1 means read the NUMA node setting in the NumaNode directive in the configuration file.

        HostBuffersRx = [16,2048,0],[16,2048,1],[16,2048,2],[16,2048,3]
        HostBuffersTx = [16,2048,0],[16,2048,1],[16,2048,2],[16,2048,3]

You can check what NUMA node your card is on with: `cat "/sys/bus/pci/devices/0000:5b:00.0/numa_node"`. You'll just have to replace the bus ID with your card's bus ID. You can retrieve that with the `/opt/napatech3/bin/adapterinfo` command.

## Install DPDK

1. `export NAPATECH3_PATH=/opt/napatech3`
2. Download with `git clone https://github.com/napatech/dpdk.git`
      1.I put this in `/opt` and will assume you have done the same in this guide.
3. Edit the security limits with `vim /etc/security/limits.conf`. After making the below edits you will need to log out and log back in for them to take effect.
      1.Add the following lines at the end of the file. This assumes you are running as root:

                root    hard   memlock           unlimited
                root    soft   memlock           unlimited

4. Run `yum install -y gcc numactl-devel kernel-devel pciutils elfutils-libelf-devel make libpcap python3 tar vim wget tmux vim mlocate hwloc libpcap-devel python36-devel`
5. set the environment variable RTE_SDK. It is the directory in which you extracted all the DPDK files. `export RTE_SDK=/opt/dpdk` (or your directory)
6. Run `make config T=x86_64-native-linuxapp-gcc install CONFIG_RTE_LIBRTE_PMD_PCAP=y CONFIG_RTE_LIBRTE_PDUMP=y DESTDIR=install CONFIG_RTE_LIBRTE_PMD_NTACC=y` to build dpdk. Ensure your install directory exists.
7. `make -j`

**NOTE**: The option CONFIG_RTE_LIBRTE_PMD_PCAP=y enabled libpcap support in DPDK.
This is required for pdump to work.

Once an DPDK target environment directory has been created (such as x86_64-native-linux-gcc), 
it contains all libraries and header files required to build an application. When 
compiling an application in the Linux* environment on the DPDK, the following variables 
must be exported:

- RTE_TARGET - Points to the DPDK target environment directory.

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

## Configuration

### Configure Ports

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

3. Next run option 6 to instert huge pages for NUMA systems. Notice you will be prompted to select an amount of memory on a per processor basis. This is because there are pages associated with each individual processor to increase performance via locality. I used a value of 4096 for each NUMA node. For 1GB per NUMA node insert 512.
