# Useful Materials

[NapaTech Installation Instructions](https://www.ntop.org/guides/pf_ring/modules/napatech.html)

(Creatinga EXT4 Filesystem)[https://thelastmaimou.wordpress.com/2013/05/04/magic-soup-ext4-with-ssd-stripes-and-strides/]

# My Environment

I am running a Dell FC640 on a Dell R940

See ![Server Specs](./server_specs.csv) for hardware details.

## Hard Drive Layout:

I had a RAID of 12 SAS SSDs in RAID0 on the PERC740. I had 7 NVMe drives I used. I couldn't get the 8th NVMe drive working.

    [root@r940 /]# lsblk
    NAME            MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
    sda               8:0    0  10.5T  0 disk /raiddata
    sdb               8:16   0 223.5G  0 disk
    ├─sdb1            8:17   0   200M  0 part /boot/efi
    ├─sdb2            8:18   0     1G  0 part /boot
    └─sdb3            8:19   0 222.3G  0 part
    ├─centos-root 253:0    0 218.3G  0 lvm  /
    └─centos-swap 253:1    0     4G  0 lvm  [SWAP]
    sdc               8:32   0  59.8G  0 disk
    nvme0n1         259:6    0   1.5T  0 disk
    └─nvme0n1p1     259:8    0   1.5T  0 part
    └─data-data   253:2    0  10.2T  0 lvm  /data
    nvme1n1         259:0    0   1.5T  0 disk
    └─nvme1n1p1     259:1    0   1.5T  0 part
    └─data-data   253:2    0  10.2T  0 lvm  /data
    nvme2n1         259:2    0   1.5T  0 disk
    └─nvme2n1p1     259:3    0   1.5T  0 part
    └─data-data   253:2    0  10.2T  0 lvm  /data
    nvme3n1         259:4    0   1.5T  0 disk
    └─nvme3n1p1     259:5    0   1.5T  0 part
    └─data-data   253:2    0  10.2T  0 lvm  /data
    nvme4n1         259:10   0   1.5T  0 disk
    └─nvme4n1p1     259:13   0   1.5T  0 part
    └─data-data   253:2    0  10.2T  0 lvm  /data
    nvme5n1         259:11   0   1.5T  0 disk
    nvme6n1         259:7    0   1.5T  0 disk
    └─nvme6n1p1     259:9    0   1.5T  0 part
    └─data-data   253:2    0  10.2T  0 lvm  /data
    nvme7n1         259:12   0   1.5T  0 disk
    └─nvme7n1p1     259:14   0   1.5T  0 part
    └─data-data   253:2    0  10.2T  0 lvm  /data


    [root@r940 /]# pvs
    PV             VG     Fmt  Attr PSize    PFree
    /dev/nvme0n1p1 data   lvm2 a--    <1.46t    0
    /dev/nvme1n1p1 data   lvm2 a--    <1.46t    0
    /dev/nvme2n1p1 data   lvm2 a--    <1.46t    0
    /dev/nvme3n1p1 data   lvm2 a--    <1.46t    0
    /dev/nvme4n1p1 data   lvm2 a--    <1.46t    0
    /dev/nvme6n1p1 data   lvm2 a--    <1.46t    0
    /dev/nvme7n1p1 data   lvm2 a--    <1.46t    0
    /dev/sdb3      centos lvm2 a--  <222.31g    0
    [root@r940 /]# vgs
    VG     #PV #LV #SN Attr   VSize    VFree
    centos   1   2   0 wz--n- <222.31g    0
    data     7   1   0 wz--n-  <10.19t    0
    [root@r940 /]# lvs
    LV   VG     Attr       LSize    Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
    root centos -wi-ao---- <218.31g
    swap centos -wi-ao----    4.00g
    data data   -wi-ao----  <10.19t


    WARNING: fdisk GPT support is currently new, and therefore in an experimental phase. Use at your own discretion.

    Disk /dev/nvme1n1: 1600.3 GB, 1600321314816 bytes, 3125627568 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk label type: gpt
    Disk identifier: 759A1CF7-125F-469B-981E-149EBDBE3456


    #         Start          End    Size  Type            Name
    1         2048   3125626879    1.5T  Linux LVM
    WARNING: fdisk GPT support is currently new, and therefore in an experimental phase. Use at your own discretion.

    Disk /dev/nvme2n1: 1600.3 GB, 1600321314816 bytes, 3125627568 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk label type: gpt
    Disk identifier: 57898F4D-5B5E-4495-B695-E48EA3FCFA01


    #         Start          End    Size  Type            Name
    1         2048   3125626879    1.5T  Linux LVM
    WARNING: fdisk GPT support is currently new, and therefore in an experimental phase. Use at your own discretion.

    Disk /dev/nvme3n1: 1600.3 GB, 1600321314816 bytes, 3125627568 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk label type: gpt
    Disk identifier: DB46E8E3-5E96-4228-A148-E6C8F0187DF4


    #         Start          End    Size  Type            Name
    1         2048   3125626879    1.5T  Linux LVM
    WARNING: fdisk GPT support is currently new, and therefore in an experimental phase. Use at your own discretion.

    Disk /dev/nvme0n1: 1600.3 GB, 1600321314816 bytes, 3125627568 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk label type: gpt
    Disk identifier: 4066CDE1-E36E-41FB-8277-5E3FFDB55B4A


    #         Start          End    Size  Type            Name
    1         2048   3125626879    1.5T  Linux LVM
    WARNING: fdisk GPT support is currently new, and therefore in an experimental phase. Use at your own discretion.

    Disk /dev/nvme6n1: 1600.3 GB, 1600321314816 bytes, 3125627568 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk label type: gpt
    Disk identifier: 0360D46A-9A41-4A8D-A449-94CCDC01FA8B


    #         Start          End    Size  Type            Name
    1         2048   3125626879    1.5T  Linux LVM
    WARNING: fdisk GPT support is currently new, and therefore in an experimental phase. Use at your own discretion.

    Disk /dev/nvme4n1: 1600.3 GB, 1600321314816 bytes, 3125627568 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk label type: gpt
    Disk identifier: A5D3EDDF-C93D-4B33-92B0-D25B009EEB9D


    #         Start          End    Size  Type            Name
    1         2048   3125626879    1.5T  Linux LVM

    Disk /dev/nvme5n1: 1600.3 GB, 1600321314816 bytes, 3125627568 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes

    WARNING: fdisk GPT support is currently new, and therefore in an experimental phase. Use at your own discretion.

    Disk /dev/nvme7n1: 1600.3 GB, 1600321314816 bytes, 3125627568 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes
    Disk label type: gpt
    Disk identifier: 71A0B583-E727-45B6-A1AB-791D341709B6


    #         Start          End    Size  Type            Name
    1         2048   3125626879    1.5T  Linux LVM

    Disk /dev/sda: 11515.9 GB, 11515881062400 bytes, 22491955200 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 1048576 bytes / 1048576 bytes

    WARNING: fdisk GPT support is currently new, and therefore in an experimental phase. Use at your own discretion.

    Disk /dev/sdb: 240.0 GB, 239990276096 bytes, 468731008 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 4096 bytes
    I/O size (minimum/optimal): 4096 bytes / 4096 bytes
    Disk label type: gpt
    Disk identifier: F1E6A9A1-C85F-46C1-A27E-DBC41C9260AC


    #         Start          End    Size  Type            Name
    1         2048       411647    200M  EFI System      EFI System Partition
    2       411648      2508799      1G  Microsoft basic
    3      2508800    468729855  222.3G  Linux LVM

    Disk /dev/sdc: 64.2 GB, 64239960064 bytes, 125468672 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 512 bytes / 512 bytes


    Disk /dev/mapper/centos-root: 234.4 GB, 234407067648 bytes, 457826304 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 4096 bytes
    I/O size (minimum/optimal): 4096 bytes / 4096 bytes


    Disk /dev/mapper/centos-swap: 4294 MB, 4294967296 bytes, 8388608 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 4096 bytes
    I/O size (minimum/optimal): 4096 bytes / 4096 bytes


    Disk /dev/mapper/data-data: 11202.2 GB, 11202210037760 bytes, 21879316480 sectors
    Units = sectors of 1 * 512 = 512 bytes
    Sector size (logical/physical): 512 bytes / 512 bytes
    I/O size (minimum/optimal): 131072 bytes / 917504 bytes

## CPU Layout

    [root@r940 data]# lscpu
    Architecture:          x86_64
    CPU op-mode(s):        32-bit, 64-bit
    Byte Order:            Little Endian
    CPU(s):                176
    On-line CPU(s) list:   0-175
    Thread(s) per core:    2
    Core(s) per socket:    22
    Socket(s):             4
    NUMA node(s):          4
    Vendor ID:             GenuineIntel
    CPU family:            6
    Model:                 85
    Model name:            Intel(R) Xeon(R) Gold 6152 CPU @ 2.10GHz
    Stepping:              4
    CPU MHz:               1394.146
    CPU max MHz:           3700.0000
    CPU min MHz:           1000.0000
    BogoMIPS:              4200.00
    Virtualization:        VT-x
    L1d cache:             32K
    L1i cache:             32K
    L2 cache:              1024K
    L3 cache:              30976K
    NUMA node0 CPU(s):     0,4,8,12,16,20,24,28,32,36,40,44,48,52,56,60,64,68,72,76,80,84,88,92,96,100,104,108,112,116,120,124,128,132,136,140,144,148,152,156,160,164,168,172
    NUMA node1 CPU(s):     1,5,9,13,17,21,25,29,33,37,41,45,49,53,57,61,65,69,73,77,81,85,89,93,97,101,105,109,113,117,121,125,129,133,137,141,145,149,153,157,161,165,169,173
    NUMA node2 CPU(s):     2,6,10,14,18,22,26,30,34,38,42,46,50,54,58,62,66,70,74,78,82,86,90,94,98,102,106,110,114,118,122,126,130,134,138,142,146,150,154,158,162,166,170,174
    NUMA node3 CPU(s):     3,7,11,15,19,23,27,31,35,39,43,47,51,55,59,63,67,71,75,79,83,87,91,95,99,103,107,111,115,119,123,127,131,135,139,143,147,151,155,159,163,167,171,175
    Flags:                 fpu vme de pse tsc msr pae mce cx8 apic sep mtrr pge mca cmov pat pse36 clflush dts acpi mmx fxsr sse sse2 ss ht tm pbe syscall nx pdpe1gb rdtscp lm constant_tsc art arch_perfmon pebs bts rep_good nopl xtopology nonstop_tsc aperfmperf eagerfpu pni pclmulqdq dtes64 monitor ds_cpl vmx smx est tm2 ssse3 sdbg fma cx16 xtpr pdcm pcid dca sse4_1 sse4_2 x2apic movbe popcnt tsc_deadline_timer aes xsave avx f16c rdrand lahf_lm abm 3dnowprefetch epb cat_l3 cdp_l3 invpcid_single intel_ppin intel_pt ssbd mba ibrs ibpb stibp tpr_shadow vnmi flexpriority ept vpid fsgsbase tsc_adjust bmi1 hle avx2 smep bmi2 erms invpcid rtm cqm mpx rdt_a avx512f avx512dq rdseed adx smap clflushopt clwb avx512cd avx512bw avx512vl xsaveopt xsavec xgetbv1 cqm_llc cqm_occup_llc cqm_mbm_total cqm_mbm_local dtherm ida arat pln pts pku ospke md_clear spec_ctrl intel_stibp flush_l1d
    [root@r940 data]# cpu_layout.py
    ======================================================================
    Core and Socket Information (as reported by '/sys/devices/system/cpu')
    ======================================================================

    cores =  [0, 5, 1, 4, 2, 3, 8, 12, 9, 11, 10, 21, 16, 20, 17, 19, 18, 28, 24, 27, 25, 26]
    sockets =  [0, 1, 2, 3]

            Socket 0          Socket 1          Socket 2          Socket 3
            --------          --------          --------          --------
    Core 0  [0, 88]           [1, 89]           [2, 90]           [3, 91]
    Core 5  [4, 92]           [5, 93]           [6, 94]           [7, 95]
    Core 1  [8, 96]           [9, 97]           [10, 98]          [11, 99]
    Core 4  [12, 100]         [13, 101]         [14, 102]         [15, 103]
    Core 2  [16, 104]         [17, 105]         [18, 106]         [19, 107]
    Core 3  [20, 108]         [21, 109]         [22, 110]         [23, 111]
    Core 8  [24, 112]         [25, 113]         [26, 114]         [27, 115]
    Core 12 [28, 116]         [29, 117]         [30, 118]         [31, 119]
    Core 9  [32, 120]         [33, 121]         [34, 122]         [35, 123]
    Core 11 [36, 124]         [37, 125]         [38, 126]         [39, 127]
    Core 10 [40, 128]         [41, 129]         [42, 130]         [43, 131]
    Core 21 [44, 132]         [45, 133]         [46, 134]         [47, 135]
    Core 16 [48, 136]         [49, 137]         [50, 138]         [51, 139]
    Core 20 [52, 140]         [53, 141]         [54, 142]         [55, 143]
    Core 17 [56, 144]         [57, 145]         [58, 146]         [59, 147]
    Core 19 [60, 148]         [61, 149]         [62, 150]         [63, 151]
    Core 18 [64, 152]         [65, 153]         [66, 154]         [67, 155]
    Core 28 [68, 156]         [69, 157]         [70, 158]         [71, 159]
    Core 24 [72, 160]         [73, 161]         [74, 162]         [75, 163]
    Core 27 [76, 164]         [77, 165]         [78, 166]         [79, 167]
    Core 25 [80, 168]         [81, 169]         [82, 170]         [83, 171]
    Core 26 [84, 172]         [85, 173]         [86, 174]         [87, 175]

## CentOS 7 Release Info

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

# Format Your Data Partitions

Create physical volumes and volume groups with:

    pvcreate <NVMe drive>
    vgcreate data <List of NVMe Drives>

**NOTE:** I only did this on the NVMe drives.

To create the logical volume I used:

    lvcreate -l 100%FREE -i7 -I128 -n data data

To format the drive I used:

    mkfs.ext4 -F -b 4096 -E discard,stride=16,stripe-width=256 # This was the 12 SAS SSDs I had in a RAID
    mkfs.ext4 -F -b 4096 -E discard,stride=16,stripe-width=256 /dev/mapper/data-data # This was the NVMes I tied together with LVM
    mkfs.ext4 -F -b 4096 -E discard,stride=16,stripe-width=256 /dev/mapper/data2-data2
    mount -o rw,auto,discard /dev/mapper/data-data /data
    mount -o rw,auto,discard /dev/sda /raiddata/
    mount -o rw,auto,discard /dev/mapper/data2-data2 /data2
    echo noop > /sys/block/sda/queue/scheduler

# Install NapaTech Driver

## Install Driver

1. Download the [Napatech software](https://supportportal.napatech.com/index.php?/selfhelp/view-article/Link%E2%84%A2-Capture-Software-11.9.0-release-for-Linux/580) from here
2. Run `yum groupinstall "Development Tools" && yum install -y kernel-devel wget gettext-devel openssl-devel perl-CPAN perl-devel zlib-devel pciutils && yum install -y https://centos7.iuscommunity.org/ius-release.rpm && yum remove -y git && yum install -y git2u-all`
3. Unzip and run `package_install_3gd.sh`
4. Run the following commands:

        /opt/napatech3/bin/ntload.sh
        /opt/napatech3/bin/ntstart.sh

# Install n2disk and ntop

## Perform Installation

1. Install epel with `yum install -y epel-release`
2. Erase the zeromq3 package with `yum erase zeromq && yum clean all && yum update -y && reboot`
3. Pull ntop repo with `wget http://packages.ntop.org/centos-stable/ntop.repo -O /etc/yum.repos.d/ntop.repo`
4. Install required packages with `yum install -y pfring-dkms pfring n2disk nprobe ntopng ntopng-data cento pfring-drivers-zc-dkms redis hiredis-devel`

## Configure n2disk

1. Create backup of the the NapaTech ini file `cp /opt/napatech3/config/ntservice.ini /opt/napatech3/config/ntservice.ini.bak`
2. Update /opt/napatech3/config/ntservice.ini with the following values:

        TimestampFormat = PCAP_NS
        PacketDescriptor = PCAP
        HostBufferSegmentSizeRx = 4

TODO change these lines see notes for help

HostBuffersRx = [16,16,0],[16,16,1]
HostBuffersTx = [16,16,0],[16,16,1]

3. You will need to start and stop the ntservice for these changes to take effect with:

        /opt/napatech3/bin/ntstop.sh
        /opt/napatech3/bin/ntstart.sh


## Perform Configuration Zero Copy Driver

4. Edit the pfring configuration file with `vim /etc/pf_ring/interfaces.conf` and add your configuration.

        MANAGEMENT_INTERFACES="em1"
        CAPTURE_INTERFACES="nt:0"

5. Open the file `/etc/ntopng/ntopng.conf`. If you do not have a license add `--community` to the end
6. Configure the firewall to accept connections to ntopng with: `firewall-cmd --zone=public --permanent --add-port=3000/tcp && firewall-cmd --reload`
7. Enable and start services with:

        systemctl enable redis.service
        systemctl enable ntopng.service
        systemctl enable pf_ring
        systemctl start redis.service
        systemctl start ntopng.service
        systemctl start pf_ring

8. Make sure the services are running correctly with:

        systemctl status redis.service
        systemctl status ntopng.service
        systemctl status pf_ring

## Configure License

1. Run `zcount -i nt:0` and note the serial number
2. Output n2disk license to `/etc/n2disk.license`
3. Output ntopng license to `/etc/ntopng.license`

# Useful Tips

## Hardware Filtering

Napatech NICs support full-blown hardware filtering out of the box. Thanks to nBPF we convert BPF expressions to hardware filters. This feature is supported transparently, and thus all PF_RING/libpcap-over-PF_RING can benefit from it.

Example:

    pfcount -i nt:3 -f "tcp and port 80 and src host 192.168.1.1"

## Hostbuffer Notes

HostBuffersRx = [16,2048,0],[16,2048,1],[16,2048,2],[16,2048,3]
HostBuffersTx = [16,2048,0],[16,2048,1],[16,2048,2],[16,2048,3]

First number is the number of host buffers
Second number is the size of the host buffers
Third number is the NUMA node

You have to have one set of numbers for each NUMA node.

## Testing Transmit Speed

    ./pktgen -p 1 -r 10G

## Testing the PCAP transmit speed

To test to see if the Napatech card is up and running run this command:

    ./pfcount -i nt:0
    ./monitoring

You can press t to switch stats between receive and transmit.

## Testing Receive

    chmod -R 777 /data
    rm /tmp/*-none\.* 2>/dev/null; while true; do grep 'Dropped:\|Slow.*:' -C50 /proc/net/pf_ring/stats/* 2>/dev/null; cp /proc/net/pf_ring/stats/*none* /tmp 2>/dev/null; sleep 1; done
    
## NUMA Lookup

Run `lscpu`

# Things we tried:

We used the ![](./cpu_layout.py) to list the cpu layout and determine where we wanted to run what threads.

Tests 1-6 were with the default settings for a RAID0 partition on Linux at setup time.

#### Test 1

This is running at 100Gb/s generation

    n2disk -a -v -l  -o /<Storage path> -x $(date +%s.) -i nt:0

This seemed to dump everything to one thread. We maxed out and had ~82% packet loss. 

##### Test 2

This is running at 100Gb/s generation

    n2disk -a -v -l  -o /data/ -x $(date +%s.) -i nt:0 -n 5000 -m 10000 -p $((4*1024)) -b $((12*1024)) -C 4096 -c 32 -z 2,3,4,5,6,7 -Z -w 16,17,18,19,20,20,21 -S 22

Throughput results:

    [root@r940 bin]# cat /proc/net/pf_ring/stats/*none*
    Duration:          0:00:00:53:022
    Throughput:        2.12 Mpps    17.65 Gbps
    Packets:           78780625
    Filtered:          78780625
    Dropped:           518512807
    Bytes:             81931850000
    DumpedBytes:       71137406724
    DumpedFiles:       17
    SlowSlavesLoops:   0
    SlowStorageLoops:  432580
    CaptureLoops:      19532
    FirstDumpedEpoch:  0
    LastDumpedEpoch:   1574185087

Worked better but we got a warning saying the time thread was on a different core than the reader/writer threads.

#### Test 3

This is running at 100Gb/s generation

    n2disk -a -v -l  -o /data/ -x $(date +%s.) -i nt:0 -n 5000 -m 10000 -p $((4*1024)) -b $((12*1024)) -C 4096 -c 32 -z 2,3,4,5,6,7 -Z -w 16,17,18,19,20,20,21 -S 56

Worked better:

    19/Nov/2019 12:41:59 [n2disk.c:1109] Average Capture Throughput: 22.49 Gbit / 2.69 Mpps

#### Test 4

This is running at 100Gb/s generation

    n2disk -a -v -l  -o /data/ -x $(date +%s.) -i nt:0 -n 5000 -m 10000 -p $((4*1024)) -b $((12*1024)) -C 4096 -c 0 -z 8,12,16,20,24,28,32,26,40,44,48,52,56,60,64,68,72,76,80,84,88 -Z -w 92,96,100,104,108,112,116,120,124,128,132,136,140,144,148,152,156,160,164,168,172 -S 4

#### Test 5

This is running at 20Gb/s generation

    n2disk -a -v -l  -o /data/ -x $(date +%s.) -i nt:0 -n 5000 -m 10000 -p $((4*1024)) -b $((12*1024)) -C 4096 -c 0 -z 8,12,16,20,24,28,32,26,40,44,48,52,56,60,64,68,72,76,80,84,88 -Z -w 92,96,100,104,108,112,116,120,124,128,132,136,140,144,148,152,156,160,164,168,172 -S 4

Failed. We got a lot of packet loss.

#### Test 6

This is running at 10Gb/s generation

    n2disk -a -v -l  -o /data/ -x $(date +%s.) -i nt:0 -n 5000 -m 10000 -p $((4*1024)) -b $((12*1024)) -C 4096 -c 0 -z 8,12,16,20,24,28,32,26,40,44,48,52,56,60,64,68,72,76,80,84,88 -Z -w 92,96,100,104,108,112,116,120,124,128,132,136,140,144,148,152,156,160,164,168,172 -S 4

No packet drops.

#### Test 7

This is running at 20Gb/s generation

    n2disk -a -v -l  -o /data/ -x $(date +%s.) -i nt:0 -n 5000 -m 10000 -p $((4*1024)) -b $((12*1024)) -C 4096 -c 0 -z 8,12,16,20,24,28,32,26,40,44,48,52,56,60,64,68,72,76,80,84,88 -Z -w 92,96,100,104,108,112,116,120,124,128,132,136,140,144,148,152,156,160,164,168,172 -S 4

This was with a data partition formatting according to the above.

#### Test 8

    /opt/napatech3/bin/ntpl -e "Delete = All"

    /opt/napatech3/bin/ntpl -e "Setup[NumaNode=2] = StreamID == 0"
    # Repeat this for each stream ID. In our case 0-4

    ./profiling # use this to see traffic being received
    # N is the NUMA node that the profiler detects the traffic on

    /opt/napatech3/bin/ntpl -e "HashMode = Hash2TupleSorted"
    /opt/napatech3/bin/ntpl -e "Assign[StreamId=(0..3)] = port == 0"

The problem with this was that we couldn't get n2disk to listen on multiple interfaces.
It also didn't really give us a way to split the traffic across multiple reader threads.

#### Test 9

1. I made four directories, one for each n2disk process
2. I did the following:

        /opt/napatech3/bin/ntpl -e "Delete = All"

        /opt/napatech3/bin/ntpl -e "Setup[NumaNode=2] = StreamID == 0"
        # Repeat this for each stream ID. In our case 0-4

        /opt/napatech3/bin/ntpl -e "HashMode = Hash2TupleSorted"
        /opt/napatech3/bin/ntpl -e "Assign[StreamId=(0..3)] = port == 0"

        ./profiling # use this to see traffic being received
        # N is the NUMA node that the profiler detects the traffic on

3. Run the following commands:

        n2disk -a -v -l  -o /data/data0 -x $(date +%s.) -i nt:stream0 -n 5000 -m 10000 -p $((20*1024)) -b $((40*1024)) -C 4096 -c 120 -z 0,4,8,12,16,20,24,28 -Z -w 88,92,96,100,104,108,112,116 -S 32

        n2disk -a -v -l  -o /data/data1 -x $(date +%s.) -i nt:stream1 -n 5000 -m 10000 -p $((20*1024)) -b $((40*1024)) -C 4096 -c 121 -z 1,5,9,13,17,21,25,29 -Z -w 89,93,97,101,105,109,113,117 -S 33

        n2disk -a -v -l  -o /data/data2 -x $(date +%s.) -i nt:stream2 -n 5000 -m 10000 -p $((20*1024)) -b $((40*1024)) -C 4096 -c 156 -z 36,40,44,48,52,56,60,64 -Z -w 124,128,132,136,140,144,148,152 -S 68

        n2disk -a -v -l  -o /data/data3 -x $(date +%s.) -i nt:stream3 -n 5000 -m 10000 -p $((20*1024)) -b $((40*1024)) -C 4096 -c 157 -z 37,41,45,49,53,57,61,65 -Z -w 125,129,133,137,141,145,149,153 -S 69

        -a : Archive pcap file (rename to .old) instead of overwriting if already present on disk.
        -v : Verbose.
        -o : Directory where dump files will be saved (multiple -o can be specified)
        -x : Dump file prefix.
        -i : Ingress packet device.
        -n : Max number of nested dump sub-directories.
        -m : Max number of files before restarting file name.
        -p : Max pcap file length (MBytes).
        -b : Buffer length (MBytes).
        -C : Size (KB) of the chunk written to disk (must be multiple of 4096). Default: 64 KB.
        -c : Bind the reader thread to the specified core.
        -z : Enable multithread compression and/or indexing and bind thread(s) to the specified core ids (e.g. 0,1,2,3) (mandatory with indexing on Napatech cards)
        -Z : Compute index on the thread(s) used for compression (-z) instead of using the capture thread(s).
        -w : Bind the writer thread(s) to the specified core ids. A comma-separated list of cores (e.g. 0,1,2,3) should be specified in case of multiple dump directories (-o).
        -S : Enable time pulse thread (optimise sw packet timestamping) and bind it to the specified core.

With this setup I was able to get 70Gb/s. I tested 100Gb/s and got drops. Did not
perform further testing to narrow down exactly how much traffic I could push before
moving on to the next test.

#### Test 10

1. I made seven directories, one for each n2disk process. 4 assigned to the NVMe drives and 3 assigned to the SAS SSD RAID
2. I did the following:

        /opt/napatech3/bin/ntpl -e "Delete = All"

        /opt/napatech3/bin/ntpl -e "Setup[NumaNode=2] = StreamID == 0"
        # Repeat this for each stream ID. In our case 0-6

        /opt/napatech3/bin/ntpl -e "HashMode = Hash2TupleSorted"
        /opt/napatech3/bin/ntpl -e "Assign[StreamId=(0..6)] = port == 0"

        ./profiling # use this to see traffic being received
        # N is the NUMA node that the profiler detects the traffic on
        watch cat /proc/net/pf_ring/stats/*none*

3. Run the following commands:

        n2disk -a -v -l  -o /data/data0 -x $(date +%s.) -i nt:stream0 -n 5000 -m 10000 -p $((20*1024)) -b $((40*1024)) -C 4096 -c 120 -z 0,4,8,12,16,20,24,28 -Z -w 88,92,96,100,104,108,112,116 -S 32

        n2disk -a -v -l  -o /data/data1 -x $(date +%s.) -i nt:stream1 -n 5000 -m 10000 -p $((20*1024)) -b $((40*1024)) -C 4096 -c 121 -z 1,5,9,13,17,21,25,29 -Z -w 89,93,97,101,105,109,113,117 -S 33

        n2disk -a -v -l  -o /data/data2 -x $(date +%s.) -i nt:stream2 -n 5000 -m 10000 -p $((20*1024)) -b $((40*1024)) -C 4096 -c 156 -z 36,40,44,48,52,56,60,64 -Z -w 124,128,132,136,140,144,148,152 -S 68

        n2disk -a -v -l  -o /data/data3 -x $(date +%s.) -i nt:stream3 -n 5000 -m 10000 -p $((20*1024)) -b $((40*1024)) -C 4096 -c 157 -z 37,41,45,49,53,57,61,65 -Z -w 125,129,133,137,141,145,149,153 -S 69

        n2disk -a -v -l  -o /raiddata/data0 -x $(date +%s.) -i nt:stream4 -n 5000 -m 10000 -p $((20*1024)) -b $((40*1024)) -C 4096 -c 123 -z 3,7,11,15,19,23,27,31 -Z -w 91,95,99,103,107,111,115,119 -S 35

        n2disk -a -v -l  -o /raiddata/data1 -x $(date +%s.) -i nt:stream5 -n 5000 -m 10000 -p $((20*1024)) -b $((40*1024)) -C 4096 -c 159 -z 39,43,47,51,55,59,63,67 -Z -w 127,131,135,139,143,147,151,155 -S 71

        n2disk -a -v -l  -o /raiddata/data2 -x $(date +%s.) -i nt:stream6 -n 5000 -m 10000 -p $((20*1024)) -b $((40*1024)) -C 4096 -c 174 -z 54,58,62,66,70,74,78,82 -Z -w 142,146,150,154,158,162,166,170 -S 86

        -a : Archive pcap file (rename to .old) instead of overwriting if already present on disk.
        -v : Verbose.
        -o : Directory where dump files will be saved (multiple -o can be specified)
        -x : Dump file prefix.
        -i : Ingress packet device.
        -n : Max number of nested dump sub-directories.
        -m : Max number of files before restarting file name.
        -p : Max pcap file length (MBytes).
        -b : Buffer length (MBytes).
        -C : Size (KB) of the chunk written to disk (must be multiple of 4096). Default: 64 KB.
        -c : Bind the reader thread to the specified core.
        -z : Enable multithread compression and/or indexing and bind thread(s) to the specified core ids (e.g. 0,1,2,3) (mandatory with indexing on Napatech cards)
        -Z : Compute index on the thread(s) used for compression (-z) instead of using the capture thread(s).
        -w : Bind the writer thread(s) to the specified core ids. A comma-separated list of cores (e.g. 0,1,2,3) should be specified in case of multiple dump directories (-o).
        -S : Enable time pulse thread (optimise sw packet timestamping) and bind it to the specified core.

With this setup I was able to get 70Gb/s. I tested 100Gb/s and got drops. Did not
perform further testing to narrow down exactly how much traffic I could push before
moving on to the next test.



## Compile PF_RING Driver (PROBABLY NOT NECESSARY)

**NOTE** There is a note in the documentation saying that installing from repository comes with NapaTech support.

1. Move to opt run `git clone https://github.com/ntop/PF_RING.git`
2. Move into the directory and run `cd PF_RING/kernel && make && sudo insmod pf_ring.ko`
3. Next run `cd ../userland/lib && ./configure && make`
4. Next run `cd ../libpcap && ./configure && make`
5. Next run `cd ../examples && make`