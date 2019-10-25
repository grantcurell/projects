# Notes for Creating Traffic Generator

## Environment

### VMWare

I built out a VM on my vSphere cluster running 6.7.0.

### Guest OS

I used CentOS 7

Info:

    Last login: Thu Oct 24 13:13:56 2019 from 192.168.1.6
    [root@centos ~]# cat /etc/*-release
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



## Optional - Install VMWare Tools

I like using VMWare tools when I have a GUI because it makes the experience a bit
smoother.

Install by doing the following:

1. `yum install -y kernel-devel`
2. Make sure your host has a CD drive
3. Mount the VMWare tools disk image in the vSphere client
4. Run `mount /dev/cdrom /mount`
5. Copy the vmware tools installation file somewhere
6. Extract it
7. Run the installer file

## Configuration of VM Networking

I used a dedicated physical interface connected directly to a virtual switch
with all security settings disabled and fed that directly into NIC2 of my packet
generator.

## Installation of Packet Sender

1. To install Packet Sender you need a package management solution called snap. Follow instructions [here](https://snapcraft.io/docs/installing-snap-on-centos). I rebooted at the end of the instructions.
2. Packet Sender requires a GUI. I installed that with `yum -y groups install "GNOME Desktop"`
3. Download Packet Sender from [here](https://packetsender.com/download#show)
4. After you download the file append the execute permission to it with `chmod a+x [filename]`
5. Install it with `snap install packetsender`
6. 