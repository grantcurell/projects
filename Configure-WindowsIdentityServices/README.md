# Configure-WindowsIdentityServices

Turn a **fresh Windows Server** into a fully configured **identity server** — Active
Directory, DNS, DHCP, domain time, a security baseline, and (optionally) PKI/WSUS/log
collection — by editing **one YAML file** and running **one script**.

This is a sibling project to the *Windows Workstation Deployer for Offline Environments*.
The deployer needs a domain to join workstations to; this project **builds that domain**
(the domain controller). It is standalone and is **not** part of the deployer's default
workflow.

> **Read this first.** This automation **changes core infrastructure** and **reboots the
> server**. It builds the **first domain controller in a brand-new forest**. It is **not**
> a migration tool and must **never** be pointed at an existing/production Active Directory
> without a real migration plan.

---

## Table of contents

- [What you get](#what-you-get)
- [When to use it (and when not to)](#when-to-use-it-and-when-not-to)
- [What you need before you start](#what-you-need-before-you-start)
- [Step 1 — Prepare the Windows Server VM](#step-1--prepare-the-windows-server-vm)
- [Step 2 — Copy the project onto the server](#step-2--copy-the-project-onto-the-server)
- [Step 3 — Install the YAML PowerShell module](#step-3--install-the-yaml-powershell-module)
- [Step 4 — Create and edit your config](#step-4--create-and-edit-your-config)
- [Step 5 — Preview without changing anything (PlanOnly)](#step-5--preview-without-changing-anything-planonly)
- [Step 6 — Run it](#step-6--run-it)
- [Step 7 — The reboot (this is normal)](#step-7--the-reboot-this-is-normal)
- [Step 8 — Validate](#step-8--validate)
- [Did it work? Quick health check](#did-it-work-quick-health-check)
- [Where the logs and evidence live](#where-the-logs-and-evidence-live)
- [If something goes wrong (rollback)](#if-something-goes-wrong-rollback)
- [Passwords](#passwords)
- [The golden rule: no defaults in code](#the-golden-rule-no-defaults-in-code)
- [Project layout](#project-layout)

---

## What you get

When the run finishes you will have a Windows Server configured as:

- **Active Directory Domain Services** — a new forest/domain.
- **DNS** — installed with AD, forwarders, and reverse lookup zones.
- **DHCP** — authorized in AD, with your scopes, options, and reservations.
- **Authoritative domain time** (`w32time`) on the PDC emulator.
- **OUs, security groups, and service accounts** from your config.
- **GPO baseline** — password/lockout policy, plus **hardening, firewall, and Defender**
  settings you explicitly turn on.
- **Optional add-ons** (each is off unless you enable it): **PKI** (AD CS), **WSUS**,
  **Windows Event Forwarding**, **Wazuh** agent prep, and **GitLab/Keycloak/YubiKey**
  identity-integration artifacts.
- **Evidence + a final report** so you can prove what was done.

## When to use it (and when not to)

**Use it for:** standing up the **first domain controller in a new forest** on a clean
Windows Server (lab, greenfield site, or the DC the offline deployer will join machines to).

**Do NOT use it for:** adding a DC to an existing domain, migrating, or touching a
production directory. The script refuses to run if the server is already a domain
controller for a *different* domain.

## What you need before you start

- A **Windows Server** VM (Server 2019/2022/2025), freshly installed, **not** domain-joined.
- A **local Administrator** login on that server.
- A **planned static IP**, hostname, domain name, and DNS/DHCP details — written down and
  approved. The script will **not** guess any of these.
- A **maintenance window** — the server reboots during AD promotion.
- Internet access (or a local mirror) **only** to install the `powershell-yaml` module
  once. The script itself never downloads anything from the internet.

## Step 1 — Prepare the Windows Server VM

If the server runs on **Proxmox** (the common case here), do this first so disks and the
network behave:

1. Install Windows Server and finish initial setup.
2. **Mount the VirtIO drivers ISO**: in Proxmox, *VM → Hardware → Add → CD/DVD Drive* and
   attach `virtio-win.iso`. It usually appears as drive `D:`.
3. **Install the VirtIO drivers** (storage + network) from that ISO if Windows did not
   already pick them up.
4. **Install the QEMU Guest Agent** manually: run `D:\virtio-win-guest-tools.exe` and
   complete the wizard. (The script will **not** install it silently unless you explicitly
   allow that in YAML.)
5. In Proxmox, enable the agent under *VM → Options → QEMU Guest Agent*.
6. **Reboot** the server.

> Not on Proxmox? Set `proxmoxGuest.enabled: false` in your config and skip this step.

## Step 2 — Copy the project onto the server

Copy this whole folder to the server, e.g.:

```
C:\Admin\Configure-WindowsIdentityServices
```

Open **PowerShell as Administrator** (right-click → *Run as administrator*). The script
**stops immediately** if it is not elevated or not running on Windows Server.

## Step 3 — Install the YAML PowerShell module

The script reads YAML, so it needs `powershell-yaml`. Install it once:

```powershell
Install-Module powershell-yaml -Scope AllUsers
```

If the module is missing at runtime, the script stops and tells you this exact command.
It will **not** auto-install modules.

## Step 4 — Create and edit your config

Everything the script does comes from your YAML file. Copy the template and edit it:

```powershell
cd C:\Admin\Configure-WindowsIdentityServices
Copy-Item .\config.example.yaml .\config.yaml
notepad .\config.yaml
```

**Go through every value.** At minimum set:

- **Network/identity:** `network.computerName`, `network.interfaceAlias`,
  `network.timeZone`, `network.ipv4.address`, `prefixLength`, `defaultGateway`, and the
  before/after-promotion DNS client servers.
- **Active Directory:** `activeDirectory.domainName`, `netbiosName`, `forestMode`,
  `domainMode`, and the NTDS/SYSVOL paths.
- **DNS:** `dns.forwarders`, `dns.reverseLookupZones`, `dns.requiredRecordsToValidate`.
- **DHCP:** `dhcp.serverDnsName`, `serverIpAddress`, and each scope's
  `scopeId/startRange/endRange/subnetMask` plus router/DNS/NTP options.
- **Time:** `time.externalNtpServers`, `time.ntpFlags`, `time.behaviorIfNotPdc`.
- **Structure:** `organizationalUnits.structure[]`, `groups.items[]`,
  `serviceAccounts.accounts[]`.
- **Policy:** `gpo.gpos[]` (each needs a `linkOrder`), plus `hardening.*`, `firewall.*`,
  `defender.*`.
- **Optional features:** `eventForwarding`, `wazuh`, `pki`, `wsus`, `identityIntegrations`
  — each must be explicitly `enabled: true` or `enabled: false`. If you enable one, fill in
  **all** of its required child values.

Notes:

- `config.yaml` is **git-ignored on purpose** — it holds your real hostnames/IPs/domain.
  Only the generic `config.example.yaml` is shipped.
- The script does **not** read the YAML comments; they are just guidance. Real values must
  be set as real keys.

## Step 5 — Preview without changing anything (PlanOnly)

Always dry-run first. This validates your config and prints every operation it *would*
perform, then exits **without changing the system**:

```powershell
.\Configure-WindowsIdentityServices.ps1 -ConfigPath .\config.yaml -PlanOnly
```

If the config is invalid (missing/empty/contradictory values), it stops here and tells you
**exactly what to fix**. Fix `config.yaml` and re-run until the plan is clean.

## Step 6 — Run it

The simplest path is to run the whole thing — it walks the phases in order and uses a
resume task to continue across the reboot:

```powershell
.\Configure-WindowsIdentityServices.ps1 -ConfigPath .\config.yaml
```

Prefer to go one phase at a time? Run them in this order:

```powershell
.\Configure-WindowsIdentityServices.ps1 -ConfigPath .\config.yaml -Phase Preflight
.\Configure-WindowsIdentityServices.ps1 -ConfigPath .\config.yaml -Phase PromoteDomainController
# --- server reboots here ---
.\Configure-WindowsIdentityServices.ps1 -ConfigPath .\config.yaml -Phase PostPromotion
.\Configure-WindowsIdentityServices.ps1 -ConfigPath .\config.yaml -Phase Validate
```

- **Preflight** — checks elevation/OS/pending-reboot, installs the AD/DNS/DHCP roles.
- **PromoteDomainController** — promotes to a new forest. **Prompts for the DSRM
  (Directory Services Restore Mode) password**, then reboots.
- **PostPromotion** — configures DNS/DHCP/time/OUs/groups/service accounts/GPOs/hardening
  and any optional features you enabled.
- **Validate** — runs `dcdiag`, replication, DNS/DHCP/time checks, and writes the report.

## Step 7 — The reboot (this is normal)

AD promotion **reboots the server**. Don't panic.

1. After it comes back up, **sign in as the domain Administrator**.
2. A scheduled resume task continues the run automatically; resume state lives under
   `execution.statePath` (default `C:\ProgramData\Configure-WindowsIdentityServices`).
3. If you were running phase-by-phase, run the `PostPromotion` command now.

Re-running is safe: the script is idempotent where it can be and picks up from the right
phase instead of starting over.

## Step 8 — Validate

If you didn't run the full pipeline, run validation explicitly:

```powershell
.\Configure-WindowsIdentityServices.ps1 -ConfigPath .\config.yaml -ValidateOnly
```

This writes evidence files and `summary.txt` / `summary.json` / `final-report.json`.

## Did it work? Quick health check

Run these and compare against your config:

```powershell
Get-Service ADWS,DNS,DHCPServer,CertSvc,w32time | Select-Object Name,Status,StartType
Get-ADDomain | Select-Object DNSRoot,NetBIOSName,DomainMode,PDCEmulator
Get-ADForest | Select-Object ForestMode,RootDomain
Get-DnsServerForwarder
Get-DhcpServerv4Scope
w32tm /query /status
```

You want: services **Running**, domain/forest modes matching your config, your DNS
forwarders + reverse zone present, your DHCP scope ranges present, and a healthy NTP
source.

## Where the logs and evidence live

All paths come from `config.yaml` (defaults shown):

- **Transcript log:** `execution.transcriptPath`
- **Structured operation log (JSON Lines):** `execution.jsonLogPath`
- **Evidence + reports:** `execution.evidencePath` — `summary.txt`, `summary.json`,
  `final-report.json`, `dcdiag.txt`, `dcdiag-dns.txt`, `repadmin-replsummary.txt`,
  `GPO\*.html`.
- **State/resume markers:** `current-phase.json`, `preflight-complete.json`,
  `roles-installed.json`, `ad-promoted.json`, `post-promotion-complete.json`,
  `validation-complete.json`, and `failure.json` (only if a run failed).

Secrets are **never** written to logs.

## If something goes wrong (rollback)

Detailed runbooks are in [`docs/`](./docs):

- [`docs/operator-runbook.md`](./docs/operator-runbook.md) — the full operator sequence.
- [`docs/rollback-runbook.md`](./docs/rollback-runbook.md) — how to back out before/after
  promotion, and when a clean rebuild beats a rollback.
- [`docs/ad-backup-restore-runbook.md`](./docs/ad-backup-restore-runbook.md) — system-state
  backup and authoritative vs non-authoritative restore.
- [`docs/security-decisions.md`](./docs/security-decisions.md) — what hardening was applied,
  skipped, or not implemented.
- [`docs/validation-evidence-template.md`](./docs/validation-evidence-template.md) — the
  list of evidence artifacts to expect.

**Honest tip:** for a lab/greenfield box, restoring a pre-promotion VM snapshot is usually
faster and cleaner than unwinding AD. Snapshot the VM **before** Step 6.

## Passwords

You are never asked to put passwords in YAML. By default the script **prompts** securely
for:

- the **DSRM** password during forest promotion, and
- each **service account** password as accounts are created.

For unattended runs you can pre-set them as environment variables (current session only):

```powershell
$env:CONFIGURE_WIS_DSRM_PASSWORD = 'YourStrongDSRMPassword'
$env:CONFIGURE_WIS_SERVICEACCOUNT_PASSWORD = 'YourStrongSvcPassword'
```

The DSRM password is used once and never stored; passwords are never logged.

## The golden rule: no defaults in code

There are **no hard-coded environment defaults** anywhere in the PowerShell. Domain names,
IPs, DNS forwarders, NTP servers, OU/group/account names, GPO names, paths — every
environment-specific value must come from your YAML. If a required value for an enabled
feature is missing, empty, or invalid, the script **stops before changing anything** and
tells you what to fix. It will not silently substitute a guess.

## Project layout

```
Configure-WindowsIdentityServices/
  Configure-WindowsIdentityServices.ps1   # entrypoint
  config.example.yaml                      # template — copy to config.yaml (git-ignored)
  README.md                                # this guide
  lib/                                     # one module per concern (AD, DNS, DHCP, GPO, ...)
  docs/                                     # operator + rollback + backup runbooks
  tests/Pester/                            # config-validation tests (run on a dev box)
  tools/Test-PkiOnHost.ps1                 # optional PKI spot-check helper
```
