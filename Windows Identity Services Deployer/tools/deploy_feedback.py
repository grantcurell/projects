"""Human-readable deploy progress snapshots for lab harnesses."""
from __future__ import annotations

from typing import Any


def _bool(status: dict[str, Any], key: str) -> bool:
    return bool(status.get(key))


def format_marker_row(status: dict[str, Any]) -> str:
    """Compact marker checklist: done=✓ pending=·"""
    items = [
        ("planonly", _bool(status, "planonlyComplete")),
        ("preflight", _bool(status, "preflightComplete")),
        ("promote", _bool(status, "adPromoted")),
        ("post", _bool(status, "postPromotionComplete")),
        ("validate", _bool(status, "validationComplete")),
    ]
    return "  ".join(f"{name} {'✓' if done else '·'}" for name, done in items)


def last_transcript_hint(tail: object) -> str | None:
    if not tail:
        return None
    text = str(tail)
    for line in reversed(text.splitlines()):
        stripped = line.strip()
        if not stripped or stripped.startswith("***"):
            continue
        if stripped.startswith("[INFO ]") or stripped.startswith("[ERROR]"):
            return stripped[:220]
        if "TerminatingError" in stripped or stripped.startswith("ERROR:"):
            return stripped[:220]
    # Fall back to last non-empty line if transcript is still at header-only stage.
    for line in reversed(text.splitlines()):
        stripped = line.strip()
        if stripped and not stripped.startswith("***") and "Host Application:" not in stripped:
            return stripped[:220]
    return None


def describe_likely_activity(status: dict[str, Any]) -> str:
    if _bool(status, "validationComplete"):
        return "Validation finished — deploy should be complete."

    if _bool(status, "failed"):
        msg = status.get("failureMessage") or "unknown error"
        return f"Configure reported failure: {msg}"

    phase = status.get("phase") or "unknown"
    running = _bool(status, "configureInProgress")
    resume = _bool(status, "resumeTaskPresent")
    preflight = _bool(status, "preflightComplete")
    promoted = _bool(status, "adPromoted")
    post = _bool(status, "postPromotionComplete")

    if running:
        hints = {
            "Preflight": (
                "Preflight is running: computer rename, static IP, and Windows role "
                "installs (often 15–30+ minutes; TiWorker keeps configureInProgress "
                "false even while work is happening)."
            ),
            "PromoteDomainController": (
                "Forest promotion is running (Install-ADDSForest). Expect a reboot "
                "when this phase completes."
            ),
            "PostPromotion": (
                "PostPromotion is running: DNS, DHCP, OUs, GPOs, PKI, hardening, "
                "and integration artifacts (longest phase)."
            ),
            "Validate": "Validation is running: dcdiag, service checks, and final report.",
        }
        return hints.get(str(phase), f"Configure process is running (phase={phase}).")

    if resume:
        if promoted and not post:
            return (
                "Resume task is registered after domain promotion — the box may be "
                "rebooting or configure will continue at logon without showing as a "
                "background process yet."
            )
        if not preflight:
            return (
                "Resume task is registered — likely after a rename/static-IP reboot. "
                "Configure should continue at logon; polls may show configureInProgress=false "
                "for a minute or two."
            )
        return (
            "Resume scheduled task is registered. Configure may continue at logon even "
            "when no background powershell process is visible yet."
        )

    if not preflight:
        return (
            "Preflight not complete yet. If you just saw a Windows restart screen, that "
            "is often the rename reboot — wait for WinRM to return and markers to advance."
        )
    if preflight and not promoted:
        return "Preflight complete; waiting for forest promotion (or a promotion reboot)."
    if promoted and not post:
        return "Domain promoted; waiting for PostPromotion (or a post-promotion reboot)."
    if post and not _bool(status, "validationComplete"):
        return "PostPromotion complete; waiting for validation to finish."
    return "Idle between steps — waiting for configure or resume task to advance markers."


def format_deploy_snapshot(
    status: dict[str, Any],
    *,
    host: str,
    remaining_sec: int | None = None,
    relaunch: int | None = None,
    max_relaunches: int | None = None,
    action: str | None = None,
) -> str:
    """Multi-line human snapshot suitable for printing every poll."""
    lines: list[str] = []
    header_bits = ["--- deploy status ---"]
    if relaunch is not None and max_relaunches is not None:
        header_bits.append(f"launch {relaunch}/{max_relaunches}")
    if remaining_sec is not None:
        header_bits.append(f"{remaining_sec}s left")
    lines.append(" ".join(header_bits))

    hostname = status.get("hostname") or "?"
    phase = status.get("phase") or "pending"
    lines.append(f"  target: {host}  hostname: {hostname}  phase: {phase}")
    lines.append(f"  markers: {format_marker_row(status)}")

    proc = "yes" if _bool(status, "configureInProgress") else "no"
    resume = "yes" if _bool(status, "resumeTaskPresent") else "no"
    lines.append(f"  configure process visible: {proc}  resume task: {resume}")

    lines.append(f"  activity: {describe_likely_activity(status)}")

    hint = last_transcript_hint(status.get("transcriptTail"))
    if hint:
        lines.append(f"  transcript: {hint}")

    if action:
        lines.append(f"  action: {action}")

    lines.append("  (next update in ~30s; silence usually means reboot or role install, not failure)")
    return "\n".join(lines)
