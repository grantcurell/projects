#!/usr/bin/env python3
"""Detached deploy driver/monitor for the identity-services lab.

Design notes (hard-won):

  * Poll ONE known host with a SHORT timeout. A busy/rebooting box fails fast and
    is reported as "unreachable, retrying" instead of blocking the loop. Status
    uses only marker-file reads (no Get-WindowsFeature, which stalls for minutes
    while the servicing stack is busy).

  * Credentials change across promotion: before promotion the local
    `Administrator` account works; AFTER the box becomes a domain controller the
    same account is `IDENTITY\\Administrator` and local auth returns HTTP 401. The
    driver tries each candidate and uses whichever authenticates.

  * Anti-storm relaunch logic: the previous version relaunched configure every
    poll whenever it was not running, and start_configure deletes failure.json on
    each launch -- so a process that died with a real error was relaunched
    forever and the error was wiped before it could be seen. Now:
      - a failure is retried at most ONCE; if the SAME failure message recurs the
        driver stops and reports it (fatal, not transient),
      - after issuing a launch the driver waits a grace period and confirms the
        process actually came up before considering another relaunch,
      - relaunches are bounded.

  * Reboots are expected (post-promotion). A dropped connection is treated as
    "rebooting" and simply retried until the box returns.
"""
from __future__ import annotations

import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tools"))
import winrm_deploy  # noqa: E402
import lab_credentials  # noqa: E402
import deploy_feedback  # noqa: E402

PRIMARY_HOST = lab_credentials.lab_winrm_host()
FALLBACK_HOST = lab_credentials.lab_winrm_fallback_host()
NETBIOS = lab_credentials.lab_netbios_name()
DOMAIN_DNS = lab_credentials.lab_domain_dns()

CONNECT_READ_TIMEOUT = 25
CONNECT_OP_TIMEOUT = 20
POLL_INTERVAL_SEC = 20
GRACE_AFTER_LAUNCH_SEC = 45
MAX_WAIT_MINUTES = 90
MAX_RELAUNCHES = 10

LOG_PATH = Path("/tmp/wis-deploy.log")


def cred_candidates() -> list[tuple[str, str]]:
    password = lab_credentials.lab_winrm_password()
    return [
        ("Administrator", password),
        (f"{NETBIOS}\\Administrator", password),
        (f"Administrator@{DOMAIN_DNS}", password),
    ]


def log(msg: str) -> None:
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}"
    print(line, flush=True)
    with LOG_PATH.open("a") as fh:
        fh.write(line + "\n")


def connect_any() -> tuple[object, str, str] | tuple[None, None, None]:
    """Return (session, host, user) for the first host+cred that authenticates."""
    for host in (PRIMARY_HOST, FALLBACK_HOST):
        for user, pw in cred_candidates():
            try:
                session = winrm_deploy.connect(
                    host, user, pw,
                    read_timeout_sec=CONNECT_READ_TIMEOUT,
                    operation_timeout_sec=CONNECT_OP_TIMEOUT,
                )
                winrm_deploy.query_deploy_status(session)  # auth + reachability probe
                return session, host, user
            except Exception:
                continue
    return None, None, None


def clear_failure(session) -> None:
    winrm_deploy.run_ps(
        session,
        r"$f='C:\ProgramData\WindowsIdentityServicesDeployer\failure.json';"
        r"if(Test-Path $f){Remove-Item $f -Force}",
    )


def main() -> int:
    log("=== detached deploy driver started ===")
    deadline = time.time() + MAX_WAIT_MINUTES * 60
    relaunches = 0
    retried_failure: str | None = None
    last_signature: tuple | None = None

    while time.time() < deadline:
        remaining = int(deadline - time.time())
        session, host, user = connect_any()

        if session is None:
            log(
                f"unreachable on all hosts/creds (likely rebooting); retrying ({remaining}s left) — "
                "this is normal during rename/promotion reboots"
            )
            time.sleep(POLL_INTERVAL_SEC)
            continue

        status = winrm_deploy.query_deploy_status(session)
        phase = status.get("phase")
        running = bool(status.get("configureInProgress"))
        failed = bool(status.get("failed"))
        complete = bool(status.get("validationComplete") or status.get("converged"))
        msg = str(status.get("failureMessage") or "")

        action: str | None
        if complete:
            action = "done"
        elif running:
            action = "configure process detected — monitoring"
        elif failed:
            action = "failure seen — will retry once then stop if identical"
        elif relaunches >= MAX_RELAUNCHES:
            action = "max relaunches reached"
        else:
            action = f"launching configure (attempt {relaunches + 1}/{MAX_RELAUNCHES})"

        log(
            deploy_feedback.format_deploy_snapshot(
                status,
                host=host or "?",
                remaining_sec=remaining,
                relaunch=relaunches if relaunches else None,
                max_relaunches=MAX_RELAUNCHES if relaunches else None,
                action=action,
            )
        )

        signature = (host, user, phase, running, failed, complete)
        if signature != last_signature:
            last_signature = signature

        if complete:
            log("DEPLOY COMPLETE (validation marker present)")
            return 0

        if running:
            time.sleep(POLL_INTERVAL_SEC)
            continue

        if failed:
            if retried_failure is not None and msg == retried_failure:
                log(f"FATAL: failure recurred identically, not transient: {msg}")
                tail = status.get("transcriptTail")
                if tail:
                    log("--- transcript tail ---")
                    log(str(tail)[-1500:])
                return 1
            log(f"failure detected (will retry once): {msg}")
            retried_failure = msg
            clear_failure(session)
            # fall through to relaunch

        if relaunches >= MAX_RELAUNCHES:
            log(f"giving up after {relaunches} relaunches; last phase={phase}")
            return 1
        relaunches += 1
        log(f"configure idle -> launching detached as {user} (attempt {relaunches}/{MAX_RELAUNCHES})")
        try:
            winrm_deploy.start_configure(
                session,
                plan_only=False,
                dsrm_password=lab_credentials.lab_dsrm_password(),
                service_account_password=lab_credentials.lab_service_account_password(),
            )
        except Exception as exc:
            log(f"start_configure error (will retry): {exc}")
            time.sleep(POLL_INTERVAL_SEC)
            continue

        # Grace window: confirm it actually came up before allowing another relaunch.
        time.sleep(GRACE_AFTER_LAUNCH_SEC)

    log(f"driver timed out after {MAX_WAIT_MINUTES} minutes")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
