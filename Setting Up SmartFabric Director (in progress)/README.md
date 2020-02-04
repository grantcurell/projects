# Setting Up SmartFabric Director

## Helpful Links

[SmartFabric Director Download Page](https://www.force10networks.com/CSPortal20/Software/SmartFabric.aspx)

[SmartFabric Director User's Guide](https://topics-cdn.dell.com/pdf/smartfabric-os10-5-0_en-us.pdf)

## My Configuration

### Dell 4112F-ON

    Dell EMC Networking OS10 Enterprise
    Copyright (c) 1999-2020 by Dell Inc. All Rights Reserved.
    OS Version: 10.5.0.4
    Build Version: 10.5.0.4.638
    Build Time: 2020-01-30T21:08:56+0000
    System Type: S4112F-ON
    Architecture: x86_64
    Up Time: 01:33:00

### Dell OS10 Running in GNS3

I used the GNS3 VM and tied the switch with a virtual cloud into my actual infrastructure.

    Dell EMC Networking OS10 Enterprise
    Copyright (c) 1999-2019 by Dell Inc. All Rights Reserved.
    OS Version: 10.5.0.0
    Build Version: 10.5.0.0.326
    Build Time: 2019-08-07T00:12:30+0000
    System Type: S5248F-VM
    Architecture: x86_64
    Up Time: 00:32:14

## Setup

1. Download, extract, upload to vCenter (or ESXi)
2. Fill in network settings.
3. When it finishes importing, keep in mind that the username and password is:
   1. Username: admin@sfd.local
   2. Password: The password you set

## Problems Encountered

### On the 4112F-ON

These were taken from the physical switch running 10.5.0.4.638

I have confirmed I am in full switch mode:

    OS10# show switch-operating-mode

    Switch-Operating-Mode : Full Switch Mode

- Page 10 step 6 of [the manual](https://downloads.dell.com/manuals/all-products/esuprt_networking_int/esuprt_networking_mgmt_software/smart-fabric-director_users-guide_en-us.pdf) does not work. There is no cert command.
- Page 11 step 1 of [the manual](https://downloads.dell.com/manuals/all-products/esuprt_networking_int/esuprt_networking_mgmt_software/smart-fabric-director_users-guide_en-us.pdf) does not work. There is no switch-port-profile command.

### With the VM

See [bug notes](./BUG.md).