# How to Get DPDK with pdump Running

The purpose of this experiment is to get Intel's DPDK framework up and running on
a virtual machine.

# Useful Materials

[VMWare info on Intel DPDK](https://www.vmware.com/content/dam/digitalmarketing/vmware/en/pdf/techpaper/intel-dpdk-vsphere-solution-brief-white-paper.pdf)

[How to Compile DPDK](https://doc.dpdk.org/guides/linux_gsg/build_dpdk.html#install-the-dpdk-and-browse-sources)

[Info on Linux Drivers for DPDK](https://doc.dpdk.org/guides/linux_gsg/linux_drivers.html)

# My Environment

I am running this inital test on ESXi 6.7 in a virtual machine

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

    Linux centos.lan 3.10.0-1062.4.1.el7.x86_64 #1 SMP Fri Oct 18 17:15:30 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux

# Installation

## Configure GRUB Command Line for Virtualized DPDK

In order for DPDK to work in a virtual environment you must disable memory protection.
The reason for this is that with memory protection enabled CentOS will block read/write/execution
to the DMA'd portion of memory. See [this](https://stackoverflow.com/questions/52542310/incompatible-hardware-version-error-when-running-dpdk-on-vmware-with-vmxnet3-i) post.

Do the following:

1. `cd /etc/default`
2. `vim grub`
3. Edit GRUB-CMDLINE and Add “nopku”

                GRUB_CMDLINE_LINUX="crashkernel=auto rd.lvm.lv=centos/root rd.lvm.lv=centos/swap rhgb quiet nopku  transparent_hugepage=never log_buf_len=8M"

4. Recompile grub: sudo grub2-mkconfig -o /boot/grub2/grub.cfg
5. `reboot`

## Install DPDK

1. Download from [https://core.dpdk.org/download/](https://core.dpdk.org/download/)
2. Run `yum install -y gcc numactl-devel kernel-devel pciutils elfutils-libelf-devel make libpcap python3 tar vim wget tmux vim mlocate hwloc libpcap-devel`
3. Extract dpdk and cd into its directory
4. set the environment variable RTE_SDK. It is the directory in which you extracted all the DPDK files. `export RTE_SDK=<YOUR_DIR>`
5. Run `make install T=x86_64-native-linux-gcc DESTDIR=<INSTALL_DIR>` to build dpdk. Ensure your install directory exists.

Once an DPDK target environment directory has been created (such as x86_64-native-linux-gcc), 
it contains all libraries and header files required to build an application. When 
compiling an application in the Linux* environment on the DPDK, the following variables 
must be exported:

- RTE_TARGET - Points to the DPDK target environment directory.
<br>

        export RTE_TARGET=/opt/dpdk-19.08/x86_64-native-linux-gcc

You may want to add this variable and RTE_SDK to *~/.bash_profile*

# Configuration

## Update Ulimits

1. Edit the security limits with `vim /etc/security/limits.conf`
2. Add the following lines at the end of the file:

        root    hard   memlock           unlimited
        root    soft   memlock           unlimited

3. Reboot and see if the system has the newly updated value

## Configure vfio-pci to Load on Boot

1. Go to /etc/modules-load.d/

        cd /etc/modules-load.d

2. Run `echo vfio-pci > vfio-pci.conf`
3. If you don't reboot you will need to run `modprobe vfio-pci`

## Configure Ports

1. Move to your `INSTALL_DIR` and run `./usertools/dpdk-setup.sh`. This should give you a menu with all available DPDK options. The menu is setup in such a way that you must perform each step listed in the menu. If things have gone correctly to this point your Step 1 should look like the following:

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

**WARNING**: If you run Option 3 to insert the VFIO module I found that it actually
caused DPDK to stop working.

3. Next run option 6 to instert huge pages for NUMA systems. Notice you will be prompted to select an amount of memory on a per processor basis. This is because there are pages associated with each individual processor to increase performance via locality.
4. Run option 7 and make sure you receive output and that network devices are listed. My output looks like this:

        Network devices using kernel driver
        ===================================
        0000:0b:00.0 'VMXNET3 Ethernet Controller 07b0' if=ens192 drv=vmxnet3 unused=vfio-pci *Active*
        0000:13:00.0 'VMXNET3 Ethernet Controller 07b0' if=ens224 drv=vmxnet3 unused=vfio-pci *Active*

        No 'Baseband' devices detected
        ==============================

        No 'Crypto' devices detected
        ============================

        No 'Eventdev' devices detected
        ==============================

        No 'Mempool' devices detected
        =============================

        No 'Compress' devices detected
        ==============================

        No 'Misc (rawdev)' devices detected
        ===================================

**NOTE**: The active keyword means that DPDK thinks the interface is under active use.
This typically means it has an IP address assigned to it.

5. Run option 9 to bind an interface to DPDK
6. 

# Notes

- You can use PCI passthrough on the x520 and x710

1. Run `ethtool -i <your_interface>` to figure out what kind of driver you have
2. Run `bash /opt/dpdk-19.08/usertools/dpdk-setup.sh`
3. Run option 47 and then enter 64 when prompted
4. Run option 44 to insert the VRIO module
5.  Run `ulimit -u unlimited` to increase the memlock limit (NOTE: I don't think this did what I needed it to.)

add iommu=pt intel_iommu=on
grub2-mkconfig -o /boot/grub2/grub.cfg