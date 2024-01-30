#!/bin/bash

modprobe uio && insmod /opt/dpdk-19.08/install/lib/modules/4.18.0-147.el8.x86_64/extra/dpdk/igb_uio.ko
/opt/dpdk-19.08/install/share/dpdk/usertools/dpdk-devbind.py --bind=igb_uio eno1
/opt/dpdk-19.08/install/share/dpdk/usertools/dpdk-setup.sh