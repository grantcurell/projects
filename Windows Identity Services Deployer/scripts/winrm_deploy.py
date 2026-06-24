"""WinRM helpers to push the deployer project + config.yaml and run Configure-WindowsServer.ps1."""
from __future__ import annotations

import base64
import io
import json
import os
import socket
import time
import uuid
import zipfile
from collections.abc import Callable
from pathlib import Path

REMOTE_DIR = r"C:\Admin\Windows Identity Services Deployer"
TEMP_DIR = r"C:\Windows\Temp\WIS"
# Must match baseline.yaml execution.statePath so the orchestrator and the
# deployer script agree on where failure/completion markers live.
STATE_DIR = r"C:\ProgramData\WindowsIdentityServicesDeployer"
TRANSCRIPT_PATH = rf"{TEMP_DIR}\configure-transcript.log"
# Keep chunks small: each chunk's base64 is embedded in a powershell
# -EncodedCommand, which is subject to WinRM's command-size limit (larger values
# such as 16000 trigger HTTP 400 Bad Request). 1200 is the proven-reliable size.
CHUNK_SIZE = 1000


def build_project_zip(root: Path, *, include_config: Path | None = None) -> bytes:
    skip_prefixes = (
        ".git/",
        "vendor/Modules/powershell-yaml/0.4.7/lib/net35/",
        "vendor/Modules/powershell-yaml/0.4.7/lib/netstandard2.1/",
        "vendor/powershell-yaml/",
    )
    skip_suffixes = (".bak",)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in root.rglob("*"):
            if path.is_dir():
                continue
            rel = path.relative_to(root).as_posix()
            if rel in ("config.yaml", "lab-secrets.env") or rel.startswith("config.yaml.bak."):
                continue
            if rel.startswith(".git/"):
                continue
            if any(rel.startswith(prefix) for prefix in skip_prefixes):
                continue
            if any(rel.endswith(suffix) for suffix in skip_suffixes):
                continue
            zf.write(path, rel)
        if include_config is not None:
            zf.write(include_config, "config.yaml")
    return buf.getvalue()


def run_ps(session, script: str, *, retries: int = 3) -> tuple[int, str, str]:
    last_error: Exception | None = None
    for attempt in range(retries):
        try:
            result = session.run_ps(script)
            out = (result.std_out or b"").decode("utf-8", errors="replace")
            err = (result.std_err or b"").decode("utf-8", errors="replace")
            return int(result.status_code), out, err
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt + 1 >= retries:
                break
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(str(last_error or "WinRM PowerShell execution failed."))


def upload_bytes(session, target_path: str, payload: bytes, *, work_dir: str | None = None) -> None:
    # Each chunk is written to its own part file (partN.bin) and the parts are
    # assembled deterministically at the end. This makes every step idempotent and
    # retry-safe: a lost WinRM response that triggers a retry simply rewrites the
    # same partN.bin instead of double-appending to a shared file (which silently
    # corrupted the zip in the old append-based scheme).
    chunks = [payload[i : i + CHUNK_SIZE] for i in range(0, len(payload), CHUNK_SIZE)]
    n = len(chunks)
    total = len(payload)
    staging = work_dir or rf"{TEMP_DIR}\{uuid.uuid4().hex[:12]}"
    init_ps = f"""
$ErrorActionPreference = 'Stop'
$tempRoot = '{TEMP_DIR}'
if (-not (Test-Path -LiteralPath $tempRoot)) {{ New-Item -ItemType Directory -Path $tempRoot -Force | Out-Null }}
$dir = '{staging}'
if (-not (Test-Path $dir)) {{ New-Item -ItemType Directory -Path $dir -Force | Out-Null }}
Get-ChildItem -LiteralPath $dir -Filter 'part*.b64' -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
Get-ChildItem -LiteralPath $dir -Filter 'part*.bin' -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
if (Test-Path -LiteralPath '{target_path}') {{ Remove-Item -LiteralPath '{target_path}' -Force }}
Write-Output 'INIT_OK'
"""
    code, out, err = run_ps(session, init_ps)
    if code != 0 or "INIT_OK" not in out:
        raise RuntimeError(err or out or "Upload init failed.")

    for index, chunk in enumerate(chunks):
        encoded = base64.b64encode(chunk).decode("ascii")
        b64_path = rf"{staging}\part{index}.b64"
        bin_path = rf"{staging}\part{index}.bin"
        expected = len(chunk)
        script = f"""
$ErrorActionPreference = 'Stop'
@'
{encoded}
'@ | Set-Content -LiteralPath '{b64_path}' -NoNewline -Encoding ASCII
certutil -decode '{b64_path}' '{bin_path}' | Out-Null
Remove-Item -LiteralPath '{b64_path}' -Force -ErrorAction SilentlyContinue
Write-Output 'CHUNK_OK_{index}'
"""
        code, out, err = run_ps(session, script)
        if code != 0 or f"CHUNK_OK_{index}" not in out:
            raise RuntimeError(f"Upload chunk {index} failed: {err or out}")
        if (index + 1) % 5 == 0 or index + 1 == n:
            print(f"  uploaded chunk {index + 1}/{n}", flush=True)

    assemble_ps = f"""
$ErrorActionPreference = 'Stop'
$dir = '{staging}'
$target = '{target_path}'
if (Test-Path -LiteralPath $target) {{ Remove-Item -LiteralPath $target -Force }}
$dst = [IO.File]::Open($target, [IO.FileMode]::Create, [IO.FileAccess]::Write)
try {{
  for ($i = 0; $i -lt {n}; $i++) {{
    $p = Join-Path $dir ("part{{0}}.bin" -f $i)
    if (-not (Test-Path -LiteralPath $p)) {{ throw "missing part $i during assembly" }}
    $src = [IO.File]::OpenRead($p)
    try {{ $src.CopyTo($dst) }} finally {{ $src.Close() }}
  }}
}} finally {{ $dst.Close() }}
$finalLen = (Get-Item -LiteralPath $target).Length
if ($finalLen -ne {total}) {{ throw "assembled size mismatch: got $finalLen expected {total}" }}
Write-Output "ASSEMBLED_OK=$finalLen"
"""
    code, out, err = run_ps(session, assemble_ps)
    if code != 0 or "ASSEMBLED_OK=" not in out:
        raise RuntimeError(f"Upload assembly failed: {err or out}")

    cleanup_ps = f"""
$ErrorActionPreference = 'SilentlyContinue'
Get-ChildItem -LiteralPath '{staging}' -Filter 'part*.bin' -ErrorAction SilentlyContinue | Remove-Item -Force -ErrorAction SilentlyContinue
Write-Output 'STAGING_CLEARED'
"""
    run_ps(session, cleanup_ps)


def upload_project(session, root: Path, config_path: Path) -> None:
    payload = build_project_zip(root, include_config=config_path)
    upload_id = uuid.uuid4().hex[:12]
    staging = rf"{TEMP_DIR}\{upload_id}"
    zip_path = rf"{staging}\deploy.zip"
    upload_bytes(session, zip_path, payload, work_dir=staging)
    deploy_ps = f"""
$ErrorActionPreference = 'Stop'
$zipPath = '{zip_path}'
$dest = '{REMOTE_DIR}'
if (Test-Path $dest) {{ Remove-Item -LiteralPath $dest -Recurse -Force }}
New-Item -ItemType Directory -Path $dest -Force | Out-Null
Expand-Archive -LiteralPath $zipPath -DestinationPath $dest -Force
Write-Output "DEPLOYED_TO=$dest"
"""
    code, out, err = run_ps(session, deploy_ps)
    if code != 0 or "DEPLOYED_TO=" not in out:
        raise RuntimeError(err or out or "Project deploy failed.")


def _configure_env_block(
    dsrm_password: str | None,
    service_account_password: str | None,
) -> str:
    env_lines = []
    if dsrm_password:
        env_lines.append(f"$env:CONFIGURE_WIS_DSRM_PASSWORD = '{dsrm_password.replace(chr(39), chr(39)*2)}'")
    if service_account_password:
        env_lines.append(
            f"$env:CONFIGURE_WIS_SERVICEACCOUNT_PASSWORD = '{service_account_password.replace(chr(39), chr(39)*2)}'"
        )
    env_block = "\n".join(env_lines)
    if env_block:
        env_block += "\n"
    return env_block


def _configure_prepare_script(env_block: str) -> str:
    return f"""
$ErrorActionPreference = 'Stop'
{env_block}Set-Location -LiteralPath '{REMOTE_DIR}'
$vendorModules = Join-Path (Get-Location) 'vendor\\Modules'
if (Test-Path $vendorModules) {{
  $env:PSModulePath = "$vendorModules;" + $env:PSModulePath
}}
if (-not (Get-Module -ListAvailable powershell-yaml)) {{
  if (Test-Path (Join-Path $vendorModules 'powershell-yaml\\0.4.7\\powershell-yaml.psd1')) {{
    Write-Output 'MODULE_PATH_VENDOR'
  }} else {{
    Set-PSRepository -Name PSGallery -InstallationPolicy Trusted
    Install-Module powershell-yaml -Scope AllUsers -Force -AllowClobber -Repository PSGallery
    Write-Output 'MODULE_INSTALLED_FROM_GALLERY'
  }}
}}
Import-Module powershell-yaml -Force
. '.\\lib\\Config.ps1'
$cfg = Import-ProjectConfig -ConfigPath '.\\config.yaml'
Assert-ProjectConfig -Config $cfg
Write-Output 'CONFIG_VALIDATION_OK'
"""


def run_configure(
    session,
    *,
    plan_only: bool,
    dsrm_password: str | None = None,
    service_account_password: str | None = None,
) -> tuple[int, str, str]:
    flag = " -PlanOnly" if plan_only else ""
    env_block = _configure_env_block(dsrm_password, service_account_password)
    script = (
        _configure_prepare_script(env_block)
        + f".\\Configure-WindowsServer.ps1 -ConfigPath '.\\config.yaml'{flag}\n"
        + "Write-Output 'RUN_OK'\n"
    )
    return run_ps(session, script)


def start_configure(
    session,
    *,
    plan_only: bool,
    dsrm_password: str | None = None,
    service_account_password: str | None = None,
) -> None:
    """Launch Configure-WindowsServer.ps1 in a detached process (survives WinRM reboot drops)."""
    status = query_deploy_status(session)
    if status.get("configureInProgress"):
        return
    if plan_only and status.get("planonlyComplete"):
        return
    if not plan_only and (status.get("validationComplete") or status.get("converged")):
        return

    flag = " -PlanOnly" if plan_only else ""
    env_block = _configure_env_block(dsrm_password, service_account_password)
    launch_path = rf"{TEMP_DIR}\run-configure.ps1"
    # The launched script is wrapped in transcript + try/catch so a death before or
    # within Configure-WindowsServer.ps1 (module import, parse error, etc.) still
    # leaves a durable failure marker. Without this the poll loop cannot distinguish
    # "still running" from "died silently" and waits out the whole deadline.
    script = f"""
$ErrorActionPreference = 'Stop'
$tempDir = '{TEMP_DIR}'
if (-not (Test-Path -LiteralPath $tempDir)) {{ New-Item -ItemType Directory -Path $tempDir -Force | Out-Null }}
$stateRoot = '{STATE_DIR}'
if (-not (Test-Path -LiteralPath $stateRoot)) {{ New-Item -ItemType Directory -Path $stateRoot -Force | Out-Null }}
$failFile = Join-Path $stateRoot 'failure.json'
if (Test-Path -LiteralPath $failFile) {{ Remove-Item -LiteralPath $failFile -Force }}
$launchPath = '{launch_path}'
@'
$ErrorActionPreference = 'Stop'
$stateRoot = '{STATE_DIR}'
if (-not (Test-Path -LiteralPath $stateRoot)) {{ New-Item -ItemType Directory -Path $stateRoot -Force | Out-Null }}
try {{ Start-Transcript -Path '{TRANSCRIPT_PATH}' -Force | Out-Null }} catch {{}}
try {{
{env_block}  Set-Location -LiteralPath '{REMOTE_DIR}'
  $vendorModules = Join-Path (Get-Location) 'vendor\\Modules'
  if (Test-Path $vendorModules) {{
    $env:PSModulePath = "$vendorModules;" + $env:PSModulePath
  }}
  Import-Module powershell-yaml -Force
  .\\Configure-WindowsServer.ps1 -ConfigPath '.\\config.yaml'{flag}
}}
catch {{
  try {{
    @{{ timestamp = (Get-Date).ToString('o'); message = $_.Exception.Message; stack = [string]$_.ScriptStackTrace; source = 'launcher' }} |
      ConvertTo-Json -Depth 6 | Set-Content -LiteralPath (Join-Path $stateRoot 'failure.json') -Encoding UTF8
  }} catch {{}}
  throw
}}
finally {{
  try {{ Stop-Transcript | Out-Null }} catch {{}}
}}
'@ | Set-Content -LiteralPath $launchPath -Encoding UTF8
$proc = Start-Process -FilePath 'powershell.exe' -ArgumentList @('-NoProfile','-ExecutionPolicy','Bypass','-File',$launchPath) -WindowStyle Hidden -PassThru
Start-Sleep -Seconds 2
$matches = @(Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" -ErrorAction SilentlyContinue |
  Where-Object {{ $_.CommandLine -like '*Configure-WindowsServer.ps1*' -or $_.CommandLine -like '*run-configure.ps1*' }})
if (@($matches).Count -eq 0) {{
  throw 'Configure process did not start (no matching powershell.exe within 2s).'
}}
"CONFIGURE_STARTED pid=$($proc.Id) matches=$($matches.Count)"
"""
    code, out, err = run_ps(session, script)
    if code != 0 or "CONFIGURE_STARTED" not in out:
        raise RuntimeError(err or out or "Failed to start configure in background.")


def query_deploy_status(session) -> dict[str, object]:
    ps = rf"""
$ErrorActionPreference = 'SilentlyContinue'
$base = 'C:\ProgramData\WindowsIdentityServicesDeployer'
$result = [ordered]@{{
  hostname = $env:COMPUTERNAME
  phase = $null
  validationComplete = $false
  planonlyComplete = $false
  converged = $false
  failed = $false
  failureMessage = $null
  summaryExists = $false
  resumeTaskPresent = $false
  configureInProgress = $false
  transcriptTail = $null
}}
$phaseFile = Join-Path $base 'current-phase.json'
if (Test-Path -LiteralPath $phaseFile) {{
  $raw = Get-Content -LiteralPath $phaseFile -Raw | ConvertFrom-Json
  if ($raw.currentPhase) {{ $result.phase = [string]$raw.currentPhase }}
}}
$result.validationComplete = Test-Path -LiteralPath (Join-Path $base 'validation-complete.json')
$result.planonlyComplete = Test-Path -LiteralPath (Join-Path $base 'planonly-complete.json')
$result.converged = $result.validationComplete
$result.summaryExists = Test-Path -LiteralPath (Join-Path $base 'Evidence\summary.txt')
$failFile = Join-Path $base 'failure.json'
if (Test-Path -LiteralPath $failFile) {{
  $result.failed = $true
  $fail = Get-Content -LiteralPath $failFile -Raw | ConvertFrom-Json
  $result.failureMessage = [string]$fail.message
}}
$taskName = 'WindowsIdentityServicesDeployer-Resume'
$result.resumeTaskPresent = $null -ne (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue)
$configureMatches = Get-CimInstance Win32_Process -Filter "Name='powershell.exe'" -ErrorAction SilentlyContinue |
  Where-Object {{ $_.CommandLine -like '*Configure-WindowsServer.ps1*' -or $_.CommandLine -like '*run-configure.ps1*' }}
$result.configureInProgress = @($configureMatches).Count -gt 0
$transcript = '{TRANSCRIPT_PATH}'
if (Test-Path -LiteralPath $transcript) {{
  $result.transcriptTail = (Get-Content -LiteralPath $transcript -Tail 25 -ErrorAction SilentlyContinue) -join "`n"
}}
$result | ConvertTo-Json -Compress
"""
    code, out, err = run_ps(session, ps)
    if code != 0 or not out.strip():
        raise RuntimeError(err or out or "Failed to query deploy status.")
    return json.loads(out.strip())


def wait_for_deploy(
    host: str,
    user: str,
    password: str,
    *,
    plan_only: bool,
    dsrm_password: str | None = None,
    service_account_password: str | None = None,
    max_wait_minutes: int = 120,
    poll_interval_sec: int = 30,
    on_status: Callable[[dict[str, object]], None] | None = None,
) -> dict[str, object]:
    deadline = time.time() + max_wait_minutes * 60
    started = False
    while time.time() < deadline:
        try:
            session = connect(host, user, password, read_timeout_sec=90, operation_timeout_sec=80)
            status = query_deploy_status(session)
        except Exception:
            time.sleep(poll_interval_sec)
            for ip in [host, "192.168.5.10"]:
                sock = socket.socket()
                sock.settimeout(0.2)
                try:
                    if sock.connect_ex((ip, 5985)) == 0:
                        host = ip
                finally:
                    sock.close()
            continue
        if on_status:
            on_status(status)
        if plan_only:
            if status.get("planonlyComplete"):
                if status.get("failed"):
                    raise RuntimeError(str(status.get("failureMessage") or "PlanOnly failed."))
                return status
        elif status.get("validationComplete") or status.get("converged") or status.get("summaryExists"):
            return status
        if status.get("failed") and not status.get("configureInProgress"):
            raise RuntimeError(str(status.get("failureMessage") or "Deploy failed."))
        if not started and not status.get("configureInProgress"):
            start_configure(
                session,
                plan_only=plan_only,
                dsrm_password=dsrm_password,
                service_account_password=service_account_password,
            )
            started = True
        time.sleep(poll_interval_sec)
        for ip in [host, "192.168.5.10"]:
            sock = socket.socket()
            sock.settimeout(0.2)
            try:
                if sock.connect_ex((ip, 5985)) == 0:
                    host = ip
            finally:
                sock.close()
    raise RuntimeError(f"Deploy did not complete within {max_wait_minutes} minutes.")


def connect(
    host: str,
    user: str,
    password: str,
    *,
    read_timeout_sec: int = 3600,
    operation_timeout_sec: int = 3500,
):
    import winrm

    if not password:
        raise RuntimeError("WinRM password is required.")
    return winrm.Session(
        f"http://{host}:5985/wsman",
        auth=(user, password),
        transport="ntlm",
        server_cert_validation="ignore",
        read_timeout_sec=read_timeout_sec,
        operation_timeout_sec=operation_timeout_sec,
    )
