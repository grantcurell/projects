# Testing GPUDirect RDMA

## Test Scenario

TODO

## Lab Configuration

### Hardware Configuration

TODO

### RHEL Version

```
NAME="Red Hat Enterprise Linux"
VERSION="8.4 (Ootpa)"
ID="rhel"
ID_LIKE="fedora"
VERSION_ID="8.4"
PLATFORM_ID="platform:el8"
PRETTY_NAME="Red Hat Enterprise Linux 8.4 (Ootpa)"
ANSI_COLOR="0;31"
CPE_NAME="cpe:/o:redhat:enterprise_linux:8.4:GA"
HOME_URL="https://www.redhat.com/"
DOCUMENTATION_URL="https://access.redhat.com/documentation/red_hat_enterprise_linux/8/"
BUG_REPORT_URL="https://bugzilla.redhat.com/"

REDHAT_BUGZILLA_PRODUCT="Red Hat Enterprise Linux 8"
REDHAT_BUGZILLA_PRODUCT_VERSION=8.4
REDHAT_SUPPORT_PRODUCT="Red Hat Enterprise Linux"
REDHAT_SUPPORT_PRODUCT_VERSION="8.4"
Red Hat Enterprise Linux release 8.4 (Ootpa)
Red Hat Enterprise Linux release 8.4 (Ootpa)
```

## Installation

1. Download MLNX_OFED drivers from https://www.mellanox.com/products/infiniband-drivers/linux/mlnx_ofed
   1. MLNX_OFED is version dependent. I suggest you use  `subscription-manager release --set=8.4` to ensure your version of RHEL stays at the version for which MLNX_OFED was compiled
2. Upload the ISO to the target box
3. Run:

```bash
dnf group install "Development Tools" -y
dnf install -y tk tcsh tcl gcc-gfortran kernel-modules-extra gcc-g++ gdb rsync ninja-build make zip
mount MLNX* /mnt
cd /mnt
./mlnxofedinstall
```

4. 

