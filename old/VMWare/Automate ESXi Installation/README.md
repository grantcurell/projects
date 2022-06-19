# Automating ESXi Installation

This Ansible playbook runs on CentOS. It will create a server which
allows you to install ESXi automatically via PXE boot and Kickstart.

For more information on ESXi's Kickstart capabilities see [this link](https://docs.vmware.com/en/VMware-vSphere/6.5/com.vmware.vsphere.install.doc/GUID-341A83E4-2A6C-4FB9-BE30-F1E19D12947F.html)

## Prerequisites

### Install CentOS

You can download and install CentOS [here](https://www.centos.org/download/)

The installation services used by this program are very lightweight so you can
install on just about anything. A 12GB hard drive, 2GB RAM, and a single processor
are enough for what we are doing.

Go ahead and install CentOS on whatever you like, the only requirement is that
it must be reachable at layer 2 by the ESXi hosts you want to install.

### Install Ansible and git

Before continuing you will need to install Ansible on your host by running `yum install -y ansible git`.

### Clone the Repo

I typically use opt for optional programs. You may install wherever you like, but
in this guide I will use opt. Clone the repo with: `git clone https://github.com/grantcurell/esxi-autoinstall.git`

Move into the esxi-autoinstall directory with `cd /opt/esxi-autoinstall`

## Configure the Inventory File

Ansible is controlled by what is called an inventory file. This inventory file contains
all the configuration settings which will be used by Ansible. In our case, we will
need to populate this with the settings we wish ESXi to have after installation.

The inventory file is called *inventory.yml*

You will need to fill in the following values:

- dns
- dhcp_start
- dhcp_end
- gateway
- netmask
- domain
- root_password
- server_ip
- iso_esxi_pth
- iso_esxi_checksum

Finally you will also need to fill in the host information. These are the hosts on
which you would like to install ESXi. 

### Boot Drives

Most of the values are self explanatory however, boot_drive and data_drives may 
be a bit confusing. These options allow you to tell Ansible where to install ESXi
and on which disks to configure datastores. The official documentation on how ESXi
names drives is [here](https://docs.vmware.com/en/VMware-vSphere/6.5/com.vmware.vsphere.install.doc/GUID-E7274FBA-CABC-43E8-BF74-2924FD3EFE1E.html)
The disks are in the order in which ESXi detects them. To get the order you may
have to manually install ESXi on a system. You can make an educated guess from
the BIOS menu or if you have something like iDrac you can look at the order of the
disks on the RAID controller (assuming you have one).

## Running the Code

Once you are finished editing the *inventory.yml* file, `cd` to the root of the esxi-autoinstall
directory and run `make`. This will run the makefile in the directory. You can
see what it is doing by examining the file called *Makefile*

## Advanced

You may want the installer to do some crazier things. The kickstart script used
to configure the hosts can be modified to run arbitrary esxcli commands. You're
on your own if you want to go this route, but you can find the kickstart file
with the esxcli commands in *roles/profiles/templates/ks.cfg.j2*.