# OS10 Password Recovery Bug

## YouTube Reproduction

https://youtu.be/b5MJiLTl9KE

## Update

It looks like the instructions are set up to take care of this, but they need to be updated - ![](https://www.dell.com/support/manuals/us/en/04/networking-s4148f-on/smartfabric-os-user-guide-10-5-1/recover-linux-password?guid=guid-4263f287-20e8-4f25-8092-75a532f0c7ea&lang=en-us) step 8 tells you to run a `sed` command that looks like it is targeted at reloving the problem, but it only tells you to run it on 10.5.1.0. When I went through this procedure I just ignored it because the customer was on 10.5.1.3

## Description

Follow [Password recovery instructions](https://www.dell.com/support/manuals/us/en/04/networking-s4148f-on/smartfabric-os-user-guide-10-5-1/recover-linux-password?guid=guid-4263f287-20e8-4f25-8092-75a532f0c7ea&lang=en-us) to get into the switch at boot.

During step 9:

`/opt/dell/os10/bin/recover_linuxadmin_password.sh` produces `mount: special device /dev/mapper/OS10-CONFIG does not exist`.

This is due to a previous configuration of OS10 when tho configuration was mounted on its own logical volume. It has since been moved to SYSROOT.

Removing the below lines resolves the issue:

![](images/lines.jpg)
