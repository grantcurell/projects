# How to ONIE Install and ZTP Config Dell SONiC

- [How to ONIE Install and ZTP Config Dell SONiC](#how-to-onie-install-and-ztp-config-dell-sonic)
  - [My Test Platform](#my-test-platform)
    - [Switch](#switch)
    - [Server OS](#server-os)
  - [Prepare to Install Operating System](#prepare-to-install-operating-system)
    - [Manually Install SONiC via ONIE](#manually-install-sonic-via-onie)
    - [Fully Automated Installation from OS10 to SONiC](#fully-automated-installation-from-os10-to-sonic)
      - [Overview](#overview)
  - [Configure DHCP Server for SONiC ZTP](#configure-dhcp-server-for-sonic-ztp)
    - [Configure DHCP for ZTP](#configure-dhcp-for-ztp)
    - [Configure Your HTTP Server](#configure-your-http-server)
      - [More Configuration Options](#more-configuration-options)
  - [Running ZTP](#running-ztp)
  - [Get Command Line](#get-command-line)

See [Install Workflow](./overview.pptx) for an overview of how this process flows.
Video of the full sequence: https://youtu.be/Xm4stcPvnUc

## My Test Platform

### Switch
```
OS10# show version
Dell EMC Networking OS10 Enterprise
Copyright (c) 1999-2021 by Dell Inc. All Rights Reserved.
OS Version: 10.5.3.0
Build Version: 10.5.3.0.44
Build Time: 2021-10-06T23:03:55+0000
System Type: S5212F-ON
Architecture: x86_64
Up Time: 00:34:10
```

### Server OS
```
Fedora release 35 (Thirty Five)
NAME="Fedora Linux"
VERSION="35 (Workstation Edition)"
ID=fedora
VERSION_ID=35
VERSION_CODENAME=""
PLATFORM_ID="platform:f35"
PRETTY_NAME="Fedora Linux 35 (Workstation Edition)"
ANSI_COLOR="0;38;2;60;110;180"
LOGO=fedora-logo-icon
CPE_NAME="cpe:/o:fedoraproject:fedora:35"
HOME_URL="https://fedoraproject.org/"
DOCUMENTATION_URL="https://docs.fedoraproject.org/en-US/fedora/f35/system-administrators-guide/"
SUPPORT_URL="https://ask.fedoraproject.org/"
BUG_REPORT_URL="https://bugzilla.redhat.com/"
REDHAT_BUGZILLA_PRODUCT="Fedora"
REDHAT_BUGZILLA_PRODUCT_VERSION=35
REDHAT_SUPPORT_PRODUCT="Fedora"
REDHAT_SUPPORT_PRODUCT_VERSION=35
PRIVACY_POLICY_URL="https://fedoraproject.org/wiki/Legal:PrivacyPolicy"
VARIANT="Workstation Edition"
VARIANT_ID=workstation
Fedora release 35 (Thirty Five)
Fedora release 35 (Thirty Five)
```


## Prepare to Install Operating System

This first section discusses operating system installation. If you manually install the OS, you will start the next section of the instructions with the OS already installed. If you are performing the fully automated setup, you will install the OS later on in the instructions.

### Manually Install SONiC via ONIE

1. Download SONiC OS for your manufacturer. In my case I pulled Dell's stable image.
2. Follow the instructions [for setting up and running ONIE](../README.md#how-to-configure-onie)
   1. Use SONiC binary instead of OS10

### Fully Automated Installation from OS10 to SONiC

#### Overview

1. On a separate host, set up an HTTP server to host your operating system files
   1. You could also use TFTP but for demonstration here I am using HTTP
2. On a separate host, set up a DHCP server to feed the ZTD/ZTP options
3. Force OS10 to reboot in ONIE uninstall mode and then allow it to boot in ONIE install mode (see [reload command](https://dl.dell.com/content/manual35024495-dell-smartfabric-os10-user-guide-release-10-5-4.pdf?language=en-us#page=67))
4. Install SONiC

Dell switches are often shipped with OS10 by default (many times to meet TAA compliance requirements). In this scenario you may have just purchased several switches and you want to fully automate their out-of-the-box installation by replacing OS10 with SONiC. By default, OS10 will boot for the first time in Zero Touch Deployment (ZTD) mode. Entering configuration mode or rebooting the switch disables it. You can re-enable it with `reload ztd`. **WARNING** This will delete your startup configuration. You can check ztd status with `show ztd-status`. At time of writing [this](https://dl.dell.com/content/manual43922122-dell-smartfabric-os10-user-guide-release-10-5-4.pdf?language=en-us&ps=true) is the current OS10 manual. See page 93 for information on ZTD.

1. While you can ONIe boot / ZTD with the switch's frontpanel ports, I tested this configuration using the management interface. These instructions are written assuming you have the management interface plugged in. If you need to console into the management interface the settings are:

        Baud Rate: 115200
        Data Bits: 8
        Stop Bits: 1
        Parity: None
        Flow Control: None

2. Configure HTTP server
   1. On your Fedora box run `dnf install httpd`
   2. Start it with `systemctl start httpd`
   3. Upload the SONiC binary to `var/www/html`
   4. Run `ln -s Enterprise_SONiC_OS_4.0.1_Enterprise_Premium.bin onie-installer` to create a symbolic link with the name onie-installer. This is the name ONIE will automatically search for.
   5. Confirm your web server is working by browsing to onie-installer at `http://<your_ip>/onie-installer`.
3. On your Fedora box run `dnf install -y dhcp-server`
4. Edit your DHCP server configuration with `vim /etc/dhcp/dhcpd.conf`. Replace the IP addresses with your IP addresses. Note: You will modify the line `option bootfile-name "http://192.168.1.186:80/initial.json";       # For Option 67 (HTTP)` further on in the instructions

        #
        # DHCP Server Configuration file.
        #   see /usr/share/doc/dhcp-server/dhcpd.conf.example
        #   see dhcpd.conf(5) man page
        #


        ddns-update-style interim;

        option ztd-provision-url code 240 = text;

        subnet 192.168.1.0 netmask 255.255.255.0 {

                max-lease-time 86400;

                min-lease-time 60;

                default-lease-time 86400;

                option netbios-node-type 8;

                host OS10 {
                        hardware ethernet b0:4f:13:37:b8:c0;
                        fixed-address 192.168.1.90;
                        option default-url "http://192.168.1.186/ztd/onie-installer";     # For Option 114 (Default URL)
                        option bootfile-name "http://192.168.1.186:80/initial.json";       # For Option 67 (HTTP)
                }
        }

5. Run `systemctl restart dhcpd` to apply the configuration and ensure that dhcpd is running.
6. You are now ready to move on to the ZTP configuration

## Configure DHCP Server for SONiC ZTP

The official ZTP documentation for SONiC is [here](https://github.com/Azure/SONiC/blob/master/doc/ztp/ztp.md).

### Configure DHCP for ZTP

The first thing you will need to do is configure the DHCP server servicing the devices to provide option 67 which will point to initial boot file used by SONiC's ZTP agent. The options for URL are defined [here](https://github.com/Azure/SONiC/blob/master/doc/ztp/ztp.md#url-object). As shown above, I used the following DHCP configuration file (located at `/etc/dhcp/dhcpd.conf` on Fedora):

        #
        # DHCP Server Configuration file.
        #   see /usr/share/doc/dhcp-server/dhcpd.conf.example
        #   see dhcpd.conf(5) man page
        #


        ddns-update-style interim;

        option ztd-provision-url code 240 = text;

        subnet 192.168.1.0 netmask 255.255.255.0 {

                max-lease-time 86400;

                min-lease-time 60;

                default-lease-time 86400;

                option netbios-node-type 8;

                host OS10 {
                        hardware ethernet b0:4f:13:37:b8:c0;
                        fixed-address 192.168.1.90;
                        option default-url "http://192.168.1.186/ztd/onie-installer";     # For Option 114 (Default URL)
                        option bootfile-name "http://192.168.1.186:80/initial.json";       # For Option 67 (HTTP)
                }
        }

Notice the line `option bootfile-name "http://192.168.1.186:80/initial.json";       # For Option 67 (HTTP)`. If you want to use TFTP you can replace the `http://` with `tftp://`. This line tells SONiC where to look for a configuration pointer. The name `initial.json` does not matter - you can name this file whatever you want. This file will contain a web address pointing to `config_db.json` which is the file SONiC gives ZTP to configure itself.

Run `systemctl restart dhcpd` to ensure your changes take effect.

### Configure Your HTTP Server

As mentioned above, you have to create a file which points to config_db.json. A copy of mine is below.

```json
{
  "ztp": {
    "configdb-json" : {
      "url": {
        "source": "http://192.168.1.186:80/config_db.json"
      }
    }
  }
}
```

The *source* field points to the actual configuration file you want to deploy to the networking device. On your web server you will also need to provide this configuration file. In my case I only had it update the device's management IP address but you can have it configure any aspect of the switch:

```json
{
  "MGMT_INTERFACE": {
      "eth0|192.168.1.96/24": {
          "gwaddr": "192.168.1.1"
      }
  }
}
```

This file's sections are identical to what is in */etc/sonic/config_db.json*. If you want to see what something should look like you can look there and then copy/paste.

#### More Configuration Options

The file `initial.json` has a myriad of options allowing you to do things like set firmware options, set the password, perform connection tests on completion, etc. I only demonstrated one here just to get started. See Dell's SONiC manual for additional options.

## Running ZTP

If you have already installed SONiC manually, at this point you can leave things running and SONiC's ZTP should automatically start. If not, you can make sure it is on with `ztp enable` and then `ztp run` to force it to run.

If you are performing a fully automated install, then at this point, if your DHCP server config is correct, you should see OS10 reboot into ONIE uninstall mode. It will uninstall OS10, reboot in ONIE install mode, and install SONiC. **Note:** The way this works is OS10 checks the onie-installer argument provided in the DHCP configuration. If the installer is not OS10, it reboots in ONIE uninstall mode.

See https://youtu.be/Xm4stcPvnUc for a depiction of what the entire process looks like from start to finish.

## Get Command Line

Run `sonic-cli` to get an OS-10 style command line.
