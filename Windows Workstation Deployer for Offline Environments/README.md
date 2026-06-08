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
  - [Domain join (online first-boot)](#domain-join-online-first-boot)
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
  - Download URL: [Intel Rapid Storage Technology Driver and Application 7WNN0 (Dell)](https://dl.dell.com/FOLDER12407846M/2/Intel-Rapid-Storage-Technology-Driver-and-Application_7WNN0_WIN64_20.2.1.1016_A01.EXE)


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

- The setup wizard (`./setup`) **prompts** for each secret (Proxmox root, gold image, WinPE builder, deployer LXC, and the deploy-share SMB password) and **encrypts** them into `inventories/windows-deployer/group_vars/all/vault.yml`.
- A vault password file `.vault_pass` is auto-created (`chmod 600`) and referenced by `ansible.cfg` (`vault_password_file = .vault_pass`), so playbooks decrypt automatically with no `--ask-vault-pass`.
- `.vault_pass` and the populated `vault.yml` are **git-ignored**. A fresh clone has no secrets; re-run the wizard to repopulate them. `group_vars/all/main.yml` only references them as `{{ vault_* }}`.
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

7) Run the on-deployer offline setup TUI (configures network + optional domain join):

```bash
pct exec <new-vmid> -- offline-setup
```

8) Deploy in offline site:
- Ensure target network can PXE boot from the restored deployer.
- Boot target workstation(s) on that network.
- They should chain through iPXE/wimboot and install from `/srv/deploy/images/deploy.wim`.

## Domain join (online first-boot)

This deployer joins workstations to AD **online, at first boot**, using `Add-Computer` — there are **no ODJ blobs, no `djoin`, and no WinRM helper**. The deployer itself never joins the domain.

Flow:

1. On the deployer, run `offline-setup` and choose **Enable domain join? Yes**.
2. Enter a **delegated** join account (UPN `user@domain` or `DOMAIN\user`) — **not Domain Admin**. It is stored in the deployer's Ansible Vault.
3. Provide the **site DNS server(s)** (which may or may not be the domain controller). The TUI runs AD SRV + LDAP discovery, confirms the account can **create computer objects** in the chosen OU, and resolves the DC — all before any workstation is deployed. There is no manual fallback; the wizard cannot advance past a failed check.
4. The TUI writes non-secret `domain.json` / `naming.json` to `/srv/deploy/site` and renders the join credential from the vault to the protected, off-web `[join]` SMB share (`/var/lib/windows-deployer/join`, mode `0700`).
5. During PXE deploy, `deploy.ps1` sets the computer name from the BIOS service tag and stages a SYSTEM-context `SetupComplete.cmd` + `first-boot-join.ps1` (plus the transient credential) into the image — no domain contact in WinPE.
6. At first boot, `first-boot-join.ps1` runs `Add-Computer -NewName <service-tag> -DomainName ... -OUPath ... -Credential ... -Force` (never `-Restart`), then **scrubs the credential and itself**, and only then calls `Restart-Computer -Force`. The machine reboots domain-joined and named after its service tag.

The join credential lives off the nginx web root and is served only over authenticated SMB; it exists on the target for a single boot and is then scrubbed.

## How to Force Rebuild

Set force_rebuild to true in the [inventory file](./inventories/windows-deployer/group_vars/all/main.yml)

```yaml
windows:
  winpe_builder:
    force_rebuild: false
```
