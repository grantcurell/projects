# Configuring and Running Cisco Trex

## Helpful Materials

[Trex GUI Releases](https://github.com/cisco-system-traffic-generator/trex-stateless-gui/releases)

[Installing Trex with Napatech](https://trex-tgn.cisco.com/trex/doc/trex_appendix_napatech.html)

[Dell R840 Bifurcation](https://qrl.dell.com/Files/en-us/html/Manuals/R840/Shoemaker_4U_Slotbifurcation=GUID-C00A48B5-849E-4569-B08E-F488A3CE43F4=1=en-us=.html)

[Understanding PCIe](https://community.mellanox.com/s/article/understanding-pcie-configuration-for-maximum-performance#jive_content_id_PCIe_Max_Payload_Size)

[Trex Traffic YAML (config file definitions)](https://trex-tgn.cisco.com/trex/doc/trex_manual.html#_traffic_yaml_f_argument_of_stateful)

[Trex Traffic Generator Config Section Definitions](https://trex-tgn.cisco.com/trex/doc/trex_manual.html#_clients_servers_ip_allocation_scheme)

## Install T-Rex

### Make Sure You Have Sufficient DRAM Chennels

In all bare metal cases, it’s important to have 4 DRAM channels. Fewer channels will impose a performance issue. To test it you can run `sudo dmidecode -t memory | grep CHANNEL` and check CHANNEL x

### Build T-Rex with NapaTech Support

1. Browse to [trex's release page](https://github.com/cisco-system-traffic-generator/trex-core/releases) and pull the latest release.
2. Unzip/untar it into `/opt`
3. Run `cd /opt/trex-core-2.81/linux_dpdk` (change version as necessary)
4. Run `./b configure`
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
                'configure' finished successfully (0.443s)

5. Run `./b`. At the end it should say *'build' finished successfully*
6. To address the individual ports on a PCI NIC you need to use the syntax <pci-device>/<port-no>.
7. Modify */etc/trex_cfg.yaml* with the bus ID and any other relevant config settings:

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