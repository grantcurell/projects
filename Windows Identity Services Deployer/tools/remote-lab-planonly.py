#!/usr/bin/env python3
"""Upload lab config.yaml and run PlanOnly against the promoted lab DC."""
from __future__ import annotations

import base64
import os
from pathlib import Path

import winrm

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = Path(__file__).resolve().parent / "lab-config.yaml"
HOST = os.environ.get("WIS_LAB_WINRM_HOST", "192.168.5.10")
USER = os.environ.get("WIS_LAB_WINRM_USER", "Administrator")
PASSWORD = os.environ.get("WIS_LAB_WINRM_PASSWORD", "")
REMOTE = r"C:\Admin\Windows Identity Services Deployer"
TEMP_DIR = r"C:\Windows\Temp\WISDeploy"
CHUNK_SIZE = 1200


def session() -> winrm.Session:
    if not PASSWORD:
        raise RuntimeError("Set WIS_LAB_WINRM_PASSWORD before running remote lab tests.")
    return winrm.Session(
        f"http://{HOST}:5985/wsman",
        auth=(USER, PASSWORD),
        transport="ntlm",
        server_cert_validation="ignore",
        read_timeout_sec=300,
        operation_timeout_sec=240,
    )


def run_ps(script: str) -> tuple[int, str, str]:
    result = session().run_ps(script)
    out = (result.std_out or b"").decode("utf-8", errors="replace")
    err = (result.std_err or b"").decode("utf-8", errors="replace")
    return int(result.status_code), out, err


def upload_bytes(target_path: str, payload: bytes) -> None:
    chunks = [payload[i : i + CHUNK_SIZE] for i in range(0, len(payload), CHUNK_SIZE)]
    init_ps = f"""
$ErrorActionPreference = 'Stop'
$dir = '{TEMP_DIR}'
if (-not (Test-Path $dir)) {{ New-Item -ItemType Directory -Path $dir -Force | Out-Null }}
$path = '{target_path}'
if (Test-Path $path) {{ Remove-Item -LiteralPath $path -Force }}
Write-Output 'INIT_OK'
"""
    code, out, err = run_ps(init_ps)
    if code != 0 or "INIT_OK" not in out:
        raise RuntimeError(err or out)

    for index, chunk in enumerate(chunks):
        encoded = base64.b64encode(chunk).decode("ascii")
        b64_path = rf"{TEMP_DIR}\cfg{index}.b64"
        bin_path = rf"{TEMP_DIR}\cfg{index}.bin"
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
        code, out, err = run_ps(script)
        if code != 0 or f"CHUNK_OK_{index}" not in out:
            raise RuntimeError(f"chunk {index}: {err or out}")


def main() -> int:
    payload = CONFIG_PATH.read_bytes()
    remote_config = rf"{REMOTE}\config.yaml"
    print(f"Uploading lab config ({len(payload)} bytes)...")
    upload_bytes(remote_config, payload)

    ps = f"""
$ErrorActionPreference = 'Stop'
Write-Output '=== identity ==='
hostname
(Get-CimInstance Win32_ComputerSystem).Domain
Get-Service ADWS,DNS,DHCPServer -ErrorAction SilentlyContinue | Format-Table Name,Status -AutoSize | Out-String
Set-Location -LiteralPath '{REMOTE}'
.\\Configure-WindowsServer.ps1 -ConfigPath '.\\config.yaml' -PlanOnly
Write-Output 'PLANONLY_OK'
"""
    print("Running PlanOnly with lab config.yaml...")
    code, out, err = run_ps(ps)
    print(out)
    if err.strip():
        print("stderr:", err.strip()[-3000:])
    return 0 if code == 0 and "PLANONLY_OK" in out else 1


if __name__ == "__main__":
    raise SystemExit(main())
