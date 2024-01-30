# Create Kickstart Server on Fedora

## Files

All files housed [here](https://github.com/grantcurell/grantcurell.github.io/tree/master/docs/Create%20Kickstart%20Server%20on%20Fedora)

## Intro

This Ansible playbook runs on CentOS. It will create a server which
allows you to install Fedora automatically via PXE boot and Kickstart.

For more information on Fedora's Kickstart capabilities see [this link](https://docs.fedoraproject.org/en-US/fedora/rawhide/install-guide/appendixes/Kickstart_Syntax_Reference/#appe-kickstart-syntax-reference)

## Useful Information

[How to set up Fedora Kickstart](https://docs.fedoraproject.org/en-US/fedora/rawhide/install-guide/advanced/Network_based_Installations/)

[The Fedora Mirror I used](http://ftp.muug.mb.ca/pub/fedora/linux/releases/31/Everything/x86_64/os/Packages/)

https://gist.github.com/andrewwippler/b636cdb68249ab5ffb67b4d8693a780b

## Prerequisites

Note: If you use a VM it will need at least 90GB of space.

### Install CentOS

You can download and install CentOS [here](https://www.centos.org/download/)

The installation services used by this program are very lightweight so you can
install on just about anything. A 12GB hard drive, 2GB RAM, and a single processor
are enough for what we are doing.

Go ahead and install CentOS on whatever you like, the only requirement is that
it must be reachable at layer 2 by the Fedora hosts you want to install.

### Install Ansible and git

Before continuing you will need to install Ansible on your host by running `yum install -y ansible git`.

### Disable SELinux

Or set proper policies. Pick your poison. Since I only stood this thing up for as long as it took to kickstart I was
lazy and just disabled it. Sue me.

`setenforce 0`

I also updated this in `/etc/selniux/config`.

### Grab Image Files

You need to grab the image files for vmlinuz and initrd.img in order for Linux to boot properly. For Fedora grab them from
the below.

    wget https://download.fedoraproject.org/pub/fedora/linux/releases/31/Server/x86_64/os/images/pxeboot/vmlinuz -O /var/lib/tftpboot/vmlinuz
    wget https://download.fedoraproject.org/pub/fedora/linux/releases/31/Server/x86_64/os/images/pxeboot/initrd.img -O /var/lib/tftpboot/initrd.img
    wget http://fedora.mirrors.pair.com/linux/releases/31/Server/x86_64/os/images/install.img -O /var/www/html/iso/images/install.img

### Clone the Fedora Repositories

On a host of your choosing, run the following (update the 31 to the appropriate Fedora version):

    rsync http://ftp.muug.mb.ca/pub/fedora/linux/releases/31/Everything/x86_64/os/Packages/ /var/www/html/iso/Packages

Note: You will probably have to create the above directory.

You'll need 73 GB free to sync the packages. You will also need to grab the file in [the repodata directory](http://ftp.muug.mb.ca/pub/fedora/linux/releases/31/Everything/x86_64/os/repodata/) called ending with comps.xml. You can see its exact name in repomd.xml.

Set it and forget it because it will be a bit while this all downloads. After you are downloading run:

    createrepo -g <THE COMPS FILE YOU DOWNLOADED> /var/www/html/iso/Packages

### Clone the Repo

I typically use opt for optional programs. You may install wherever you like, but
in this guide I will use opt. Clone the repo with: `git clone https://github.com/grantcurell/Fedora-autoinstall.git`

Move into the Fedora-autoinstall directory with `cd /opt/Fedora-autoinstall`

## Configure the Inventory File

Ansible is controlled by what is called an inventory file. This inventory file contains
all the configuration settings which will be used by Ansible. In our case, we will
need to populate this with the settings we wish Fedora to have after installation.

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
- iso_fedora_pth
- iso_fedora_checksum

Finally you will also need to fill in the host information. These are the hosts on
which you would like to install Fedora. 

### Boot Drives

Most of the values are self explanatory however, boot_drive and data_drives may 
be a bit confusing. These options allow you to tell Ansible where to install Fedora
and on which disks to configure datastores. The official documentation on how Fedora
names drives is [here](https://docs.vmware.com/en/VMware-vSphere/6.5/com.vmware.vsphere.install.doc/GUID-E7274FBA-CABC-43E8-BF74-2924FD3EFE1E.html)
The disks are in the order in which Fedora detects them. To get the order you may
have to manually install Fedora on a system. You can make an educated guess from
the BIOS menu or if you have something like iDrac you can look at the order of the
disks on the RAID controller (assuming you have one).

## Running the Code

Once you are finished editing the *inventory.yml* file, `cd` to the root of the Fedora-autoinstall
directory and run `make`. This will run the makefile in the directory. You can
see what it is doing by examining the file called *Makefile*

## CRITICAL: Change BIOS Settings

If you have NVMe drives and are trying to install Fedora, make sure you go into your BIOS and disable Intel Rapid Storage
Technology. If you do not, the NVMe drive will not appear and Anaconda will report that there are no disks available.

### (Optional) Make it so that all hosts receive dhcp

I intentionally left it set up so that only configured hosts would receive dhcpd to make sure no one nukes their network.
That said, if you want to make it so that all hosts receive dhcp edit `/etc/dhcp/dhcpd.conf` remove the line `deny unknown-clients`
and then add the line `filename "uefi/BOOTX64.EFI";` in the `subnet {}` directive. You will have to repeat this if you
run make again. After you are done, run `systemctl restart dhcpd`

## Make the Repository Available to Your Clients

Add a file called `local.repo` in `/etc/yum.repos.d/local.repo` with the following contents:

    [local]
    name=Local
    baseurl=http://192.168.1.121/iso/Packages
    enabled=1
    gpgcheck=0

## Advanced

### Importing Packages from Another System Minimally

#### Method 2 - Under Development

Say you want to create a new offline installer. What you'll have to do is go to a system that has all of the packages
you might want to use in your new image. You will then want to scrape all those packages so that you can then use them
on your new kickstart server. Do the following.

1. On the system that already has the packages run: `dnf list installed | cut -d ' ' -f 1 | tr '\r\n' ' ' | sed s/Installed//g`.
2. The above command gets a list of all packages on the system and outputs them space separated. You could pipe that into xargs, but I prefer to do this next part manually in case there are any packages that don't work. Copy the output of the above and paste it as an argument to `dnf download --resolve <YOUR_STUFF>`. That will download all the packages on the server and their dependencies.
3. If any packages do not resolve you can run `dnf list installed | cut -d ' ' -f 1 | tr '\r\n' ' ' | sed s/Installed//g | sed s/<PACKAGE_NAME_THAT_DIDNT_WORK>//g` to omit it from the list.
4. After you run make on the Kickstart server to run the above command, go to `/var/www/html/iso/packages/` and copy all of the packages to that directory. You can use something like `scp * root@192.168.1.121:/var/www/html/iso/packages/` to do this.
5. When you are done, browse to your server using Chrome or something and make sure all the packages are available. Ex: http://192.168.1.121/iso/packages/

## Info on the Kickstart Process

Kickstart has a lot of black magic going on. So below I give a high level overview of what's happening.

1. Server boots and you tell it to boot with PXE.
2. PXE will then send out a DHCP request. The DHCP server that responds should be your kickstart server (typically) and it will have a few extra options set. Namely there should be a line that looks like the following:

        # This line tell sth server to reach out over TFTP and grab the uefi/BOOTX64.EFI file. This file is a binary
        # file which tells the server how to boot. It will be specific to your distro and you should generally get
        # it from the ISO which you want to install. The path is a relative path against the TFTP root directory.
        filename "uefi/BOOTX64.EFI";

3. Next, if you are doing UEFI, the server will search for a series of file names in the TFTP server's UEFI directory until it finds a boot menu profile that matches. I couldn't find documentation on it, but if you watch `/var/log/messages` you can actually see it try different as show below. It progresses through listed host MAC addresses first, then the IP address in hex format, and at the very end tries the default grub.cfg. To get maximum output you can add `server_args     = -s /var/lib/tftpboot --verbose` to `/etc/xinetd.d/tftp` assuming you are using xinetd to get this output.

        Jan 21 15:45:00 controller xinetd[10044]: START: tftp pid=10048 from=172.16.71.98
        Jan 21 15:45:00 controller in.tftpd[10049]: RRQ from 172.16.71.98 filename uefi/BOOTX64.EFI
        Jan 21 15:45:00 controller in.tftpd[10049]: Error code 8: User aborted the transfer
        Jan 21 15:45:00 controller in.tftpd[10050]: RRQ from 172.16.71.98 filename uefi/BOOTX64.EFI
        Jan 21 15:45:00 controller in.tftpd[10050]: Client 172.16.71.98 finished uefi/BOOTX64.EFI
        Jan 21 15:45:00 controller in.tftpd[10051]: RRQ from 172.16.71.98 filename uefi/grubx64.efi
        Jan 21 15:45:00 controller in.tftpd[10051]: Client 172.16.71.98 finished uefi/grubx64.efi
        Jan 21 15:45:00 controller in.tftpd[10052]: RRQ from 172.16.71.98 filename /uefi/grub.cfg-01-00-50-56-86-d4-06
        Jan 21 15:45:00 controller in.tftpd[10052]: Client 172.16.71.98 File not found /uefi/grub.cfg-01-00-50-56-86-d4-06
        Jan 21 15:45:00 controller in.tftpd[10053]: RRQ from 172.16.71.98 filename /uefi/grub.cfg-AC104762
        Jan 21 15:45:00 controller in.tftpd[10053]: Client 172.16.71.98 File not found /uefi/grub.cfg-AC104762
        Jan 21 15:45:00 controller in.tftpd[10054]: RRQ from 172.16.71.98 filename /uefi/grub.cfg-AC10476
        Jan 21 15:45:00 controller in.tftpd[10054]: Client 172.16.71.98 File not found /uefi/grub.cfg-AC10476
        Jan 21 15:45:00 controller in.tftpd[10055]: RRQ from 172.16.71.98 filename /uefi/grub.cfg-AC1047
        Jan 21 15:45:00 controller in.tftpd[10055]: Client 172.16.71.98 File not found /uefi/grub.cfg-AC1047
        Jan 21 15:45:00 controller in.tftpd[10056]: RRQ from 172.16.71.98 filename /uefi/grub.cfg-AC104
        Jan 21 15:45:00 controller in.tftpd[10056]: Client 172.16.71.98 File not found /uefi/grub.cfg-AC104
        Jan 21 15:45:00 controller in.tftpd[10057]: RRQ from 172.16.71.98 filename /uefi/grub.cfg-AC10
        Jan 21 15:45:00 controller in.tftpd[10057]: Client 172.16.71.98 File not found /uefi/grub.cfg-AC10
        Jan 21 15:45:00 controller in.tftpd[10058]: RRQ from 172.16.71.98 filename /uefi/grub.cfg-AC1
        Jan 21 15:45:00 controller in.tftpd[10058]: Client 172.16.71.98 File not found /uefi/grub.cfg-AC1
        Jan 21 15:45:00 controller in.tftpd[10059]: RRQ from 172.16.71.98 filename /uefi/grub.cfg-AC
        Jan 21 15:45:00 controller in.tftpd[10059]: Client 172.16.71.98 File not found /uefi/grub.cfg-AC
        Jan 21 15:45:00 controller in.tftpd[10060]: RRQ from 172.16.71.98 filename /uefi/grub.cfg-A
        Jan 21 15:45:00 controller in.tftpd[10060]: Client 172.16.71.98 File not found /uefi/grub.cfg-A
        Jan 21 15:45:00 controller in.tftpd[10061]: RRQ from 172.16.71.98 filename /uefi/grub.cfg
        Jan 21 15:45:00 controller in.tftpd[10061]: Client 172.16.71.98 finished /uefi/grub.cfg
        Jan 21 15:45:00 controller in.tftpd[10062]: RRQ from 172.16.71.98 filename /EFI/BOOT/x86_64-efi/command.lst
        Jan 21 15:45:00 controller in.tftpd[10062]: Client 172.16.71.98 File not found /EFI/BOOT/x86_64-efi/command.lst
        Jan 21 15:45:00 controller in.tftpd[10063]: RRQ from 172.16.71.98 filename /EFI/BOOT/x86_64-efi/fs.lst
        Jan 21 15:45:00 controller in.tftpd[10063]: Client 172.16.71.98 File not found /EFI/BOOT/x86_64-efi/fs.lst
        Jan 21 15:45:00 controller in.tftpd[10064]: RRQ from 172.16.71.98 filename /EFI/BOOT/x86_64-efi/crypto.lst
        Jan 21 15:45:00 controller in.tftpd[10064]: Client 172.16.71.98 File not found /EFI/BOOT/x86_64-efi/crypto.lst
        Jan 21 15:45:00 controller in.tftpd[10065]: RRQ from 172.16.71.98 filename /EFI/BOOT/x86_64-efi/terminal.lst
        Jan 21 15:45:00 controller in.tftpd[10065]: Client 172.16.71.98 File not found /EFI/BOOT/x86_64-efi/terminal.lst
        Jan 21 15:45:00 controller in.tftpd[10066]: RRQ from 172.16.71.98 filename /uefi/grub.cfg
        Jan 21 15:45:00 controller in.tftpd[10066]: Client 172.16.71.98 finished /uefi/grub.cfg
        Jan 21 15:45:02 controller in.tftpd[10067]: RRQ from 172.16.71.98 filename /vmlinuz
        Jan 21 15:45:03 controller in.tftpd[10067]: Client 172.16.71.98 finished /vmlinuz
        Jan 21 15:45:03 controller in.tftpd[10068]: RRQ from 172.16.71.98 filename /initrd.img
        Jan 21 15:45:08 controller in.tftpd[10068]: Client 172.16.71.98 finished /initrd.img

4. The boot menu profile (grub.cfg) looks like the below. The most important line is the linuxefi line. This line points to where your installation media should be hosted. Typically using httpd.

        set default="1"

        function load_video {
        insmod efi_gop
        insmod efi_uga
        insmod video_bochs
        insmod video_cirrus
        insmod all_video
        }

        load_video
        set gfxpayload=keep
        insmod gzio
        insmod part_gpt
        insmod ext2

        set timeout=1
        ### END /etc/grub.d/00_header ###

        ### BEGIN /etc/grub.d/10_linux ###
        menuentry 'Install Super Legit Fedora' --class fedora --class gnu-linux --class gnu --class os {
                echo "Loading vmlinuz"
                linuxefi vmlinuz inst.ks=http://192.168.2.101/ks/uefi/fedora.cfg inst.repo=http://192.168.1.121/iso/

                echo "Loading initrd.img"
                initrdefi initrd.img
        }

5. The host in question will reach out and in this configuration grab a file called `install.img` located at /var/www/html/iso/images/ in this build. This file allows the host to boot and perform its other functions.

TODO - finish this.
