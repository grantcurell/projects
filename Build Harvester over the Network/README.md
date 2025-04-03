# Build Harvester over the Network

- [Build Harvester over the Network](#build-harvester-over-the-network)
  - [Network Setup Assumptions](#network-setup-assumptions)
  - [PXE Host OS](#pxe-host-os)
  - [Configure HTTP Server](#configure-http-server)
  - [Download and Place Boot Artifacts](#download-and-place-boot-artifacts)
  - [DHCP Server Configuration (ISC DHCP)](#dhcp-server-configuration-isc-dhcp)
    - [Logic Overview](#logic-overview)
    - [Install ISC DHCP Server on Rocky 9](#install-isc-dhcp-server-on-rocky-9)
    - [Configure `/etc/dhcp/dhcpd.conf`](#configure-etcdhcpdhcpdconf)
    - [🔥 Step 3: Restart DHCP](#-step-3-restart-dhcp)
  - [Create Required Scripts](#create-required-scripts)
  - [Create Configurations](#create-configurations)
    - [Create `config-create.yaml` (for first node)](#create-config-createyaml-for-first-node)
    - [Create `config-join.yaml` (for all JOIN nodes)](#create-config-joinyaml-for-all-join-nodes)
  - [Troubleshooting](#troubleshooting)

## Network Setup Assumptions

| Component         | Value                               |
|------------------|-------------------------------------|
| HTTP Server IP   | `10.10.25.90`                        |
| Subnet           | `10.10.25.0/24`                      |
| Router/Gateway   | `10.10.25.90` (same as HTTP server)  |
| DNS              | `8.8.8.8`                            |
| VIP for cluster  | `10.10.25.99`                        |
| NIC              | `ens5`                               |
| ISO Version      | `v1.4.2`                             |
| Boot Directory   | `/usr/share/nginx/html/harvester/`  |

## PXE Host OS

```bash
[grant@rockydesktop ~]$ cat /etc/*-release
NAME="Rocky Linux"
VERSION="9.5 (Blue Onyx)"
ID="rocky"
ID_LIKE="rhel centos fedora"
VERSION_ID="9.5"
PLATFORM_ID="platform:el9"
PRETTY_NAME="Rocky Linux 9.5 (Blue Onyx)"
ANSI_COLOR="0;32"
LOGO="fedora-logo-icon"
CPE_NAME="cpe:/o:rocky:rocky:9::baseos"
HOME_URL="https://rockylinux.org/"
VENDOR_NAME="RESF"
VENDOR_URL="https://resf.org/"
BUG_REPORT_URL="https://bugs.rockylinux.org/"
SUPPORT_END="2032-05-31"
ROCKY_SUPPORT_PRODUCT="Rocky-Linux-9"
ROCKY_SUPPORT_PRODUCT_VERSION="9.5"
REDHAT_SUPPORT_PRODUCT="Rocky Linux"
REDHAT_SUPPORT_PRODUCT_VERSION="9.5"
Rocky Linux release 9.5 (Blue Onyx)
Rocky Linux release 9.5 (Blue Onyx)
Rocky Linux release 9.5 (Blue Onyx)
```

## Configure HTTP Server

```bash
sudo dnf install -y nginx
sudo systemctl enable --now nginx
sudo chcon -Rt httpd_sys_content_t /usr/share/nginx/html/harvester
sudo firewall-cmd --add-service=http --permanent
sudo firewall-cmd --reload
```

## Download and Place Boot Artifacts

Download the following files from the [Harvester Releases page](https://github.com/harvester/harvester/releases):

From the release you're using, download:

- The **ISO file**
- The **vmlinuz** kernel
- The **initrd** image
- The **rootfs squashfs** file

Also download the UEFI iPXE binary:

- `ipxe.efi` from [http://boot.ipxe.org/ipxe.efi](http://boot.ipxe.org/ipxe.efi)
  - `wget http://boot.ipxe.org/ipxe.efi`

Place them all into your HTTP server directory:

```bash
mkdir -p /usr/share/nginx/html/harvester
# Copy all downloaded files into this directory
```

## DHCP Server Configuration (ISC DHCP)

I am using the following:

| Detail                     | Value               |
|----------------------------|---------------------|
| DHCP/HTTP Server IP       | `10.10.25.90`        |
| Subnet                    | `10.10.25.0/24`      |
| DHCP Range                | `10.10.25.90–96`     |
| VIP for Harvester cluster | `10.10.25.99`        |
| Interface Name            | `ens5`               |

| VM     | MAC Address           | IP Address     | Mode   | Hostname   |
|--------|------------------------|----------------|--------|------------|
| harv1  | `00:50:56:8a:ce:66`    | `10.10.25.91`  | CREATE | `harv1`    |
| harv2  | `00:50:56:8a:99:71`    | `10.10.25.92`  | JOIN   | `harv2`    |
| harv3  | `00:50:56:8a:53:e9`    | `10.10.25.93`  | JOIN   | `harv3`    |

### Logic Overview

1. **UEFI HTTP client boots → sends DHCP request**
   - DHCP sees `vendor-class-identifier = "HTTPClient"`
2. **DHCP replies with**:
   ```dhcp
   filename "http://10.10.25.90/harvester/ipxe.efi";
   ```
   → This gives the UEFI client the raw iPXE binary

3. The client **loads and executes `ipxe.efi`**
4. Then the iPXE binary sends **a second DHCP request**
   - This time it sends `user-class = "iPXE"`
5. DHCP replies with either:
   - `ipxe-create-efi` (for CREATE node)
   - `ipxe-join-efi` (for JOIN nodes)

### Install ISC DHCP Server on Rocky 9

```bash
sudo dnf install -y dhcp-server
sudo systemctl enable --now dhcpd
```

### Configure `/etc/dhcp/dhcpd.conf`

Paste this **entire config**:

```shell
# Defines the client architecture type (used to detect UEFI vs BIOS)
option architecture-type code 93 = unsigned integer 16;

# Define your network subnet and DHCP range
subnet 10.10.25.0 netmask 255.255.255.0 {
  option routers 10.10.25.90;               # <--- Update to the IP of your DHCP/HTTP server (gateway for PXE nodes)
  option domain-name-servers 8.8.8.8;       # <--- Optional: your preferred DNS server(s)
  range 10.10.25.90 10.10.25.96;            # <--- Update to your desired DHCP IP range
}

# GROUP 1: First node in CREATE mode
group {
  # Boot logic based on PXE/iPXE/UEFI HTTP detection
  if exists user-class and option user-class = "iPXE" {
    if option architecture-type = 00:07 {
      filename "http://10.10.25.90/harvester/ipxe-create-efi";  # <--- Update with your HTTP server IP if different
    } else {
      filename "http://10.10.25.90/harvester/ipxe-create";      # <--- Update with your HTTP server IP if different
    }
  } elsif substring (option vendor-class-identifier, 0, 10) = "HTTPClient" {
    option vendor-class-identifier "HTTPClient";
    filename "http://10.10.25.90/harvester/ipxe.efi";           # <--- Update with your HTTP server IP if different
  } else {
    if option architecture-type = 00:07 {
      filename "ipxe.efi";          # <--- Served via TFTP if you're supporting legacy UEFI PXE clients
    } else {
      filename "undionly.kpxe";     # <--- Served via TFTP for legacy BIOS PXE clients
    }
  }

  # Host definition for the first node
  host harv1 {
    hardware ethernet 00:50:56:8a:ce:66;   # <--- Update with MAC address of your first Harvester node (CREATE)
    fixed-address 10.10.25.91;             # <--- Static IP to assign this node
  }
}

# GROUP 2: Remaining nodes in JOIN mode
group {
  if exists user-class and option user-class = "iPXE" {
    if option architecture-type = 00:07 {
      filename "http://10.10.25.90/harvester/ipxe-join-efi";    # <--- Update with your HTTP server IP if different
    } else {
      filename "http://10.10.25.90/harvester/ipxe-join";        # <--- Update with your HTTP server IP if different
    }
  } elsif substring (option vendor-class-identifier, 0, 10) = "HTTPClient" {
    option vendor-class-identifier "HTTPClient";
    filename "http://10.10.25.90/harvester/ipxe.efi";           # <--- Update with your HTTP server IP if different
  } else {
    if option architecture-type = 00:07 {
      filename "ipxe.efi";
    } else {
      filename "undionly.kpxe";
    }
  }

  # Host definitions for JOIN nodes
  host harv2 {
    hardware ethernet 00:50:56:8a:99:71;   # <--- Update with MAC address of this Harvester node (JOIN)
    fixed-address 10.10.25.92;             # <--- Static IP to assign this node
  }

  host harv3 {
    hardware ethernet 00:50:56:8a:53:e9;   # <--- Update with MAC address of this Harvester node (JOIN)
    fixed-address 10.10.25.93;             # <--- Static IP to assign this node
  }
}
```

### 🔥 Step 3: Restart DHCP

```bash
sudo systemctl restart dhcpd
```

Check logs for any issues:

```bash
journalctl -u dhcpd -xe
```

## Create Required Scripts

```bash
HARVESTER_VERSION="v1.4.2"  # <--- Update with your harvester version
HTTP_SERVER="10.10.25.90"

mkdir -p /usr/share/nginx/html/harvester

cat <<EOF > /usr/share/nginx/html/harvester/ipxe-create
#!ipxe
kernel http://$HTTP_SERVER/harvester/harvester-$HARVESTER_VERSION-vmlinuz-amd64 initrd=harvester-$HARVESTER_VERSION-initrd-amd64 ip=dhcp net.ifnames=1 rd.cos.disable rd.noverifyssl console=tty1 root=live:http://$HTTP_SERVER/harvester/harvester-$HARVESTER_VERSION-rootfs-amd64.squashfs harvester.install.automatic=true harvester.install.config_url=http://$HTTP_SERVER/harvester/config-create.yaml
initrd http://$HTTP_SERVER/harvester/harvester-$HARVESTER_VERSION-initrd-amd64
boot
EOF

cp /usr/share/nginx/html/harvester/ipxe-create /usr/share/nginx/html/harvester/ipxe-create-efi

cat <<EOF > /usr/share/nginx/html/harvester/ipxe-join
#!ipxe
kernel http://$HTTP_SERVER/harvester/harvester-$HARVESTER_VERSION-vmlinuz-amd64 initrd=harvester-$HARVESTER_VERSION-initrd-amd64 ip=dhcp net.ifnames=1 rd.cos.disable rd.noverifyssl console=tty1 root=live:http://$HTTP_SERVER/harvester/harvester-$HARVESTER_VERSION-rootfs-amd64.squashfs harvester.install.automatic=true harvester.install.config_url=http://$HTTP_SERVER/harvester/config-join.yaml
initrd http://$HTTP_SERVER/harvester/harvester-$HARVESTER_VERSION-initrd-amd64
boot
EOF

cp /usr/share/nginx/html/harvester/ipxe-join /usr/share/nginx/html/harvester/ipxe-join-efi
```

## Create Configurations

Now that your PXE and HTTP services are ready, it's time to define the configuration files that tell each Harvester node how to install and what role it should play in the cluster.

These YAML files are consumed automatically by Harvester during PXE boot and allow fully unattended installs.

You'll need two files:

- `config-create.yaml`: for the first node (it creates the cluster)
- `config-join.yaml`: for all additional nodes (they join the cluster)

These files are served from your HTTP server and referenced in your iPXE boot scripts.

**What to Expect**

- Each node will download the YAML config during boot.
- The first node will initialize the Harvester cluster.
- Remaining nodes will automatically join once they boot with their config.
- You'll be able to access the Harvester UI at the **VIP address** you specify (e.g., `https://10.10.25.99`).

Make sure to update all placeholder values (SSH key, IPs, version, etc.) where marked. As before the text blocks are setup to be copied and pasted.

Then, power on your VMs and watch your cluster build itself.

### Create `config-create.yaml` (for first node)

```yaml
cat <<EOF > /usr/share/nginx/html/harvester/config-create.yaml
scheme_version: 1
token: harvester-cluster-token               # <--- Set your desired cluster join token (must match on all nodes)
os:
  hostname: harv1                            # <--- Update to desired hostname for this node
  password: I.am.ghost.47                    # <--- Update to your desired root password
  ssh_authorized_keys:
    - ssh-rsa AAAAB3...replace_with_your_key # <--- Replace with your actual SSH public key
  ntp_servers:
    - 0.suse.pool.ntp.org
    - 1.suse.pool.ntp.org
install:
  mode: create
  management_interface:
    interfaces:
      - name: ens5                           # <--- Update to the NIC name in your VM (likely ens5 or eth0)
    default_route: true
    method: dhcp
    bond_options:
      mode: balance-tlb
      miimon: 100
  device: /dev/sda                           # <--- Update if your VM uses a different device (e.g. /dev/vda)
  iso_url: http://10.10.25.90/harvester/harvester-v1.4.2-amd64.iso  # <--- Update with your HTTP server IP and Harvester version
  vip: 10.10.25.99                           # <--- Update to your cluster's virtual IP
  vip_mode: static
EOF
```

### Create `config-join.yaml` (for all JOIN nodes)

```yaml
cat <<EOF > /usr/share/nginx/html/harvester/config-join.yaml
scheme_version: 1
token: harvester-cluster-token               # <--- Must match token from config-create.yaml
server_url: https://10.10.25.99:443          # <--- Update to the cluster VIP of your CREATE node
os:
  hostname: harv2                            # <--- Update to unique hostname for this node
  password: I.am.ghost.47                    # <--- Update to your desired root password
  ssh_authorized_keys:
    - ssh-rsa AAAAB3...replace_with_your_key # <--- Replace with your actual SSH public key
  dns_nameservers:
    - 8.8.8.8
install:
  mode: join
  management_interface:
    interfaces:
      - name: ens5                           # <--- Update to the NIC name in your VM
    default_route: true
    method: dhcp
    bond_options:
      mode: balance-tlb
      miimon: 100
  device: /dev/sda                           # <--- Update if different
  iso_url: http://10.10.25.90/harvester/harvester-v1.4.2-amd64.iso  # <--- Update with your HTTP server IP and Harvester version
EOF
```

## Troubleshooting

