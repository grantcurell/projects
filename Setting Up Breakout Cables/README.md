# Setting Up 100Gb/s Breakout Cables

## Helpful Links

[Dell OS10 Manual](https://downloads.dell.com/manuals/common/os10_enterprise-ug_en-us.pdf)

## Platform Information

### Physical Configuration

![](images/physical.jpg)

### OS Information

    OS10# show version
    Dell EMC Networking OS10-Enterprise
    Copyright (c) 1999-2019 by Dell Inc. All Rights Reserved.
    OS Version: 10.4.2.2
    Build Version: 10.4.2.2.265
    Build Time: 2019-01-14T15:15:14-0800
    System Type: S4112F-ON
    Architecture: x86_64
    Up Time: 00:13:36

## Configure Management Port

See [Configure Management Interface on Dell OS10](/README.md#configure-managment-interface-on-dell-os10)

## Configure Breakout Port

Run:

    OS10(config)# feature auto-breakout
    OS10# write memory

That's it. I really thought it would be harder.
