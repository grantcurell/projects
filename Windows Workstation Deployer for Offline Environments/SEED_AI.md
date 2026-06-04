# SEED_AI.md - Current Agent Handoff for `Windows Workstation Deployer for Offline Environments`

## Purpose

This is the continuity file for future AI edits. It reflects the current known-good direction after recent Secure Boot PXE fixes and deployment hardening.

---

## Project roots and entrypoint

- Repo root: `/home/gcurell/labtracker/projects`
- Project root: `/home/gcurell/labtracker/Windows Workstation Deployer for Offline Environments`
- Main orchestration: `playbooks/site.yml`

---

## Environment model

### Controller
- Supported OS: Ubuntu
- Runs Ansible, setup wizard TUI, and artifact storage under `artifacts/`

### Proxmox / infra
- Proxmox API host configured in inventory (`proxmox.host`)
- Deployer LXC VMID is inventory-driven (current lab: `131`)
- Active test workstation VM is inventory-driven (current lab: `199` on `proxmox2`)

### Windows VMs required
- WinPE builder VM (WinRM reachable)
- Gold image VM (WinRM reachable)

---

## Current known-good/implemented behavior

### 1) Secure Boot iPXE -> WinPE handoff
- `roles/windows_deployer_lxc/templates/autoexec.ipxe.j2` now passes full WinPE boot set to `wimboot`:
  - `BCD`
  - `boot.sdi`
  - `boot.wim`
- UEFI path is explicit and validated over HTTP.
- Diagnostic `pause` remains enabled in Secure Boot `autoexec` for visibility.

### 2) WinPE artifacts staged and validated
- Build pipeline stages and verifies:
  - `boot.wim`
  - `bootmgr`
  - `Boot/BCD`
  - `Boot/boot.sdi`
  - `EFI/Microsoft/Boot/BCD`
  - `EFI/Boot/bootx64.efi`
- Deployer validation checks both filesystem and HTTP availability.

### 3) Deployment script hardening (`files/deploy.ps1`)
- Selects largest suitable writable local disk automatically.
- Generates runtime `diskpart` script bound to selected disk.
- Removes unsafe HTTP download fallback into `W:`.
- Verifies `W:` and EFI partition belong to selected disk.
- Validates BCD exists and is readable via `bcdedit`.

### 4) Post-deploy boot-order behavior
- `playbooks/10-test-workstation-install.yml` now supports:
  - initial install boot order: `windows.test_workstation.boot_order`
  - automatic post-success boot order: `windows.test_workstation.post_deploy_boot_order`
- Current inventory default:
  - `boot_order: order=net0`
  - `post_deploy_boot_order: order=sata0;net0`

---

## Important inventory keys

- `inventories/windows-deployer/group_vars/all.yml`
  - `windows.test_workstation.boot_order`
  - `windows.test_workstation.post_deploy_boot_order`
  - `windows.deploy.*`
  - `deployer.*`
  - `proxmox.*`

No hidden values should be introduced in playbooks/templates.

---

## Expected artifacts (controller + deployer)

Controller `artifacts/`:
- `boot.wim`
- `bootmgr`
- `boot/BCD`
- `boot/boot.sdi`
- `efi/microsoft/boot/BCD`
- `efi/boot/bootx64.efi`
- `winpe_capture.iso`
- `vzdump-lxc-<deployer-vmid>-*.tar.zst`

Deployer:
- `/srv/deploy/images/deploy.wim`

---

## Primary operational flow

1. `./setup` (TUI)
2. bootstrap is run by setup
3. final DEPLOY action launches `scripts/run-full-deploy.sh`
4. pipeline runs `playbooks/site.yml`

Manual fallback:
- `./scripts/bootstrap-controller.sh`
- `ansible-playbook -i inventories/windows-deployer/hosts.yml playbooks/site.yml`

---

## Files most likely to change next

- `roles/windows_deployer_lxc/templates/autoexec.ipxe.j2`
- `roles/windows_deployer_lxc/templates/boot.ipxe.j2`
- `playbooks/07-load-deployment-artifacts.yml`
- `playbooks/08-validate-deployer-lxc.yml`
- `playbooks/10-test-workstation-install.yml`
- `files/deploy.ps1`
- `README.md`

---

## Guardrails for next AI

- Treat Secure Boot handoff issues as pre-Windows-deploy unless proven otherwise.
- Confirm HTTP `200` for `wimboot`, `BCD`, `boot.sdi`, `boot.wim` before blaming WinPE scripts.
- Do not reintroduce writing `deploy.wim` to `W:` in WinPE.
- Keep all runtime behavior inventory-driven.

