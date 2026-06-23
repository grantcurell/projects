#!/usr/bin/env python3
"""Deploy Windows Identity Services Deployer to lab VM via small WinRM certutil chunks."""
from __future__ import annotations

import base64
import io
import os
import sys
import zipfile
from pathlib import Path

import winrm

ROOT = Path(__file__).resolve().parents[1]
WIN_HOST = os.environ.get("WIS_LAB_WINRM_HOST", "192.168.5.10")
WIN_USER = os.environ.get("WIS_LAB_WINRM_USER", "Administrator")
WIN_PASS = os.environ.get("WIS_LAB_WINRM_PASSWORD", "")
REMOTE_DIR = r"C:\Admin\Windows Identity Services Deployer"
CHUNK_SIZE = 1200
TEMP_DIR = r"C:\Windows\Temp\WISDeploy"


def build_zip() -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in ROOT.rglob("*"):
            if path.is_dir():
                continue
            rel = path.relative_to(ROOT).as_posix()
            if rel.startswith(".git/") or rel == "config.yaml":
                continue
            zf.write(path, rel)
    return buf.getvalue()


def connect() -> winrm.Session:
    if not WIN_PASS:
        raise RuntimeError("Set WIS_LAB_WINRM_PASSWORD before running remote lab tests.")
    return winrm.Session(
        f"http://{WIN_HOST}:5985/wsman",
        auth=(WIN_USER, WIN_PASS),
        transport="ntlm",
        server_cert_validation="ignore",
    )


def run_ps(session: winrm.Session, script: str) -> tuple[int, str, str]:
    result = session.run_ps(script)
    out = (result.std_out or b"").decode("utf-8", errors="replace")
    err = (result.std_err or b"").decode("utf-8", errors="replace")
    return int(result.status_code), out, err


def upload_zip(session: winrm.Session, payload: bytes) -> None:
    chunks = [payload[i : i + CHUNK_SIZE] for i in range(0, len(payload), CHUNK_SIZE)]
    print(f"Uploading {len(payload)} bytes in {len(chunks)} chunk(s)...")

    init_ps = f"""
$ErrorActionPreference = 'Stop'
$dir = '{TEMP_DIR}'
$zipPath = Join-Path $dir 'deploy.zip'
if (Test-Path $dir) {{ Remove-Item -LiteralPath $dir -Recurse -Force }}
New-Item -ItemType Directory -Path $dir -Force | Out-Null
if (Test-Path $zipPath) {{ Remove-Item -LiteralPath $zipPath -Force }}
Write-Output 'INIT_OK'
"""
    code, out, err = run_ps(session, init_ps)
    if code != 0 or "INIT_OK" not in out:
        raise RuntimeError(f"Init failed: {err or out}")

    zip_path = rf"{TEMP_DIR}\deploy.zip"
    for index, chunk in enumerate(chunks):
        encoded = base64.b64encode(chunk).decode("ascii")
        b64_path = rf"{TEMP_DIR}\chunk{index}.b64"
        bin_path = rf"{TEMP_DIR}\chunk{index}.bin"
        script = f"""
$ErrorActionPreference = 'Stop'
@'
{encoded}
'@ | Set-Content -LiteralPath '{b64_path}' -NoNewline -Encoding ASCII
certutil -decode '{b64_path}' '{bin_path}' | Out-Null
$src = [IO.File]::OpenRead('{bin_path}')
$dst = [IO.File]::Open('{zip_path}', [IO.FileMode]::Append, [IO.FileAccess]::Write)
try {{
  $src.CopyTo($dst)
}} finally {{
  $src.Close(); $dst.Close()
}}
Remove-Item -LiteralPath '{b64_path}','{bin_path}' -Force
Write-Output 'CHUNK_OK_{index}'
"""
        code, out, err = run_ps(session, script)
        if code != 0 or f"CHUNK_OK_{index}" not in out:
            raise RuntimeError(f"Chunk {index} failed: {err or out}")
        if (index + 1) % 10 == 0 or index + 1 == len(chunks):
            print(f"  chunk {index + 1}/{len(chunks)} ok")

    deploy_ps = f"""
$ErrorActionPreference = 'Stop'
$zipPath = '{zip_path}'
$dest = '{REMOTE_DIR}'
if (Test-Path $dest) {{ Remove-Item -LiteralPath $dest -Recurse -Force }}
New-Item -ItemType Directory -Path $dest -Force | Out-Null
Expand-Archive -LiteralPath $zipPath -DestinationPath $dest -Force
Write-Output "DEPLOYED_TO=$dest"
Get-ChildItem -LiteralPath $dest | Select-Object -First 12 Name
"""
    code, out, err = run_ps(session, deploy_ps)
    print(out.strip())
    if code != 0:
        raise RuntimeError(err or out)


def main() -> int:
    payload = build_zip()
    print(f"Zip size: {len(payload)} bytes")
    session = connect()

    code, out, err = run_ps(
        session,
        "Write-Output 'WINRM_OK'; hostname; "
        "(Get-CimInstance Win32_OperatingSystem).Caption",
    )
    print(out.strip())
    if code != 0 or "WINRM_OK" not in out:
        return 1

    upload_zip(session, payload)

    validate_ps = f"""
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath '{REMOTE_DIR}'
if (-not (Get-Module -ListAvailable powershell-yaml)) {{
  Install-Module powershell-yaml -Scope AllUsers -Force -AllowClobber
}}
Import-Module powershell-yaml -Force
. '.\\lib\\Config.ps1'
$cfg = Import-ProjectConfig -ConfigPath '.\\config.example.yaml'
Assert-ProjectConfig -Config $cfg
Write-Output 'CONFIG_VALIDATION_OK'
.\\Configure-WindowsServer.ps1 -ConfigPath '.\\config.example.yaml' -PlanOnly
Write-Output 'PLANONLY_OK'
"""
    print("Running Assert-ProjectConfig + PlanOnly...")
    code, out, err = run_ps(session, validate_ps)
    print(out.strip())
    if err.strip():
        print("stderr:", err.strip()[:1500])
    if code != 0:
        return 1
    if "CONFIG_VALIDATION_OK" not in out:
        print("Config validation missing success marker.")
        return 1
    print("Remote lab test complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
