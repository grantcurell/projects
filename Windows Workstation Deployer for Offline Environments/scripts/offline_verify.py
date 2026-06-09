#!/usr/bin/env python3
"""Offline-net verification + AD maintenance helper (runs ON the deployer LXC).

The controller is not on the isolated offline network, so every probe that must
reach an offline Windows guest runs here, on the deployer (the only orchestration
node on vmbr27). All operations use WinRM (pywinrm + NTLM). Secrets are read from
environment variables only, never from argv, so they never appear in process
listings or Ansible logs.

Subcommands:
  dc-preflight   Confirm the DC answers WinRM, the AD domain is up, and the target
                 OU exists. Env: DC_USER, DC_PASS.
  workstation    Gather identity/domain/scrub state from an installed workstation.
                 Env: WS_USER, WS_PASS.
  ad-object      Report whether a computer object exists in AD. Env: DC_USER, DC_PASS.
  purge          Remove a stale computer object + its DNS A record. Env: DC_USER, DC_PASS.

Every subcommand prints a single compact JSON object to stdout and exits 0 on a
successful probe (even when the answer is "not present"); it exits non-zero only
when the probe itself could not be carried out (auth/transport failure, etc.).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile


def _ensure_legacy_openssl() -> None:
    """Enable the OpenSSL legacy provider so NTLM's MD4 hash works on OpenSSL 3.

    OpenSSL reads OPENSSL_CONF when its library is first initialized, so simply
    setting the env var here (after the interpreter has already touched OpenSSL)
    is too late. If MD4 is unavailable we write a legacy-enabled config and
    re-exec this process with OPENSSL_CONF pointing at it, so the legacy provider
    is loaded from the very start. A guard env var prevents an exec loop.
    """
    import hashlib

    try:
        hashlib.new("md4")
        return
    except Exception:  # noqa: BLE001
        pass

    if os.environ.get("WINDEPLOY_OPENSSL_REEXEC") == "1":
        # We already re-exec'd with a legacy config but MD4 is still missing.
        return

    conf = tempfile.NamedTemporaryFile(
        prefix="legacy-openssl-", suffix=".cnf", delete=False, mode="w", encoding="utf-8"
    )
    conf.write(
        "openssl_conf = openssl_init\n\n"
        "[openssl_init]\n"
        "providers = provider_sect\n\n"
        "[provider_sect]\n"
        "default = default_sect\n"
        "legacy = legacy_sect\n\n"
        "[default_sect]\n"
        "activate = 1\n\n"
        "[legacy_sect]\n"
        "activate = 1\n"
    )
    conf.close()
    os.environ["OPENSSL_CONF"] = conf.name
    os.environ["WINDEPLOY_OPENSSL_REEXEC"] = "1"
    os.execv(sys.executable, [sys.executable] + sys.argv)


_ensure_legacy_openssl()

import winrm  # noqa: E402


def _winrm_session(host: str, user: str, password: str) -> "winrm.Session":
    return winrm.Session(
        f"http://{host}:5985/wsman",
        auth=(user, password),
        transport="ntlm",
        server_cert_validation="ignore",
    )


def _run_ps(host: str, user: str, password: str, script: str) -> tuple[int, str, str]:
    session = _winrm_session(host, user, password)
    result = session.run_ps(script)
    return (
        int(result.status_code),
        result.std_out.decode("utf-8", errors="replace").strip(),
        result.std_err.decode("utf-8", errors="replace").strip(),
    )


def _fail(message: str, **extra) -> None:
    payload = {"ok": False, "error": message}
    payload.update(extra)
    print(json.dumps(payload, separators=(",", ":")))
    sys.exit(2)


def _emit(payload: dict) -> None:
    payload.setdefault("ok", True)
    print(json.dumps(payload, separators=(",", ":")))
    sys.exit(0)


def cmd_dc_preflight(args: argparse.Namespace) -> None:
    user = os.environ.get("DC_USER", "")
    password = os.environ.get("DC_PASS", "")
    if not user or not password:
        _fail("DC_USER/DC_PASS environment variables are required.")
    script = f"""
$ErrorActionPreference = 'Stop'
Import-Module ActiveDirectory -ErrorAction Stop
$domain = Get-ADDomain
$ouPresent = $false
try {{ if (Get-ADOrganizationalUnit -Identity '{args.ou}') {{ $ouPresent = $true }} }} catch {{ $ouPresent = $false }}
[pscustomobject]@{{
  DnsRoot     = $domain.DNSRoot
  NetBIOSName = $domain.NetBIOSName
  PdcEmulator = $domain.PDCEmulator
  OuPresent   = $ouPresent
}} | ConvertTo-Json -Compress
"""
    try:
        code, out, err = _run_ps(args.dc_ip, user, password, script)
    except Exception as exc:  # noqa: BLE001
        _fail(f"WinRM to DC {args.dc_ip} failed: {exc}")
    if code != 0:
        _fail(f"DC AD preflight PowerShell failed: {err or out}")
    data = json.loads(out)
    dns_ok = (data.get("DnsRoot", "").lower() == args.domain.lower())
    if not dns_ok:
        _fail(
            f"DC reports domain '{data.get('DnsRoot')}', expected '{args.domain}'.",
            dc=data,
        )
    if not data.get("OuPresent"):
        _fail(f"Target OU '{args.ou}' was not found in the domain.", dc=data)
    _emit({"dc": data, "domain_ok": True, "ou_ok": True})


def cmd_workstation(args: argparse.Namespace) -> None:
    user = os.environ.get("WS_USER", "")
    password = os.environ.get("WS_PASS", "")
    if not user or not password:
        _fail("WS_USER/WS_PASS environment variables are required.")
    script = r"""
$ErrorActionPreference = 'Stop'
$bios = Get-CimInstance -ClassName Win32_BIOS
$cs = Get-CimInstance -ClassName Win32_ComputerSystem
$scriptsDir = Join-Path $env:SystemRoot 'Setup\Scripts'
[pscustomobject]@{
  ServiceTag        = ($bios.SerialNumber | Out-String).Trim()
  ComputerName      = $env:COMPUTERNAME
  PartOfDomain      = [bool]$cs.PartOfDomain
  DomainOrWorkgroup = $cs.Domain
  ResidualCredential = (Test-Path (Join-Path $scriptsDir 'join.cred'))
  ResidualJoinScript = (Test-Path (Join-Path $scriptsDir 'first-boot-join.ps1'))
} | ConvertTo-Json -Compress
"""
    try:
        code, out, err = _run_ps(args.ws_ip, user, password, script)
    except Exception as exc:  # noqa: BLE001
        _fail(f"WinRM to workstation {args.ws_ip} failed: {exc}")
    if code != 0:
        _fail(f"Workstation identity PowerShell failed: {err or out}")
    _emit({"workstation": json.loads(out)})


def cmd_ad_object(args: argparse.Namespace) -> None:
    user = os.environ.get("DC_USER", "")
    password = os.environ.get("DC_PASS", "")
    if not user or not password:
        _fail("DC_USER/DC_PASS environment variables are required.")
    script = f"""
$ErrorActionPreference = 'Stop'
Import-Module ActiveDirectory -ErrorAction Stop
$present = $false
$dn = ''
$dns = ''
try {{
  $c = Get-ADComputer -Identity '{args.name}' -Properties dNSHostName
  $present = $true
  $dn = $c.DistinguishedName
  $dns = $c.dNSHostName
}} catch {{ $present = $false }}
[pscustomobject]@{{ Present = $present; DistinguishedName = $dn; DnsHostName = $dns }} | ConvertTo-Json -Compress
"""
    try:
        code, out, err = _run_ps(args.dc_ip, user, password, script)
    except Exception as exc:  # noqa: BLE001
        _fail(f"WinRM to DC {args.dc_ip} failed: {exc}")
    if code != 0:
        _fail(f"AD object lookup PowerShell failed: {err or out}")
    _emit({"computer": json.loads(out)})


def cmd_purge(args: argparse.Namespace) -> None:
    user = os.environ.get("DC_USER", "")
    password = os.environ.get("DC_PASS", "")
    if not user or not password:
        _fail("DC_USER/DC_PASS environment variables are required.")
    script = f"""
$ErrorActionPreference = 'Stop'
Import-Module ActiveDirectory -ErrorAction Stop
$removedComputer = $false
$removedDns = $false
try {{
  $c = Get-ADComputer -Identity '{args.name}' -ErrorAction Stop
  Remove-ADComputer -Identity $c.DistinguishedName -Confirm:$false
  $removedComputer = $true
}} catch {{ }}
try {{
  $zone = '{args.domain}'
  $rec = Get-DnsServerResourceRecord -ZoneName $zone -Name '{args.name}' -RRType A -ErrorAction Stop
  if ($rec) {{ Remove-DnsServerResourceRecord -ZoneName $zone -Name '{args.name}' -RRType A -Force; $removedDns = $true }}
}} catch {{ }}
[pscustomobject]@{{ RemovedComputer = $removedComputer; RemovedDns = $removedDns }} | ConvertTo-Json -Compress
"""
    try:
        code, out, err = _run_ps(args.dc_ip, user, password, script)
    except Exception as exc:  # noqa: BLE001
        _fail(f"WinRM to DC {args.dc_ip} failed: {exc}")
    if code != 0:
        _fail(f"AD/DNS purge PowerShell failed: {err or out}")
    _emit({"purge": json.loads(out)})


def main() -> int:
    parser = argparse.ArgumentParser(description="Offline-net WinRM verification helper (runs on the deployer).")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("dc-preflight")
    p.add_argument("--dc-ip", required=True)
    p.add_argument("--domain", required=True)
    p.add_argument("--ou", required=True)
    p.set_defaults(func=cmd_dc_preflight)

    p = sub.add_parser("workstation")
    p.add_argument("--ws-ip", required=True)
    p.set_defaults(func=cmd_workstation)

    p = sub.add_parser("ad-object")
    p.add_argument("--dc-ip", required=True)
    p.add_argument("--name", required=True)
    p.set_defaults(func=cmd_ad_object)

    p = sub.add_parser("purge")
    p.add_argument("--dc-ip", required=True)
    p.add_argument("--domain", required=True)
    p.add_argument("--name", required=True)
    p.set_defaults(func=cmd_purge)

    args = parser.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
