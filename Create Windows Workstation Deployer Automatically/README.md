# Windows Workstation Deployer

Builds a Proxmox deployer LXC and deploys Windows workstations from a sysprepped golden image.

## Getting Started

Before running the setup you will need:

You must provide and keep running:
- **Proxmox cluster/node** with SSH access (the setup will ask for credentials)
- **WinPE builder VM** (Windows Server) with ADK/WinPE tooling and WinRM access.
  - You will need to build this manually. You will need a copy of Windows Server somewhere. I tested on 2025.
- **Golden image VM**
  - This is a running version of your Windows client from which you want to build a golden image. It must have WinRM enabled!
- Controller
  - This is the thing from which the Ansible will run. You'll pull your code down onto the controller and it will then orchestrate everything. Doesn't matter where or what it is as long as it has IP connectivity to Proxmox, Windows Server, the Golden Image VM, and it's running Ubuntu.


This project builds for you:
- **Deployer LXC** on Proxmox (PXE, iPXE, DHCP/TFTP/HTTP/SMB services).
  - This is the LXC container that will ultimately get tar'd up and you can go anywhere with it and deploy N workstations.
- **WinPE boot artifacts** and published deployment artifacts.
  - All the things you need to build and boot windows
- **Target workstation VM(s)** booted over PXE and installed from `deploy.wim`.
  - At the end, the code will do a test against a secureboot-enabled, UEFI, Proxmox VM from Deployer LXC just to make sure everything is working

Before you start make sure you have the Windows Server box, the golden image VM, and what will become your controller, up and running.

## Quickstart

### 1) Clone repository

On your controller:

```bash
git clone https://github.com/grantcurell/projects.git
cd projects/"Create Windows Workstation Deployer Automatically"
```

### 2) Run setup wizard

```bash
./setup
```

### 3) Run full pipeline (manual fallback)

```bash
./scripts/run-full-deploy.sh
```

## Manual commands (if needed)

```bash
./scripts/bootstrap-controller.sh
ansible-playbook -i inventories/windows-deployer/hosts.yml playbooks/00-preflight.yml
ansible-playbook -i inventories/windows-deployer/hosts.yml playbooks/site.yml
```

## Minimum prerequisites

- Proxmox reachable from this controller
- Golden image VM exists and is running
- WinPE builder VM exists and is running
- WinRM enabled on both Windows VMs

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

## Common rerun note

For normal reruns keep:

```yaml
windows:
  winpe_builder:
    force_rebuild: false
```
