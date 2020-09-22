# Password Reset Bug

## YouTube Reproduction

https://youtu.be/b5MJiLTl9KE

## Description

`/opt/dell/os10/bin/recover_linuxadmin_password.sh` produces `mount: special device /dev/mapper/OS10-CONFIG does not exist`.

This is due to a previous configuration of OS10 when tho configuration was mounted on its own logical volume. It has since been moved to SYSROOT.

Removing the below lines resolves the issue:

![](images/lines.jpg)