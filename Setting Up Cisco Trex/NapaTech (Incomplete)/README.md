# Configuring and Running Cisco Trex

## Helpful Materials

[Trex GUI Releases](https://github.com/cisco-system-traffic-generator/trex-stateless-gui/releases)

[Installing Trex with Napatech](https://trex-tgn.cisco.com/trex/doc/trex_appendix_napatech.html)

[NUMA Nodes and NapaTech](https://docs.napatech.com/reader/JIm9z8~DgULRfbHc76qu5A/G9HjOdvbUhb4QqP8GZpBVQ)

[Optimizing the NapaTech Card Settings](https://docs.napatech.com/reader/GHSQQPQbWLPdJUmxIkO91Q/VhLG5HF4vHVD3x4Z1Yfazg)

[Dell R840 Bifurcation](https://qrl.dell.com/Files/en-us/html/Manuals/R840/Shoemaker_4U_Slotbifurcation=GUID-C00A48B5-849E-4569-B08E-F488A3CE43F4=1=en-us=.html)

[Understanding PCIe](https://community.mellanox.com/s/article/understanding-pcie-configuration-for-maximum-performance#jive_content_id_PCIe_Max_Payload_Size)

[Trex Traffic YAML (config file definitions)](https://trex-tgn.cisco.com/trex/doc/trex_manual.html#_traffic_yaml_f_argument_of_stateful)

[Trex Traffic Generator Config Section Definitions](https://trex-tgn.cisco.com/trex/doc/trex_manual.html#_clients_servers_ip_allocation_scheme)

## Environment

### OS

I used CentOS 7

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

## Install NapaTech Driver (optional)

Follow the instructions in this section [Install NapaTech Driver](/Installing%20DPDK%20with%20NapaTech%20Card/README.md#install-napaTech-driver) and this section [Update Host Buffers](/Installing%20DPDK%20with%20NapaTech%20Card/README.md##update-host-buffers).

## Install T-Rex

### Make Sure You Have Sufficient DRAM Chennels

In all bare metal cases, it’s important to have 4 DRAM channels. Fewer channels will impose a performance issue. To test it you can run `sudo dmidecode -t memory | grep CHANNEL` and check CHANNEL x

### Driver Tweaks

Set the stat interval to 1:

        [System]
        ...
        StatInterval=1
        ...

The stat interval controls how frequently the statistics counters are updated.

Next set the following values:

        [Adapter?]
        ...
        HostBufferRefreshIntervalTx = 50
        CancelTxOnCloseMask = 1 # This must match the number of ports on the NIC (1,3,F)
        ...

 For me that value is 2.

Restart the NapaTech driver with `/opt/napatech3/bin/ntstop.sh && /opt/napatech3/bin/ntstart.sh`

### Build T-Rex with NapaTech Support

1. Browse to [trex's release page](https://github.com/cisco-system-traffic-generator/trex-core/releases) and pull the latest release.
2. Unzip/untar it into `/opt`
3. Run `cd /opt/trex-core-2.73/linux_dpdk` (change version as necessary)
4. Run `./b configure --with-ntacc`
   1. Verify that your output looks something like this with *'configure' finished successfully* at the bottom:

                [root@r840-1 linux_dpdk]# ./b configure --with-ntacc
                Setting top to                           : /opt/trex-core-2.73
                Setting out to                           : /opt/trex-core-2.73/linux_dpdk/build_dpdk
                Checking for program 'g++, c++'          : /usr/bin/g++
                Checking for program 'ar'                : /usr/bin/ar
                Checking if the -o link must be split from arguments : yes
                Checking for program 'gcc, cc'                       : /usr/bin/gcc
                Checking for program 'ar'                            : /usr/bin/ar
                Checking if the -o link must be split from arguments : yes
                Checking for program 'ldd'                           : /usr/bin/ldd
                Checking for library z                               : yes
                Build sanitized images (GCC >= 4.9.0)                : no
                Checking for OFED                                    : not found
                Checking for library mnl                             : not found, will use internal version
                Warning: will use internal version of ibverbs. If you need to use Mellanox NICs, install OFED:
                https://trex-tgn.cisco.com/trex/doc/trex_manual.html#_mellanox_connectx_4_support
                Checking for NTAPI                                   : Found needed NTAPI library
                'configure' finished successfully (0.443s)

5. Run `./b`. At the end it should say *'build' finished successfully*
6. Run `/opt/napatech3/bin/adapterinfo` to get the adapter info. Note the bus ID for the adapter. You will need this later. It should look something like *0000:5b:00.0*. You can drop the leading *0000:*
7. To address the individual ports on the Napatech SmartNIC, you need to use the syntax <pci-device>/<port-no>.
8. Modify */etc/trex_cfg.yaml* with the bus ID and any other relevant config settings:

         - version: 2
           interfaces: ['0000:5b:00.0/0', '0000:5b:00.0/1']
           port_info:
               - dest_mac: 00:0d:e9:06:90:24
                 src_mac:  00:0d:e9:06:48:1d
               - dest_mac: 00:0d:e9:06:90:25
                 src_mac:  00:0d:e9:06:48:1e

           platform:
               master_thread_id: 0
               latency_thread_id: 4
               dual_if:
                 - socket: 1
                   threads: [1,5,9,13,17,21,25,29,33,37,41,45,49,53,57,61]

## Setting Up Configuration Files

[NUMA Node Info](https://trex-tgn.cisco.com/trex/doc/trex_manual.html#_platform_section_configuration)

## Setting Up the GUI

1. Download the GUI from [Trex GUI Releases](https://github.com/cisco-system-traffic-generator/trex-stateless-gui/releases)


## Helpful Commands

### Check PCI Lane Capabalities

    lspci -vv -s :5b:00.0

#### Max Payload

When looking at `lspci -vv -s :5b:00.0` you can see the max payload. The maxpayload under DevCtl is the current max payload whereas DevCap is the theoretical max.