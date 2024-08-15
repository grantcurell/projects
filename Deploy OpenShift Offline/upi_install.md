# User Provisioned Infrastructure (UPI) Install

**The bootstrap host only applies to versions 4.12 and older!**

- [User Provisioned Infrastructure (UPI) Install](#user-provisioned-infrastructure-upi-install)
  - [Some Notes on How Bootstrap Works](#some-notes-on-how-bootstrap-works)
  - [Example Architecture](#example-architecture)
  - [Setting Up Your Helper Machine](#setting-up-your-helper-machine)

## Some Notes on How Bootstrap Works

- The bootstrap machine will host resources the control plane servers will use
- During the bootstrap process the control plane nodes will stand up a temporary control plane which will be used to stand up the permanent control plane
- After the temporary control plane has completed its job the bootstrap host will shut down the temporary control plane machines, which will then reboot with the actual control plane. At this time the worker machines will boot up. We will join them into the cluster with certificate signing requests.

## Example Architecture

![](images/2024-08-14-13-40-08.png)

[Source](https://github.com/ryanhay/ocp4-metal-install)

1. You must build a bootstrap VM or physical machine running RHCOS with the following specs:
   1. 4 CPUs
   2. 16GB RAM
   3. 100 GB storage

## Setting Up Your Helper Machine

The helper machine is separate from bootstrap. This is wherever you have DNS and all your services. In my case, I also made my quay registry the same machine as my helper machine so that was all co-located.

```bash
# Install required software
sudo dnf update -y
sudo dnf install -y httpd haproxy nfs-utils

# Change the listening port for httpd
sudo sed -i 's/Listen 80/Listen 0.0.0.0:8080/' /etc/httpd/conf/httpd.conf

# Configure the firewall
sudo firewall-cmd --add-service=http --zone=public --permanent  # web services hosted on worker nodes
sudo firewall-cmd --add-service=https --zone=public --permanent # web services hosted on worker nodes
sudo firewall-cmd --add-port=8080/tcp --zone=public --permanent # our web server
sudo firewall-cmd --add-port=6443/tcp --zone=public --permanent # kube-api-server on control plane nodes
sudo firewall-cmd --add-port=22623/tcp --zone=public --permanent # machine-config server
sudo firewall-cmd --add-port=9000/tcp --zone=public --permanent # HAProxy stats
sudo firewall-cmd --zone=internal --add-service mountd --permanent # for nfs
sudo firewall-cmd --zone=internal --add-service rpc-bind --permanent # for nfs
sudo firewall-cmd --zone=internal --add-service nfs --permanent # for nfs
sudo firewall-cmd --reload
sudo firewall-cmd --list-all

# Start services
sudo setsebool -P haproxy_connect_any 1 # SELinux name_bind access
sudo systemctl enable haproxy
sudo systemctl start haproxy
sudo systemctl status haproxy

# Configure NFS share
sudo mkdir -p /shares/registry
sudo chown -R nobody:nobody /shares/registry
sudo chmod -R 777 /shares/registry

##############################################
# REPLACE WITH YOUR IP RANGE                 #
##############################################
# Note: this may not run if you do this as user. You may have to VIM it.
sudo echo "/shares/registry  10.10.25.0/24(rw,sync,root_squash,no_subtree_check,no_wdelay)" > /etc/exports
##############################################
# REPLACE WITH YOUR IP RANGE                 #
##############################################

# Export the NFS share
sudo exportfs -rv

# Start NFS
sudo systemctl enable nfs-server rpcbind
sudo systemctl start nfs-server rpcbind nfs-mountd

# Generate SSH key
ssh-keygen
```