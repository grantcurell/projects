# AGENTS.md — Windows Identity Services Deployer

Operational guide for AI agents (and humans) working on this project. Read this
before touching the deploy flow. It captures the architecture, the live-lab
workflow, and the concrete bugs/pitfalls that have already cost real debugging
time — don't rediscover them.

---

## 1. What this project does

PowerShell-driven, config-as-code build of a Windows Server 2025 box into a
single-forest Active Directory domain controller plus the surrounding identity
services (DNS, DHCP, PKI/AD CS, GPOs, hardening, Defender, firewall, backup,
vuln-scanning artifacts, Keycloak/GitLab/YubiKey integration docs).

- **Driver script (runs on the Windows box):** `Configure-WindowsServer.ps1`
- **Config:** YAML (`baseline.yaml` is the live-lab config; `config.example.yaml`
  documents every key; `config.yaml` is the active copy used on the box).
- **Logic:** one file per concern under `lib/` (dot-sourced by the driver).
- **Remote orchestration (runs on the Linux controller):** `scripts/winrm_deploy.py`
  uploads the project + config over WinRM and launches the driver.
- **Harnesses (Linux side):** `tools/live-clean-build.py` (full end-to-end),
  `tools/lab-run-detached.py` (detached driver/monitor — see §6).

### Phases (in order)
`Configure-WindowsServer.ps1` runs these phases, each gated by a completion
marker file so re-runs are idempotent and resumable:

| Phase | Marker file (`*-complete.json` / `ad-promoted.json`) | What it does |
|-------|------|------|
| `Preflight` | `preflight-complete` | Pending-reboot/module/OS checks, rename, **static IP**, **install roles (NOT AD CS)**, verify roles |
| `PromoteDomainController` | `ad-promoted` | `Install-ADDSForest`, then **reboot-and-resume** |
| `PostPromotion` | `post-promotion-complete` | DNS forwarders/zones, DHCP, OUs, groups, service accounts, GPOs, hardening, Defender, firewall, **AD CS install + CA config**, backup/scan artifacts, integration docs |
| `Validate` | `validation-complete` | dcdiag, repadmin, service/DNS/DHCP/GPO/PKI assertions, evidence + final report |

`PlanOnly` runs only `Preflight` + `PromoteDomainController` with all mutating
steps gated by `if ($Context.PlanOnly) { return }`.

---

## 2. Lab environment (topology only — no secrets in git)

- **Target VM:** WinServ2025, VM **110** on **proxmox2**.
- **DC identity:** host `IDENTITY-DC01`, IP `192.168.5.10/24`, GW `192.168.5.1`,
  domain `identity.lab.example.com` (NETBIOS `IDENTITY`). See `baseline.yaml`.
- **Controller:** grantdev LXC on proxmox1.
- **Credentials:** never stored in tracked files. Copy `lab-secrets.env.example` to
  `lab-secrets.env` (gitignored), fill in values locally. All Python harnesses and
  the config wizard load that file automatically via `tools/lab_credentials.py`
  (explicit env vars still override file values). The wizard execute stage also
  prompts for WinRM, DSRM, and service-account passwords.
  Required keys: `WIS_LAB_WINRM_PASSWORD`, `WIS_LAB_DSRM_PASSWORD`,
  `WIS_LAB_SERVICEACCOUNT_PASSWORD`.
- **There is NO DHCP server on this network** until this deploy installs one.
  A NIC left in DHCP mode = dead box. See §5.1.

### Key remote paths (see `scripts/winrm_deploy.py` constants)
- Project on box: `C:\Admin\Windows Identity Services Deployer`
- State/markers: `C:\ProgramData\WindowsIdentityServicesDeployer`
  (`current-phase.json`, `*-complete.json`, `ad-promoted.json`, `failure.json`,
  `Evidence/`, `Logs/`)
- Launcher temp/transcript: `C:\Windows\Temp\WIS\` (`run-configure.ps1`,
  `configure-transcript.log`)

---

## 3. How to check status / find problems (do this FIRST, always)

Status is just marker files — query them cheaply. The single most important
performance rule:

> **NEVER call `Get-WindowsFeature` (or heavy CIM enumeration) in a status/poll
> probe while the box is installing roles.** The servicing stack (`TiWorker`)
> locks it and the call blocks for 30s–4min. A marker-only probe returns in
> ~1–3s. This wasted enormous time before it was understood.

Use `winrm_deploy.query_deploy_status(session)` — it reads marker files only.
For a quick manual probe (domain admin once promoted):

```python
import os, sys
sys.path.insert(0, 'scripts'); sys.path.insert(0, 'tools')
import winrm_deploy, lab_credentials
pw = lab_credentials.lab_winrm_password()
s = winrm_deploy.connect('192.168.5.10', r'IDENTITY\Administrator', pw,
                         read_timeout_sec=25, operation_timeout_sec=20)
print(winrm_deploy.query_deploy_status(s))
```

Where to look when something is wrong:
- **`failure.json`** in the state dir — has `message` + `stack`. This is the
  authoritative cause. (But note: `start_configure` deletes it on each launch —
  see §5.6.)
- **`current-phase.json`** — which phase it was in.
- **`Logs/transcript.log`** and `Logs/operations.jsonl` — phase start/end + errors.
  Transcripts are **buffered**, so the last visible line is NOT necessarily the
  death point. Don't over-trust the tail.
- **`Evidence/final-report.json`** — `Success` / `FailedChecks` after Validate.
- **Process check (light):** look for a `powershell.exe` whose command line
  contains `run-configure.ps1`. A synchronous `run_configure` runs as an
  **encoded command**, so its command line will NOT contain
  `Configure-WindowsServer` — don't rely on that substring for sync runs.

A clean, finished deploy has all four markers
(`preflight-complete`, `ad-promoted`, `post-promotion-complete`,
`validation-complete`), no `failure.json`, and `final-report.json` with
`Success=True`, `FailedChecks=None`. Services ADWS/DNS/DHCPServer/CertSvc/KDC/
Netlogon all `Running`, `domainRole=5`.

---

## 4. How to run a deploy

### Full end-to-end (Linux controller)
```bash
cd "Windows Identity Services Deployer"
cp lab-secrets.env.example lab-secrets.env   # once; fill in passwords locally
python3 tools/live-clean-build.py --config baseline.yaml --host 192.168.5.10
# flags: --skip-upload, --skip-planonly, --clean, --max-wait-minutes N
```

### Detached driver (survives this shell; recommended for long runs)
`tools/lab-run-detached.py` connects (tries local then domain creds), launches
the driver, and monitors via marker files. Launch fully detached so it never
blocks the session:
```bash
cd "Windows Identity Services Deployer"
setsid nohup python3 tools/lab-run-detached.py >/tmp/wis-deploy.out 2>&1 </dev/null &
tail -f /tmp/wis-deploy.log
```

### Most reliable for a stuck/late-stage run: long-held synchronous run
The detached `Start-Process` launcher has been observed dying early in some
states (cause not fully root-caused — see §5.7). When you need a phase to
actually complete, run the driver **synchronously over a long-held WinRM
connection** — the open connection keeps the process alive and captures the
real stdout/stderr. Background it so your own polling doesn't kill it:
```python
import sys; sys.path.insert(0,'scripts'); sys.path.insert(0,'tools')
import winrm_deploy, lab_credentials
pw = lab_credentials.lab_winrm_password()
s = winrm_deploy.connect('192.168.5.10', r'IDENTITY\Administrator', pw,
                         read_timeout_sec=1800, operation_timeout_sec=1790)
code,out,err = winrm_deploy.run_configure(
    s, plan_only=False,
    dsrm_password=lab_credentials.lab_dsrm_password(),
    service_account_password=lab_credentials.lab_service_account_password())
```
**Do NOT let your client time out** — closing the WinRM connection kills the
remote process. Set a generous `read_timeout_sec` and run it in a background
process that holds the connection.

---

## 5. Pitfalls discovered (the expensive ones)

### 5.1 Network: never strand the box without an IP
`lib/Network.ps1 / Set-StaticIPv4FromConfig` originally removed the existing IP
*before* adding the new one. If the add failed/was interrupted, the NIC fell
back to DHCP — and there is **no DHCP server** on this network, so the box went
dark (no route to host, black console). **Fixed:** disable DHCP on the
interface, add the target static IP *first*, reconcile the default route, and
only then remove stale addresses. Never reintroduce remove-then-add ordering.
Also handles "Instance DefaultGateway already exists" when a gateway is already
present (e.g. a manual fix).

### 5.2 AD CS must NOT be installed before promotion
Windows refuses DC promotion if the Certificate Authority role is already
present: *"Verification of prerequisites for Domain Controller promotion failed.
Certificate Server is installed."* **Fixed:** `lib/Roles.ps1` no longer installs
`ADCS-Cert-Authority` in Preflight (and doesn't assert it there). AD CS is
installed in PostPromotion by `Install-AdcsRolesIfEnabled`. If a box already has
ADCS installed from a bad run, `Uninstall-WindowsFeature ADCS-Cert-Authority`
(safe if no CA was configured) before retrying.

### 5.3 PostPromotion must run AFTER a reboot (ADWS timing)
After `Install-ADDSForest`, AD/ADWS are not usable until the box reboots.
Running PostPromotion in the same session fails with *"Unable to find a default
server with Active Directory Web Services running."* **Fixed:**
`Install-ADDSForest -NoRebootOnCompletion`, set
`$Context.RebootRequiredAfterPromotion`, mark `ad-promoted`, then `Restart-Computer`
and exit. The resume path (or the driver) picks up PostPromotion after reboot
once ADWS is online.

### 5.4 Credentials change across promotion
Before promotion: `Administrator` (local). After promotion the account is the
**domain** `IDENTITY\Administrator`; plain local auth can return HTTP 401.
`tools/lab-run-detached.py` tries multiple credential forms. When scripting
manually post-promotion, use `IDENTITY\Administrator`.

### 5.5 StrictMode + optional/empty config sections
`Set-StrictMode -Version Latest` throws *"The property 'X' cannot be found on
this object"* when you dot into a property that doesn't exist. This bit us twice:
- `hardening.localSecurityOptions: {}` (empty map) → `Configure-LocalSecurityOptions`
  blew up. **Fixed** with `Get-OptionalConfigMember` (safe member probe for both
  PSCustomObject and hashtable). Use this helper pattern for any optional section.
- A single selected phase: `Get-IncompleteProjectPhases` returning one element
  gets **unwrapped to a scalar** by PowerShell, so `$selectedPhases.Count` threw.
  **Fixed** by wrapping the call in `@(...)`. Any time you assign a function
  result you will call `.Count`/index on, wrap it in `@()`.

### 5.6 Silent death with no failure.json = parse error OR wiped marker
If a launched process dies leaving **no** `failure.json`, suspect one of:
- A **parse error** in a dot-sourced `lib/*.ps1` or in `Configure-WindowsServer.ps1`
  — these happen before the top-level try/catch, so no marker is written.
  Always parse-check after editing/uploading:
  ```powershell
  $e=$null;$t=$null
  [void][System.Management.Automation.Language.Parser]::ParseFile($path,[ref]$t,[ref]$e)
  if($e){$e|%{$_.Message}}else{'PARSE OK'}
  ```
- `start_configure` **deletes `failure.json` on every launch**. A relaunch loop
  therefore wipes the real error before you can read it. If you're chasing a
  silent failure, stop the loop and run synchronously (§4) to capture stderr.

### 5.7 Don't create relaunch storms
The detached driver historically relaunched the configure process every poll
when it saw `configureInProgress=false`, spawning multiple concurrent runs
(dangerous right before/after DCPromo) and wiping failure markers. The current
`lab-run-detached.py` retries a failure **once** and treats an identical
recurring failure as **fatal**, with bounded relaunches and a post-launch grace
window. If you see attempts 1,2,3,4… climbing every ~20–50s in the log, the box
is dying early every launch — stop and run synchronously to see why. Always
`pkill -9 -f lab-run-detached.py` before starting a new driver.

### 5.8 Invalid OU names at the domain root
`OU=Users` cannot be created at the domain root — it collides with the built-in
`CN=Users` container ("name that is already in use"). The OU-creation code
swallows "already in use" for idempotency, which silently skipped it, and
Validate then failed with "Missing OU". **Fixed** in `baseline.yaml` by renaming
to `OU=Lab Users`. Avoid OU names that collide with built-in containers
(`Users`, `Computers`, `Managed Service Accounts`, `System`, etc.).

### 5.9 Line endings (CRLF) — don't pollute the diff
Tracked files in this repo are **CRLF**. Some editors/tools rewrite them to LF,
producing thousands of lines of phantom diff. Before committing, verify with
`git diff --ignore-all-space --stat`; if the real change is tiny but the raw
diff is huge, convert the file back to CRLF before staging.

### 5.10 Concurrency / single-runner discipline
- `live-clean-build.py` uses a run lock at `/tmp/wis-clean-build.lock`.
- Never run two harnesses (or a CLI agent + IDE agent) against the same box —
  they collide on the run lock, the shared log, and the WinRM shells.

---

## 6. Upload mechanics (and why it's slow)

`winrm_deploy.upload_*` zips the project and ships it in base64 chunks embedded
in `powershell -EncodedCommand`. `CHUNK_SIZE = 1000` is deliberate: larger
values (e.g. 16000) exceed WinRM's command-size limit and return **HTTP 400**.
This means a ~300KB project is hundreds of sequential round trips (~10 min).
Use `--skip-upload` when the project is already on the box and you only changed
state, or upload just the one file you edited with `upload_bytes`.

---

## 7. Pre-commit checklist
- [ ] **No passwords, tokens, or Proxmox/root credentials** in any tracked file
  (`AGENTS.md`, harnesses, docs, YAML). Use `lab-secrets.env` locally only.
- [ ] `git diff --ignore-all-space --stat` shows only intended changes (no EOL churn).
- [ ] Edited `.ps1` files parse cleanly (parser check above) on the box.
- [ ] Do not commit `config.yaml`, `config.yaml.bak.*`, or `lab-secrets.env`.
- [ ] A clean deploy still reaches all four markers + `Success=True`.

---

## 8. Known-good end state (reference)

```
markers: preflight-complete, ad-promoted, post-promotion-complete, validation-complete
failure.json: absent
domain: identity.lab.example.com (NETBIOS IDENTITY), domainRole=5, IDENTITY-DC01 @ 192.168.5.10
services Running: ADWS, DNS, DHCPServer, CertSvc, KDC, Netlogon
Evidence/final-report.json: Success=True, FailedChecks=None
```

> Caveat: the fixes above were validated by driving the failed run to completion
> on a partially-built box (promotion succeeded, then PostPromotion+Validate were
> finished after the code fixes). A full **from-scratch** clean run on a fresh
> snapshot has not yet been re-verified end-to-end. If you revert VM 110 to its
> pre-build snapshot, do one clean automated run to confirm all fixes hold from zero.
