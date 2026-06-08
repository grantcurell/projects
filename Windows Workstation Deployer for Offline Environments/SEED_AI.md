# SEED_AI.md - Current Agent Handoff for `Windows Workstation Deployer for Offline Environments`

## Purpose

This is the continuity file for future AI edits. It reflects the current known-good direction after recent Secure Boot PXE fixes, deployment hardening, mandatory Ansible Vault, the portable hostname model, and the online first-boot `Add-Computer` domain-join overhaul.

---

## Credential model (mandatory Ansible Vault)

- ALL secrets are Ansible Vault encrypted. No plaintext-credential path, no "vault optional".
- Online build secrets live in `inventories/windows-deployer/group_vars/all/vault.yml` (encrypted, git-ignored). `group_vars/all/main.yml` references them as `{{ vault_* }}`. `vault.yml.example` documents the variable names.
- `ansible.cfg` sets `vault_password_file = .vault_pass` (auto-managed, `chmod 600`, git-ignored). The wizard (`scripts/environment-wizard.py`) prompts then encrypts via the `ansible-vault` CLI using a labeled vault id (`windeploy@.vault_pass` + `--encrypt-vault-id windeploy`) to avoid the "vault-ids default,default" ambiguity.
- The delegated domain-join credential is stored in the deployer's own vault (`/etc/windows-deployer/secrets.vault.yml`) by the offline TUI, never in Git.
- No `-e ansible_password=` overrides; credentials always come from the vault.

## Portable hostname model (no baked deployer IP)

- WinPE scripts (`files/deploy.ps1`, `files/capture.ps1`) address the deployer by `deployer.offline.hostname` (`win-deploy`), not an IP.
- iPXE templates (`autoexec.ipxe.j2`, `boot.ipxe.j2`) use `${next-server}`.
- `dnsmasq-deploy-pxe.conf.j2` enables DNS, sets DHCP option 6 to the deployer only, resolves `win-deploy` via `address=/`, and forwards upstream (site DNS when domain enabled).
- Moving the deployer to a new IP requires only `offline-setup` network reconfigure — no `boot.wim` rebuild.

## Domain join (online first-boot Add-Computer)

- No ODJ blobs, no `djoin`, no WinRM helper, no offline registry editing.
- Offline TUI (`scripts/offline-deployer-tui.py`, entry point `offline-setup`) runs ON the deployer LXC: domain yes/no -> delegated join credential into vault -> site DNS + AD SRV/LDAP discovery -> create-computer rights preflight -> write `domain.json`/`naming.json` + render `[join]` credential -> network/DNS.
- `scripts/ad_discovery.py` does DNS SRV + LDAP/LDAPS discovery and the non-mutating `allowedChildClassesEffective` create-computer rights check.
- `files/deploy.ps1` stage `stagejoin` drops `SetupComplete.cmd` + `first-boot-join.ps1` (+ transient credential, SYSTEM/Administrators ACL) into the applied image.
- `files/domain-join/first-boot-join.ps1` runs as SYSTEM at first boot: `Add-Computer -NewName <service-tag>` (no `-Restart`), scrub credential + script, then `Restart-Computer -Force`.

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
- `roles/windows_deployer_lxc/templates/autoexec.ipxe.j2` uses `${next-server}` (no baked IP) and passes the full WinPE boot set to `wimboot`:
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
- Addresses the deployer by hostname (`win-deploy`); no baked IP.
- One persistent SMB map (`Ensure-DeployShareMapped`), single unmap in `finally`.
- Reads `Z:\site\domain.json` + `naming.json`; sets computer name from BIOS service tag.
- `stagejoin` drops the first-boot script (+ transient credential when domain enabled); no `djoin`, no offline registry editing.
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

- `inventories/windows-deployer/group_vars/all/main.yml` (non-secret) + `all/vault.yml` (encrypted secrets)
  - `windows.test_workstation.boot_order`
  - `windows.test_workstation.post_deploy_boot_order`
  - `windows.deploy.*`
  - `deployer.offline.*` (stable hostname/fqdn)
  - `deployer.site.domain.*` (domain join: enabled, fqdn, ou_path, dns_servers, ...)
  - `deployer.offline_tui.*` (TUI install dir, config, vault file locations)
  - `deployer.paths.site`, `deployer.paths.join_secret`
  - `deployer.*`
  - `proxmox.*`

No hidden values should be introduced in playbooks/templates. Enforced by the
no-defaults policy: no Jinja `default()` filters, and `playbooks/00-preflight.yml`
asserts every required key (including vault credentials) is defined and non-empty.

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

- `scripts/offline-deployer-tui.py` (offline staged wizard)
- `scripts/ad_discovery.py` (DNS SRV + LDAP discovery / OU rights)
- `files/deploy.ps1` (stagejoin), `files/domain-join/first-boot-join.ps1`
- `roles/windows_deployer_lxc/templates/dnsmasq-deploy-pxe.conf.j2`
- `roles/windows_deployer_lxc/templates/autoexec.ipxe.j2`, `boot.ipxe.j2`
- `playbooks/08-validate-deployer-lxc.yml`
- `playbooks/10-test-workstation-install.yml`
- `README.md`

---

## Guardrails for next AI

- Treat Secure Boot handoff issues as pre-Windows-deploy unless proven otherwise.
- Confirm HTTP `200` for `wimboot`, `BCD`, `boot.sdi`, `boot.wim` before blaming WinPE scripts.
- Do not reintroduce writing `deploy.wim` to `W:` in WinPE.
- Keep all runtime behavior inventory-driven; no Jinja `default()` filters (no-defaults policy).
- Never commit `.vault_pass` or populated `vault.yml` / `secrets.vault.yml`; all secrets via Ansible Vault.
- Domain join is online first-boot `Add-Computer` only — do NOT reintroduce ODJ blobs, `djoin`, a WinRM helper, or offline registry editing.
- The join credential must stay off the nginx web root (authenticated `[join]` SMB only) and be scrubbed on the target after first boot.

