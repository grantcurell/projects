"""Load lab credentials from the environment — never hardcode secrets in repo files."""
from __future__ import annotations

import os


def _require(*names: str) -> str:
    for name in names:
        value = os.environ.get(name, "").strip()
        if value:
            return value
    listed = ", ".join(names)
    raise RuntimeError(
        f"Missing required credential env var. Set one of: {listed}. "
        "Copy lab-secrets.env.example to lab-secrets.env (gitignored) and "
        "run: set -a && source lab-secrets.env && set +a"
    )


def lab_winrm_password() -> str:
    return _require("WIS_LAB_WINRM_PASSWORD")


def lab_dsrm_password() -> str:
    return _require("WIS_LAB_DSRM_PASSWORD", "CONFIGURE_WIS_DSRM_PASSWORD")


def lab_service_account_password() -> str:
    return _require("WIS_LAB_SERVICEACCOUNT_PASSWORD", "CONFIGURE_WIS_SERVICEACCOUNT_PASSWORD")
