"""Load lab credentials from lab-secrets.env (gitignored) — never hardcode secrets in repo files."""
from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SECRETS_FILENAME = "lab-secrets.env"
SECRETS_PATH = PROJECT_ROOT / SECRETS_FILENAME

_loaded = False
_secrets_file_loaded = False


def secrets_path() -> Path:
    return SECRETS_PATH


def _parse_env_line(line: str) -> tuple[str, str] | None:
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if line.startswith("export "):
        line = line[7:].strip()
    if "=" not in line:
        return None
    key, _, value = line.partition("=")
    key = key.strip()
    value = value.strip()
    if not key:
        return None
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        value = value[1:-1]
    return key, value


def load_secrets(*, path: Path | None = None) -> bool:
    """Load lab-secrets.env into os.environ (setdefault — explicit env wins)."""
    global _loaded, _secrets_file_loaded
    if _loaded:
        return _secrets_file_loaded
    _loaded = True
    secrets_file = path or SECRETS_PATH
    if not secrets_file.is_file():
        _secrets_file_loaded = False
        return False
    for raw in secrets_file.read_text(encoding="utf-8").splitlines():
        parsed = _parse_env_line(raw)
        if parsed is None:
            continue
        key, value = parsed
        os.environ.setdefault(key, value)
    _secrets_file_loaded = True
    return True


def _get(name: str, *aliases: str, default: str = "") -> str:
    load_secrets()
    for key in (name, *aliases):
        value = os.environ.get(key, "").strip()
        if value:
            return value
    return default


def _require(*names: str) -> str:
    load_secrets()
    for name in names:
        value = os.environ.get(name, "").strip()
        if value:
            return value
    listed = ", ".join(names)
    raise RuntimeError(
        f"Missing required credential ({listed}). "
        f"Copy lab-secrets.env.example to {SECRETS_FILENAME}, fill in values, "
        f"and save as {SECRETS_PATH}. That file is gitignored and loaded automatically."
    )


def lab_winrm_password() -> str:
    return _require("WIS_LAB_WINRM_PASSWORD")


def lab_dsrm_password() -> str:
    return _require("WIS_LAB_DSRM_PASSWORD", "CONFIGURE_WIS_DSRM_PASSWORD")


def lab_service_account_password() -> str:
    return _require("WIS_LAB_SERVICEACCOUNT_PASSWORD", "CONFIGURE_WIS_SERVICEACCOUNT_PASSWORD")


def lab_winrm_password_if_set() -> str:
    return _get("WIS_LAB_WINRM_PASSWORD")


def lab_dsrm_password_if_set() -> str:
    return _get("WIS_LAB_DSRM_PASSWORD", "CONFIGURE_WIS_DSRM_PASSWORD")


def lab_service_account_password_if_set() -> str:
    return _get("WIS_LAB_SERVICEACCOUNT_PASSWORD", "CONFIGURE_WIS_SERVICEACCOUNT_PASSWORD")


def lab_winrm_host() -> str:
    return _get("WIS_LAB_WINRM_HOST", default="192.168.5.10")


def lab_winrm_fallback_host() -> str:
    return _get("WIS_LAB_WINRM_FALLBACK_HOST", default="192.168.5.171")


def lab_winrm_user() -> str:
    return _get("WIS_LAB_WINRM_USER", default="Administrator")


def lab_netbios_name() -> str:
    return _get("WIS_LAB_NETBIOS_NAME", default="IDENTITY")


def lab_domain_dns() -> str:
    return _get("WIS_LAB_DOMAIN_DNS", default="identity.lab.example.com")


def lab_max_wait_minutes(default: int = 120) -> int:
    raw = _get("WIS_LAB_MAX_WAIT_MINUTES")
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError as exc:
        raise RuntimeError("WIS_LAB_MAX_WAIT_MINUTES must be an integer.") from exc


load_secrets()
