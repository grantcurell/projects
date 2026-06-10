# Windows Workstation Deployer for Offline Environment

- [Windows Workstation Deployer for Offline Environment](#windows-workstation-deployer-for-offline-environment)
  - [Getting Started](#getting-started)
  - [Credentials and Ansible Vault](#credentials-and-ansible-vault)
  - [Quickstart](#quickstart)
    - [Clone repository](#clone-repository)
    - [Run setup wizard](#run-setup-wizard)
    - [Manually run full pipeline without using setup](#manually-run-full-pipeline-without-using-setup)
  - [Expected artifacts](#expected-artifacts)
  - [Portable hostname model](#portable-hostname-model)
  - [Offline Restore and Use](#offline-restore-and-use)
    - [Option 1 (recommended): guided field deployment script](#option-1-recommended-guided-field-deployment-script)
    - [Option 2: manual restore](#option-2-manual-restore)
  - [How to Force Rebuild](#how-to-force-rebuild)

Builds a deployer LXC which can be taken to offline environmment and used to deploy Windows workstations from a sysprepped golden image. Uses Proxmox for the workflow.

## Getting Started

Before running the setup you will need:
- **Proxmox cluster/node** with SSH access (the setup will ask for credentials)
- **Windows Server 2025 - WinPE builder VM** (Windows Server) with ADK/WinPE tooling and WinRM access.
  - You will need to manually build and setup Windows Server 2025 somewhere in your environment and record the credentials
  - Need to build out the Windows Server identity host / domain controller too? The sibling project [`Configure-WindowsIdentityServices`](../Configure-WindowsIdentityServices/README.md) automates that buildout (AD DS, DNS, DHCP, time, GPO baseline, optional PKI) from a single YAML file. It is standalone and not part of this deployer's workflow.
- **Golden image VM (Source VM)**
  - This is a running version of your Windows client from which you want to build a golden image. It must have WinRM enabled!
- **Controller**
  - This is the thing from which the Ansible will run. You'll pull your code down onto the controller and it will then orchestrate everything. Doesn't matter where or what it is as long as it has IP connectivity to Proxmox, Windows Server, the Golden Image VM, and it's running Ubuntu.
- **Intel RST/NVMe driver package** pre-cached on the controller for first run:
  - Put `Intel-RST-7WNN0.exe` in `artifacts/drivers/` before running the pipeline.
  - Download URL: [Intel Rapid Storage Technology Driver and Application 7WNN0 (Dell)](https://dl.dell.com/FOLDER12407846M/2/Intel-Rapid-Storage-Technology-Driver-and-Application_7WNN0_WIN64_20.2.1.1016_A01.EXE)
    - You must manually download this. Dell blocks automation against this website


This project builds for you:
- **Deployer LXC** on Proxmox (PXE, iPXE, DHCP/TFTP/HTTP/SMB services).
  - This is the LXC container that will ultimately get tar'd up and you can go anywhere with it and deploy N workstations.
- **WinPE boot artifacts** and published deployment artifacts.
  - All the things you need to build and boot windows
- **Target workstation VM(s)** booted over PXE and installed from `deploy.wim`.
  - At the end, the code will do a test against a secureboot-enabled, UEFI, Proxmox VM from Deployer LXC just to make sure everything is working

Before you start make sure you have the Windows Server box, the golden image VM, and what will become your controller, up and running.

## Credentials and Ansible Vault

Every secret in this project is stored in **Ansible Vault — always**. There is no plaintext-credential path.

- The setup wizard (`./setup`) **prompts** for each secret (Proxmox root, gold image, WinPE builder, deployer LXC, the deploy-share SMB password, and the workstation break-glass local-admin password) and **encrypts** them into `inventories/windows-deployer/group_vars/all/vault.yml`.
- A vault password file `.vault_pass` is auto-created (`chmod 600`) and referenced by `ansible.cfg` (`vault_password_file = .vault_pass`), so playbooks decrypt automatically with no `--ask-vault-pass`.
- `.vault_pass` and the populated `vault.yml` are **git-ignored**. A fresh clone has no secrets; re-run the wizard to repopulate them. `group_vars/all/main.yml` only references them as `{{ vault_* }}`.
- The **workstation local-admin** is a single break-glass account (username in `windows.workstation_local_admin.username`, password in `vault_workstation_local_admin_password`). It is created silently by `Unattend.xml` so the deployed workstation's OOBE completes with **zero interaction** — see [Unattended OOBE](#unattended-oobe). Real users sign in with **domain** accounts; this account is only a local recovery credential.
- The **delegated domain-join credential** is collected later by the offline TUI (`offline-setup`) on the deployer and stored in the deployer's own vault (`/etc/windows-deployer/secrets.vault.yml`).

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

If you want to rerun the setup, follow the instructions in [Manually run full pipeline without using setup](#manually-run-full-pipeline-without-using-setup)

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

## Portable hostname model

The exported deployer addresses itself by a **stable hostname** (`deployer.offline.hostname`, default `win-deploy`), never a baked IP:

- `deploy.ps1` / `capture.ps1` in `boot.wim` reference `win-deploy`, and the iPXE scripts use `${next-server}`. None of them contain the build IP.
- The deployer's `dnsmasq` is the clients' **only** DNS server (DHCP option 6) and resolves `win-deploy` to its current IP, forwarding everything else upstream.
- Moving the deployer to a new offline IP only requires re-running `offline-setup` (network reconfigure). **No `boot.wim` rebuild is needed.**

## Offline Restore and Use

When you are ready to export the deployer LXC container and bring it to an offline environment, you have two options: the **guided field script** (recommended) or the **manual `pct` steps**.

### Option 1 (recommended): guided field deployment script

Carry the exported tarball (`artifacts/vzdump-lxc-<deployer-vmid>-*.tar.zst`) and `scripts/offline-deploy-deployer.sh` to a machine on the offline network that can reach the offline Proxmox host, then run:

```bash
./scripts/offline-deploy-deployer.sh
```

It walks you through everything:

Requires `sshpass`, `jq`, and an SSH client on the machine running the script. After it finishes, run the offline setup TUI (it tells you exactly how) to configure the offline network and optional domain join.

### Option 2: manual restore

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

7) Run the on-deployer offline setup TUI (configures network + optional domain join).
   Run it from an interactive shell on the node (Proxmox web console or `ssh root@<node>`):

```bash
pct exec <new-vmid> -- offline-setup
```

   If you run it as a one-shot SSH command instead, you MUST pass `-t` so the TUI
   gets a real terminal (otherwise the screen fills with escape codes and input breaks):

```bash
ssh -t root@<node> "pct exec <new-vmid> -- offline-setup"
```

8) Deploy in offline site:
- Ensure target network can PXE boot from the restored deployer.
- Boot target workstation(s) on that network.
- They should chain through iPXE/wimboot and install from `/srv/deploy/images/deploy.wim`.

## How to Force Rebuild

Set force_rebuild to true in the [inventory file](./inventories/windows-deployer/group_vars/all/main.yml)

```yaml
windows:
  winpe_builder:
    force_rebuild: false
```
