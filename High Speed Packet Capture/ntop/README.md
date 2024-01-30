
# Helpful Materials

[Drill Down Deeper: Using ntopng to Zoom In, Filter Out and Go Straight to the Packets](https://www.ntop.org/n2disk/drill-down-deeper-using-ntopng-to-zoom-in-filter-out-and-go-straight-to-the-packets/)

[Traffic Recording Manual](https://www.ntop.org/guides/ntopng/traffic_recording.html)

# Configuration

## Hardware

Tracewell TFX2HE with 1 passthrough module, 1 switch module.



## Operating System Version

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

## Kernel Version

    Linux ntopdemo.lan 3.10.0-1062.4.1.el7.x86_64 #1 SMP Fri Oct 18 17:15:30 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux

# Install n2disk and ntop

## Perform Installation

1. Install epel with `yum install -y epel-release`
2. Erase the zeromq3 package with `yum erase zeromq && yum clean all && yum update -y && reboot`
3. Pull ntop repo with `wget http://packages.ntop.org/centos-stable/ntop.repo -O /etc/yum.repos.d/ntop.repo`
4. Install required packages with `yum install pfring-dkms pfring n2disk nprobe ntopng ntopng-data cento pfring-drivers-zc-dkms redis hiredis-devel`

## Perform Configuration Zero Copy Driver

1. List interfaces with `pf_ringcfg --list-interfaces`
2. Configure the driver with `pf_ringcfg --configure-driver i40e`
3. Set promiscuous mode on the interface in question with `/sbin/ip link set em1 promisc on`
4. Edit the pfring configuration file with `vim /etc/pf_ring/interfaces.conf` and add your configuration.

        MANAGEMENT_INTERFACES="<YOUR_MANAGEMENT_INTERFACE>"
        CAPTURE_INTERFACES="<YOUR_CAPTURE_INTERFACE>"

5. Open the file `etc/ntopng/ntopng.conf`. If you do not have a license add `--community` to the end
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

# Performing Filtering

