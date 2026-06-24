#!/usr/bin/env python3
"""End-to-end lab test: upload config, PlanOnly, then full deploy with reboot polling."""
from __future__ import annotations

import argparse
import os
import socket
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tools"))
import winrm_deploy  # noqa: E402
import lab_credentials  # noqa: E402

DEFAULT_CONFIG = ROOT / "baseline.yaml"
TARGET_IP = "192.168.5.10"
POLL_CONNECT_TIMEOUT = 90
POLL_INTERVAL_SEC = 30
DEFAULT_MAX_WAIT_MINUTES = 120
LOCK_FILE = Path("/tmp/wis-clean-build.lock")


def acquire_run_lock() -> None:
    if LOCK_FILE.exists():
        try:
            existing = int(LOCK_FILE.read_text().strip())
        except ValueError:
            existing = 0
        if existing and existing != os.getpid():
            try:
                os.kill(existing, 0)
                raise RuntimeError(
                    f"Another live-clean-build is already running (pid {existing}). "
                    "Stop it before starting a new run."
                )
            except OSError:
                pass
    LOCK_FILE.write_text(str(os.getpid()))


def release_run_lock() -> None:
    if LOCK_FILE.exists() and LOCK_FILE.read_text().strip() == str(os.getpid()):
        LOCK_FILE.unlink(missing_ok=True)


def scan_winrm_hosts() -> list[str]:
    found: list[str] = []
    for n in range(1, 255):
        ip = f"192.168.5.{n}"
        sock = socket.socket()
        sock.settimeout(0.08)
        try:
            if sock.connect_ex((ip, 5985)) == 0:
                found.append(ip)
        finally:
            sock.close()
    return found


def connect_lab(host: str):
    return connect_poll(host)


def wait_for_winrm(*prefer: str, attempts: int = 40, delay: int = 15) -> str:
    for attempt in range(attempts):
        for ip in prefer:
            if not ip:
                continue
            try:
                session = connect_lab(ip)
                code, out, _err = winrm_deploy.run_ps(session, "Write-Output WINRM_OK")
                if code == 0 and "WINRM_OK" in out:
                    return ip
            except Exception:
                pass
        for ip in scan_winrm_hosts():
            if ip in prefer:
                continue
            try:
                session = connect_lab(ip)
                code, out, _err = winrm_deploy.run_ps(session, "Write-Output WINRM_OK")
                if code == 0 and "WINRM_OK" in out:
                    return ip
            except Exception:
                pass
        print(f"  waiting for WinRM ({attempt + 1}/{attempts})...", flush=True)
        time.sleep(delay)
    raise RuntimeError("WinRM did not become reachable.")


def clear_remote_state(session) -> None:
    ps = r"""
$ErrorActionPreference = 'SilentlyContinue'
foreach ($p in @(
  'C:\ProgramData\WindowsIdentityServicesDeployer',
  'C:\ProgramData\Configure-WindowsIdentityServices'
)) {
  if (Test-Path -LiteralPath $p) { Remove-Item -LiteralPath $p -Recurse -Force }
}
Unregister-ScheduledTask -TaskName 'WindowsIdentityServicesDeployer-Resume' -Confirm:$false
Write-Output 'STATE_CLEARED'
"""
    code, out, err = winrm_deploy.run_ps(session, ps)
    if code != 0 or "STATE_CLEARED" not in out:
        raise RuntimeError(err or out or "Failed to clear remote state.")


def ensure_no_pending_reboot(session) -> None:
    ps = r"""
$ErrorActionPreference = 'Stop'
$cbs = Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending'
$wu = Test-Path 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired'
$pfr = $false
$sessionMgr = Get-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\Session Manager' -ErrorAction SilentlyContinue
if ($sessionMgr -and $sessionMgr.PSObject.Properties['PendingFileRenameOperations'] -and $sessionMgr.PendingFileRenameOperations) {
  $pfr = $true
}
$computer = Get-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\ComputerName\ActiveComputerName' -ErrorAction SilentlyContinue
$pending = Get-ItemProperty -Path 'HKLM:\SYSTEM\CurrentControlSet\Control\ComputerName\ComputerName' -ErrorAction SilentlyContinue
$crr = $false
if ($computer -and $pending -and $computer.ComputerName -ne $pending.ComputerName) { $crr = $true }
Write-Output "cbs=$cbs wu=$wu pfr=$pfr crr=$crr"
if ($cbs -or $wu -or $pfr -or $crr) { Restart-Computer -Force }
else { Write-Output 'CLEAN' }
"""
    code, out, _err = winrm_deploy.run_ps(session, ps)
    if "CLEAN" in out:
        return
    print("  rebooting to clear pending reboot flags...", flush=True)
    time.sleep(90)
    wait_for_winrm(*scan_winrm_hosts(), TARGET_IP, attempts=30, delay=10)


def verify_domain(session) -> bool:
    ps = rf"""
$ErrorActionPreference = 'Stop'
Write-Output "hostname=$env:COMPUTERNAME"
$ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {{ $_.IPAddress -notlike '127.*' -and $_.IPAddress -notlike '169.*' }} | Select-Object -First 1 -ExpandProperty IPAddress)
Write-Output "ip=$ip"
Import-Module ActiveDirectory -ErrorAction Stop
$domain = Get-ADDomain
Write-Output "dnsroot=$($domain.DNSRoot)"
Write-Output "netbios=$($domain.NetBIOSName)"
Get-Service ADWS,DNS,DHCPServer | ForEach-Object {{ Write-Output "service=$($_.Name) status=$($_.Status)" }}
$summary = 'C:\ProgramData\WindowsIdentityServicesDeployer\Evidence\summary.txt'
Write-Output "summary=$(Test-Path -LiteralPath $summary)"
"""
    code, out, err = winrm_deploy.run_ps(session, ps)
    print(out, flush=True)
    if code != 0:
        print(err[-2000:], flush=True)
        return False
    lower = out.lower()
    return (
        "identity.lab.example.com" in lower
        and "service=adws status=running" in lower.replace(" ", "")
        and "summary=true" in lower.replace(" ", "")
    )


def connect_poll(host: str):
    return winrm_deploy.connect(
        host,
        "Administrator",
        lab_credentials.lab_winrm_password(),
        read_timeout_sec=POLL_CONNECT_TIMEOUT,
        operation_timeout_sec=POLL_CONNECT_TIMEOUT - 10,
    )


def deploy_is_complete(status: dict[str, object]) -> bool:
    # PlanOnly writes Evidence/summary.txt; only validationComplete means full deploy done.
    return bool(status.get("validationComplete") or status.get("converged"))


def deploy_is_in_progress(status: dict[str, object]) -> bool:
    # A registered resume task or stale current-phase.json does NOT mean work is
    # actively running — only a live Configure-WindowsServer process counts.
    return bool(status.get("configureInProgress"))


def run_planonly(host: str, *, max_wait_minutes: int = 15) -> tuple[bool, str]:
    deadline = time.time() + max_wait_minutes * 60
    started = False

    while time.time() < deadline:
        remaining = int(deadline - time.time())
        try:
            session = connect_poll(host)
            status = winrm_deploy.query_deploy_status(session)
            if status.get("planonlyComplete"):
                if status.get("failed"):
                    return False, str(status.get("failureMessage") or "PlanOnly failed")
                return True, "PlanOnly completed"
            if status.get("failed") and not status.get("configureInProgress"):
                return False, str(status.get("failureMessage") or "PlanOnly failed")
            if status.get("configureInProgress"):
                print(
                    f"  PlanOnly running: phase={status.get('phase') or 'pending'} ({remaining}s left)",
                    flush=True,
                )
                started = True
            elif not started:
                print("Starting PlanOnly in background...", flush=True)
                winrm_deploy.start_configure(session, plan_only=True)
                started = True
        except Exception as exc:
            print(f"  WinRM unavailable during PlanOnly: {exc}", flush=True)
        time.sleep(POLL_INTERVAL_SEC)

    return False, f"PlanOnly did not complete within {max_wait_minutes} minutes"


def run_configure_attempt(host: str, *, plan_only: bool) -> tuple[bool, str]:
    # PlanOnly only walks Preflight + PromoteDomainController (both no-ops in plan
    # mode). Run synchronously so pass/fail is immediate; the detached launcher is
    # reserved for full deploy where reboots drop the WinRM session.
    if not plan_only:
        raise ValueError("run_configure_attempt only supports plan_only=True")
    session = winrm_deploy.connect(
        host,
        "Administrator",
        lab_credentials.lab_winrm_password(),
        read_timeout_sec=420,
        operation_timeout_sec=400,
    )
    code, out, err = winrm_deploy.run_configure(session, plan_only=True)
    combined = (out + "\n" + err).strip()
    ok = code == 0 and "RUN_OK" in out
    return ok, combined[-4000:]


def orchestrate_full_deploy(
    start_host: str,
    config_path: Path,
    *,
    uploaded: bool = False,
    max_wait_minutes: int = DEFAULT_MAX_WAIT_MINUTES,
) -> str:
    host = start_host
    deadline = time.time() + max_wait_minutes * 60
    relaunch_count = 0
    max_relaunches = 8

    while time.time() < deadline:
        remaining = int(deadline - time.time())
        try:
            session = connect_poll(host)
            if not uploaded:
                print("Uploading project...", flush=True)
                winrm_deploy.upload_project(session, ROOT, config_path)
                uploaded = True

            status = winrm_deploy.query_deploy_status(session)
            if deploy_is_complete(status):
                print(
                    f"  deploy complete on {host} "
                    f"(phase={status.get('phase')}, hostname={status.get('hostname')})",
                    flush=True,
                )
                return host

            in_progress = deploy_is_in_progress(status)
            if in_progress:
                print(
                    f"  progress: host={host} phase={status.get('phase') or 'pending'} "
                    f"resumeTask={status.get('resumeTaskPresent')} "
                    f"configureRunning={status.get('configureInProgress')} ({remaining}s left)",
                    flush=True,
                )
            else:
                # Not complete and not running: either it has not started yet, it
                # failed, or it died silently. Surface the cause and (re)launch up
                # to a bounded number of times so a transient crash does not stall.
                if status.get("failed"):
                    print(f"  previous failure: {status.get('failureMessage')}", flush=True)
                    tail = status.get("transcriptTail")
                    if tail:
                        print("  --- configure transcript tail ---", flush=True)
                        print(str(tail), flush=True)
                        print("  --- end transcript tail ---", flush=True)
                if relaunch_count >= max_relaunches:
                    raise RuntimeError(
                        f"Configure aborted after {relaunch_count} relaunch attempts. "
                        f"Last failure: {status.get('failureMessage')}"
                    )
                relaunch_count += 1
                print(
                    f"Starting configure in background on {host} "
                    f"(attempt {relaunch_count}/{max_relaunches})...",
                    flush=True,
                )
                winrm_deploy.start_configure(
                    session,
                    plan_only=False,
                    dsrm_password=lab_credentials.lab_dsrm_password(),
                    service_account_password=lab_credentials.lab_service_account_password(),
                )
        except RuntimeError:
            raise
        except Exception as exc:
            print(f"  WinRM unavailable on {host}: {exc}", flush=True)

        try:
            host = wait_for_winrm(TARGET_IP, host, *scan_winrm_hosts(), attempts=3, delay=10)
        except RuntimeError:
            pass

        time.sleep(POLL_INTERVAL_SEC)

    raise RuntimeError(f"Full deploy did not complete within {max_wait_minutes} minutes.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run an idempotent identity-services lab deploy test.")
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--host", default=os.environ.get("WIS_LAB_WINRM_HOST", ""))
    parser.add_argument("--skip-planonly", action="store_true")
    parser.add_argument(
        "--skip-upload",
        action="store_true",
        help="Skip WinRM project upload when the deployer is already on the target.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Clear remote deploy state before running (non-idempotent reset).",
    )
    parser.add_argument(
        "--max-wait-minutes",
        type=int,
        default=int(os.environ.get("WIS_LAB_MAX_WAIT_MINUTES", DEFAULT_MAX_WAIT_MINUTES)),
        help="Wall-clock limit for the full deploy poll loop.",
    )
    args = parser.parse_args()

    if not args.config.exists():
        print(f"Config not found: {args.config}", file=sys.stderr)
        return 1

    acquire_run_lock()
    try:
        return _run(args)
    finally:
        release_run_lock()


def _run(args: argparse.Namespace) -> int:
    prefer = [args.host] if args.host else []
    prefer.extend(scan_winrm_hosts())
    prefer.append(TARGET_IP)
    host = wait_for_winrm(*prefer, attempts=30, delay=10)
    print(f"WinRM host: {host}", flush=True)

    session = connect_lab(host)
    ensure_no_pending_reboot(session)
    host = wait_for_winrm(host, *scan_winrm_hosts(), TARGET_IP, attempts=20, delay=10)

    session = connect_lab(host)
    if args.clean:
        print("Clearing remote state (--clean)...", flush=True)
        clear_remote_state(session)
        ensure_no_pending_reboot(session)
        host = wait_for_winrm(host, *scan_winrm_hosts(), TARGET_IP, attempts=20, delay=10)
        session = connect_lab(host)

    print("Uploading project...", flush=True)
    if not args.skip_upload:
        winrm_deploy.upload_project(session, ROOT, args.config)
        ensure_no_pending_reboot(session)
        host = wait_for_winrm(host, *scan_winrm_hosts(), TARGET_IP, attempts=20, delay=10)
        session = connect_lab(host)
    else:
        print("  skipped (--skip-upload); using existing project on target", flush=True)
    status = winrm_deploy.query_deploy_status(session)
    if deploy_is_complete(status):
        print("Deploy already converged; verifying...", flush=True)
    elif deploy_is_in_progress(status):
        print(
            "Deploy already in progress "
            f"(phase={status.get('phase')}, configureRunning={status.get('configureInProgress')}); resuming poll...",
            flush=True,
        )
    elif not args.skip_planonly:
        print("Running PlanOnly...", flush=True)
        ok, detail = run_configure_attempt(host, plan_only=True)
        print(detail, flush=True)
        if not ok:
            print("PlanOnly FAILED", file=sys.stderr)
            return 1
        print("PlanOnly PASSED", flush=True)

    print("Running full deploy...", flush=True)
    orchestrate_full_deploy(host, args.config, uploaded=True, max_wait_minutes=args.max_wait_minutes)

    verify_host = wait_for_winrm(TARGET_IP, *scan_winrm_hosts(), attempts=30, delay=15)
    print(f"Verifying on {verify_host}...", flush=True)
    session = connect_lab(verify_host)
    if not verify_domain(session):
        print("Domain verification FAILED", file=sys.stderr)
        return 1

    print("DEPLOY PASSED", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
