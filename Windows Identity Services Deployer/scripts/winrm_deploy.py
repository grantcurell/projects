"""WinRM helpers to push the deployer project + config.yaml and run Configure-WindowsServer.ps1."""
from __future__ import annotations

import base64
import io
import zipfile
from pathlib import Path

REMOTE_DIR = r"C:\Admin\Windows Identity Services Deployer"
TEMP_DIR = r"C:\Windows\Temp\WISDeploy"
CHUNK_SIZE = 1200


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
            if rel.startswith(".git/") or rel == "config.yaml":
                continue
            if rel.startswith("config.yaml.bak."):
                continue
            if any(rel.startswith(prefix) for prefix in skip_prefixes):
                continue
            if any(rel.endswith(suffix) for suffix in skip_suffixes):
                continue
            zf.write(path, rel)
        if include_config is not None:
            zf.write(include_config, "config.yaml")
    return buf.getvalue()


def run_ps(session, script: str) -> tuple[int, str, str]:
    result = session.run_ps(script)
    out = (result.std_out or b"").decode("utf-8", errors="replace")
    err = (result.std_err or b"").decode("utf-8", errors="replace")
    return int(result.status_code), out, err


def upload_bytes(session, target_path: str, payload: bytes) -> None:
    chunks = [payload[i : i + CHUNK_SIZE] for i in range(0, len(payload), CHUNK_SIZE)]
    init_ps = f"""
$ErrorActionPreference = 'Stop'
$dir = '{TEMP_DIR}'
if (-not (Test-Path $dir)) {{ New-Item -ItemType Directory -Path $dir -Force | Out-Null }}
$path = '{target_path}'
if (Test-Path $path) {{ Remove-Item -LiteralPath $path -Force }}
Write-Output 'INIT_OK'
"""
    code, out, err = run_ps(session, init_ps)
    if code != 0 or "INIT_OK" not in out:
        raise RuntimeError(err or out or "Upload init failed.")

    for index, chunk in enumerate(chunks):
        encoded = base64.b64encode(chunk).decode("ascii")
        b64_path = rf"{TEMP_DIR}\part{index}.b64"
        bin_path = rf"{TEMP_DIR}\part{index}.bin"
        script = f"""
$ErrorActionPreference = 'Stop'
@'
{encoded}
'@ | Set-Content -LiteralPath '{b64_path}' -NoNewline -Encoding ASCII
certutil -decode '{b64_path}' '{bin_path}' | Out-Null
$src = [IO.File]::OpenRead('{bin_path}')
$dst = [IO.File]::Open('{target_path}', [IO.FileMode]::Append, [IO.FileAccess]::Write)
try {{ $src.CopyTo($dst) }} finally {{ $src.Close(); $dst.Close() }}
Remove-Item -LiteralPath '{b64_path}','{bin_path}' -Force
Write-Output 'CHUNK_OK_{index}'
"""
        code, out, err = run_ps(session, script)
        if code != 0 or f"CHUNK_OK_{index}" not in out:
            raise RuntimeError(f"Upload chunk {index} failed: {err or out}")
        if (index + 1) % 10 == 0 or index + 1 == len(chunks):
            print(f"  uploaded chunk {index + 1}/{len(chunks)}", flush=True)


def upload_project(session, root: Path, config_path: Path) -> None:
    payload = build_project_zip(root, include_config=config_path)
    zip_path = rf"{TEMP_DIR}\deploy.zip"
    upload_bytes(session, zip_path, payload)
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


def run_configure(
    session,
    *,
    plan_only: bool,
    dsrm_password: str | None = None,
    service_account_password: str | None = None,
) -> tuple[int, str, str]:
    flag = " -PlanOnly" if plan_only else ""
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
    script = f"""
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
.\\Configure-WindowsServer.ps1 -ConfigPath '.\\config.yaml'{flag}
Write-Output 'RUN_OK'
"""
    return run_ps(session, script)


def connect(host: str, user: str, password: str):
    import winrm

    if not password:
        raise RuntimeError("WinRM password is required.")
    return winrm.Session(
        f"http://{host}:5985/wsman",
        auth=(user, password),
        transport="ntlm",
        server_cert_validation="ignore",
        read_timeout_sec=3600,
        operation_timeout_sec=3500,
    )
