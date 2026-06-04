# Windows Workstation Deployer for Offline Environment

- [Windows Workstation Deployer for Offline Environment](#windows-workstation-deployer-for-offline-environment)
  - [Getting Started](#getting-started)
  - [Quickstart](#quickstart)
    - [Clone repository](#clone-repository)
    - [Run setup wizard](#run-setup-wizard)
    - [Manually run full pipeline without using setup](#manually-run-full-pipeline-without-using-setup)
  - [Expected artifacts](#expected-artifacts)
  - [Offline Restore and Use](#offline-restore-and-use)
  - [How to Force Rebuild](#how-to-force-rebuild)

Builds a deployer LXC which can be taken to offline environmment and used to deploy Windows workstations from a sysprepped golden image. Uses Proxmox for the workflow.

## Getting Started

Before running the setup you will need:
- **Proxmox cluster/node** with SSH access (the setup will ask for credentials)
- **WinPE builder VM** (Windows Server) with ADK/WinPE tooling and WinRM access.
  - You will need to build this manually. You will need a copy of Windows Server somewhere. I tested on 2025.
- **Golden image VM**
  - This is a running version of your Windows client from which you want to build a golden image. It must have WinRM enabled!
- Controller
  - This is the thing from which the Ansible will run. You'll pull your code down onto the controller and it will then orchestrate everything. Doesn't matter where or what it is as long as it has IP connectivity to Proxmox, Windows Server, the Golden Image VM, and it's running Ubuntu.
- **Intel RST/NVMe driver package** pre-cached on the controller for first run:
  - Put `Intel-RST-7WNN0.exe` in `artifacts/drivers/` before running the pipeline.
  - Source URL is defined in `inventories/windows-deployer/group_vars/all.yml` under `windows.winpe_builder.storage_drivers`.


This project builds for you:
- **Deployer LXC** on Proxmox (PXE, iPXE, DHCP/TFTP/HTTP/SMB services).
  - This is the LXC container that will ultimately get tar'd up and you can go anywhere with it and deploy N workstations.
- **WinPE boot artifacts** and published deployment artifacts.
  - All the things you need to build and boot windows
- **Target workstation VM(s)** booted over PXE and installed from `deploy.wim`.
  - At the end, the code will do a test against a secureboot-enabled, UEFI, Proxmox VM from Deployer LXC just to make sure everything is working

Before you start make sure you have the Windows Server box, the golden image VM, and what will become your controller, up and running.

## Quickstart

### Clone repository

On your controller:

```bash
git clone https://github.com/grantcurell/projects.git
cd projects/"Windows Workstation Deployer for Offline Environments"
```

### Run setup wizard

```bash
./setup
```

Follow the instructions and at the end it will kick off the deployment.

### Manually run full pipeline without using setup

```bash
./scripts/run-full-deploy.sh
```

## Expected artifacts

Controller `artifacts/` should contain:
- `boot.wim`
- `bootmgr`
- `boot/BCD`
- `boot/boot.sdi`
- `efi/microsoft/boot/BCD`
- `efi/boot/bootx64.efi`
- `winpe_capture.iso`
- `vzdump-lxc-<deployer-vmid>-*.tar.zst`

`deploy.wim` is kept on deployer LXC at `/srv/deploy/images/deploy.wim`.

## Offline Restore and Use

When you are ready to export the deployer LXC container and bring it to an offline environment do the following.

1) Copy the exported deployer backup from controller:
- `artifacts/vzdump-lxc-<deployer-vmid>-*.tar.zst`

2) Put that file onto the offline Proxmox host (example destination):
- `/var/lib/vz/dump/`

3) Restore as an LXC on offline Proxmox:

```bash
pct restore <new-vmid> /var/lib/vz/dump/vzdump-lxc-<deployer-vmid>-<timestamp>.tar.zst --storage <target-storage>
```

4) Configure offline network settings on the restored container:

```bash
pct set <new-vmid> --hostname <offline-deployer-hostname>
pct set <new-vmid> --net0 name=eth0,bridge=<offline-bridge>,ip=<offline-ip>/<prefix>,gw=<offline-gateway>
```

5) Start container and verify core services:

```bash
pct start <new-vmid>
pct exec <new-vmid> -- systemctl status nginx dnsmasq smbd
```

6) Verify deploy artifacts inside restored container:

```bash
pct exec <new-vmid> -- ls -lh /srv/deploy/images/deploy.wim
pct exec <new-vmid> -- ls -lh /srv/deploy/winpe/boot.wim
pct exec <new-vmid> -- ls -lh /srv/deploy/winpe/EFI/Microsoft/Boot/BCD
```

7) Deploy in offline site:
- Ensure target network can PXE boot from restored deployer IP.
- Boot target workstation(s) on that network.
- They should chain through iPXE/wimboot and install from `/srv/deploy/images/deploy.wim`.

## How to Force Rebuild

Set force_rebuild to true in the [inventory file](./inventories/windows-deployer/group_vars/all.yml)

```yaml
windows:
  winpe_builder:
    force_rebuild: false
```
