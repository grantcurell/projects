# Configure kdump with SSH

- [Configure kdump with SSH](#configure-kdump-with-ssh)
  - [Test System](#test-system)
  - [Setup for SSH](#setup-for-ssh)
    - [On the Crashing System](#on-the-crashing-system)
  - [Test kdump](#test-kdump)
  - [Interpreting the Files](#interpreting-the-files)

## Test System

```bash
NAME="Rocky Linux"
VERSION="9.4 (Blue Onyx)"
ID="rocky"
ID_LIKE="rhel centos fedora"
VERSION_ID="9.4"
PLATFORM_ID="platform:el9"
PRETTY_NAME="Rocky Linux 9.4 (Blue Onyx)"
ANSI_COLOR="0;32"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:rocky:rocky:9::baseos"
HOME_URL="https://rockylinux.org/"
BUG_REPORT_URL="https://bugs.rockylinux.org/"
SUPPORT_END="2032-05-31"
ROCKY_SUPPORT_PRODUCT="Rocky-Linux-9"
ROCKY_SUPPORT_PRODUCT_VERSION="9.4"
REDHAT_SUPPORT_PRODUCT="Rocky Linux"
REDHAT_SUPPORT_PRODUCT_VERSION="9.4"
Rocky Linux release 9.4 (Blue Onyx)
Rocky Linux release 9.4 (Blue Onyx)
Rocky Linux release 9.4 (Blue Onyx)
```

## Setup for SSH

### On the Crashing System

- Install kdump

```bash
dnf install -y kexec-tools
```

- To be sure you are at the default config run `kdumpctl reset-crashkernel --kernel=ALL`
- Configure kdump with `/vim /etc/kdump.conf` and add the below:

```bash
# Specify the path where the vmcore should be saved on the remote machine
path /var/crash

# Specify the SSH target
ssh root@172.16.192.128

# Specify the SSH key (optional, if not using the default key)
sshkey /root/.ssh/id_rsa

# Core collector to capture the dump, with the -F option
core_collector makedumpfile -F -l --message-level 7 -d 31
```

- Make sure the grub config is set up correctly in `/etc/default/grub`. You should see something like the below.

```bash
GRUB_CMDLINE_LINUX="crashkernel=1G-4G:192M,4G-64G:256M,64G-:512M rd.lvm.lv=rl/root"
```

**What this means**
- **crashkernel**: This parameter reserves memory for the crash kernel, which is used by kdump to capture memory dumps in case of a crash.
- **1G-4G:192M**: For systems with total RAM between 1 GB and 4 GB, 192 MB is reserved for the crash kernel.
- **4G-64G:256M**: For systems with total RAM between 4 GB and 64 GB, 256 MB is reserved for the crash kernel.
- **64G-:512M**: For systems with more than 64 GB of RAM, 512 MB is reserved for the crash kernel.

- You can make sure kdump is running with `systemctl status kdump`
- Next we need to make sure SSH is setup. Do the following on the machine you are debugging:

```bash
ssh-keygen -t rsa -b 2048
ssh-copy-id root@172.16.192.128  # Update this with your information
ssh root@172.16.192.128  # Run a quick test to make sure it worked
```

## Test kdump

I triggered a kernel dump with `echo c > /proc/sysrq-trigger`

## Interpreting the Files

- Install `crash` with `dnf install -y crash`
- The dumps show up on the remote host:

```
[root@patches 172.16.192.129-2024-07-23-15:13:11]# ls
download.sh  kernel-debuginfo-5.14.0-427.24.1.el9_4.x86_64.rpm  kexec-dmesg.log  vmcore-dmesg.txt  vmcore.flat
```

- What did suck a bit is that Rocky appears to have a bug in their build system where `kernel-debuginfo-common` is missing from their build platform so I haven't had the chance to go through the dumps. See [this bug](https://forums.rockylinux.org/t/rocky-9-1-blue-onyx-missing-kernel-debuginfo-common-x86-64/8132). 
  - Also unfortunately, the fix the dev in that post mentioned, doesn't work; [I tried it](https://forums.rockylinux.org/t/rocky-9-4-still-missing-kernel-debuginfo-common/15169). Even manually [searching the repository](https://download.rockylinux.org/pub/rocky/9.4/BaseOS/x86_64/debug/tree/Packages/k/) I couldn't find the right package so I'll need to test on RHEL or something.