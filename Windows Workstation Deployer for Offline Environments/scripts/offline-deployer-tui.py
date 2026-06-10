#!/usr/bin/env python3
"""Offline deployer setup TUI (runs ON the deployer LXC at the intranet site).

Staged wizard:
  Stage 1  Enable domain join? (Yes/No)
  Stage 2  Join credential (needs create/join computer rights in the target OU;
           a delegated account is enough, Domain Admin not required) -> Ansible Vault
  Stage 3  Site DNS server(s) (may or may not be the DC) + AD SRV/LDAP discovery
  Stage 4  Confirm discovered domain/OU; create-computer rights preflight;
           write non-secret domain.json/naming.json; render the [join] credential
  Stage 5  Network/DNS/services: deployer is the only client DNS and forwards to
           the site DNS; re-render dnsmasq; restart services; final resolution checks

Security model: the deployer never joins the domain. The delegated credential is
prompted, encrypted into a deployer-local Ansible Vault, and rendered only to the
protected off-web [join] share. The actual join happens online at first boot on the
workstation via Add-Computer.
"""
from __future__ import annotations

import ipaddress
import json
import os
import secrets as secrets_lib
import subprocess
import sys
import threading
from pathlib import Path
from typing import Any

import yaml
from textual import events, on, work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll
from textual.widgets import Button, ContentSwitcher, Footer, Input as TextInput, Log, ProgressBar, Select, Static

INSTALL_DIR = Path(__file__).resolve().parent
if str(INSTALL_DIR) not in sys.path:
    sys.path.insert(0, str(INSTALL_DIR))

import ad_discovery  # noqa: E402


DEFAULT_CONFIG_PATH = "/etc/windows-deployer/offline-config.yml"


# Labeled vault id keeps CLI encrypt/decrypt unambiguous (see environment-wizard.py).
VAULT_ID = "windeploy"


def _ansible_env() -> dict[str, str]:
    """Environment for ansible-vault subprocesses with a guaranteed-valid locale.

    Minimal container images often have LANG/LC_* pointing at a locale that was
    never generated, which makes Ansible abort with 'could not initialize the
    preferred locale: unsupported locale setting'. Force C.UTF-8 (always present
    on modern glibc/musl) so encrypt/decrypt works regardless of the host locale.
    """
    env = dict(os.environ)
    env["LC_ALL"] = "C.UTF-8"
    env["LANG"] = "C.UTF-8"
    env.pop("LANGUAGE", None)
    return env


def load_offline_config() -> dict[str, Any]:
    path = Path(os.environ.get("WINDEPLOY_OFFLINE_CONFIG", DEFAULT_CONFIG_PATH))
    if not path.exists():
        raise RuntimeError(
            f"Offline config {path} not found. The LXC role installs it during the online build."
        )
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"Invalid offline config in {path}.")
    required = [
        "offline_hostname",
        "offline_hostname_fqdn",
        "site_path",
        "join_secret_path",
        "vault_password_file",
        "vault_secrets_file",
    ]
    missing = [k for k in required if not data.get(k)]
    if missing:
        raise RuntimeError(f"Offline config is missing required keys (no defaults): {missing}")
    return data


# ---------------------------------------------------------------------------
# Deployer-local Ansible Vault helpers
# ---------------------------------------------------------------------------
def ensure_vault_pass(pass_file: Path) -> None:
    if pass_file.exists() and pass_file.read_text(encoding="utf-8").strip():
        return
    pass_file.parent.mkdir(parents=True, exist_ok=True)
    pass_file.write_text(secrets_lib.token_urlsafe(48) + "\n", encoding="utf-8")
    pass_file.chmod(0o600)


def load_vault(vault_file: Path, pass_file: Path) -> dict[str, Any]:
    if not vault_file.exists() or not pass_file.exists():
        return {}
    try:
        proc = subprocess.run(
            ["ansible-vault", "view", str(vault_file), "--vault-id", f"{VAULT_ID}@{pass_file}"],
            capture_output=True,
            text=True,
            check=True,
            env=_ansible_env(),
        )
    except Exception:  # noqa: BLE001
        return {}
    data = yaml.safe_load(proc.stdout)
    return data if isinstance(data, dict) else {}


def write_vault(secrets: dict[str, str], vault_file: Path, pass_file: Path) -> None:
    ensure_vault_pass(pass_file)
    vault_file.parent.mkdir(parents=True, exist_ok=True)
    tmp = vault_file.with_suffix(".plain.tmp")
    tmp.write_text(yaml.safe_dump(secrets, sort_keys=True), encoding="utf-8")
    try:
        proc = subprocess.run(
            [
                "ansible-vault", "encrypt", str(tmp), "--output", str(vault_file),
                "--vault-id", f"{VAULT_ID}@{pass_file}", "--encrypt-vault-id", VAULT_ID,
            ],
            capture_output=True,
            text=True,
            check=False,
            env=_ansible_env(),
        )
        if proc.returncode != 0:
            raise RuntimeError(f"ansible-vault encrypt failed: {proc.stderr.strip() or proc.stdout.strip()}")
    finally:
        if tmp.exists():
            tmp.unlink()
    vault_file.chmod(0o600)


# ---------------------------------------------------------------------------
# Widgets (mirror environment-wizard keyboard behavior)
# ---------------------------------------------------------------------------
class PersistentSelect(Select):
    """Select widget with stable keyboard behavior for open dropdown navigation."""

    def on_focus(self) -> None:
        # Never auto-open when merely focused.
        self.expanded = False

    def _cycle_option(self, direction: int) -> None:
        options = [opt for _, opt in self._options if opt is not Select.NULL]
        if not options:
            return
        current = self.value
        try:
            idx = options.index(current)
        except ValueError:
            idx = 0
        self.value = options[(idx + direction) % len(options)]
        self.action_show_overlay()

    def on_key(self, event: events.Key) -> None:
        if event.key == "q" and hasattr(self.app, "quit_armed") and bool(getattr(self.app, "quit_armed")):
            self.app.exit()
            event.stop()
            return
        if self.expanded and event.key in {"down"}:
            self._cycle_option(1)
            event.stop()
            return
        if self.expanded and event.key in {"up"}:
            self._cycle_option(-1)
            event.stop()
            return


class Input(TextInput):
    """Input that honors global Esc->q quit flow while focused."""

    def on_key(self, event: events.Key) -> None:
        app = self.app
        if event.key == "q" and hasattr(app, "quit_armed") and bool(getattr(app, "quit_armed")):
            app.exit()
            event.stop()
            return
        if event.key == "escape" and not self.selection.is_empty:
            # Cancel the edit: deselect the highlighted value WITHOUT deleting it.
            # (Fields auto-select-all on focus, so Esc here means "leave it alone".)
            # Only fall through to the global Esc->q quit flow when nothing is
            # highlighted.
            self.cursor_position = self.cursor_position
            event.stop()
            event.prevent_default()
            return


# ---------------------------------------------------------------------------
# TUI
# ---------------------------------------------------------------------------
class OfflineSetupApp(App[None]):
    CSS = """
    Screen {
        layout: vertical;
    }
    #status {
        height: 1;
        padding: 0 1;
    }
    #help {
        height: 1;
        padding: 0 1;
    }
    #control_legend {
        height: 1;
        padding: 0 1;
    }
    #stage_progress {
        height: 1;
    }
    #main-switcher {
        height: 1fr;
        min-height: 8;
        border: round $panel;
        padding: 0 1;
    }
    .stage {
        height: 1fr;
    }
    #stage-deploy {
        align: center middle;
    }
    .deploy-center {
        width: 1fr;
        height: 1fr;
        align: center middle;
    }
    #deploy_now {
        width: 32;
        height: 5;
        border: round #ff4d4f;
        background: #7f1d1d;
        color: #ffffff;
        text-style: bold;
    }
    .field {
        margin-bottom: 1;
    }
    Input:focus {
        border: round #2d8cff;
        background: #10243a;
    }
    Select:focus {
        border: round #2d8cff;
        background: #10243a;
    }
    Select:focus-within {
        border: round #2d8cff;
        background: #10243a;
    }
    Button:focus {
        border: round #2d8cff;
        background: #0b3a66;
    }
    .actions {
        margin-top: 1;
    }
    .stage-nav {
        margin-top: 1;
        height: 3;
    }
    .nav-button {
        min-width: 16;
    }
    #log {
        height: 6;
        border: round $secondary;
    }
    """

    BINDINGS = [
        ("tab", "focus_next_field", "Next Field"),
        ("shift+tab", "focus_prev_field", "Prev Field"),
        ("q", "quit", "Quit"),
    ]

    STAGE_ORDER = ["stage-domain", "stage-network", "stage-cred", "stage-dns", "stage-confirm", "stage-done"]

    def __init__(self) -> None:
        super().__init__()
        self.cfg = load_offline_config()
        self.vault_file = Path(self.cfg["vault_secrets_file"])
        self.vault_pass = Path(self.cfg["vault_password_file"])
        self.site_path = Path(self.cfg["site_path"])
        self.join_path = Path(self.cfg["join_secret_path"])
        self.offline_hostname = str(self.cfg["offline_hostname"])
        self.offline_hostname_fqdn = str(self.cfg["offline_hostname_fqdn"])
        self.existing_vault = load_vault(self.vault_file, self.vault_pass)
        self.discovery: dict[str, Any] = {}
        self.net: dict[str, Any] = {}
        self.current_stage = "stage-domain"
        self.quit_armed = False

    def compose(self) -> ComposeResult:
        yield Static("Stage 1/5: Enable domain join?", id="status")
        yield Static("Controls: Tab/Shift+Tab move fields, arrows navigate fields/options, Enter opens/selects dropdown options, q = Quit.", id="help")
        yield Static("", id="control_legend")
        yield ProgressBar(total=5, show_eta=False, show_percentage=True, id="stage_progress")
        with ContentSwitcher(initial="stage-domain", id="main-switcher"):
            with VerticalScroll(id="stage-domain", classes="stage"):
                yield Static("Stage 1: Join deployed workstations to an Active Directory domain?")
                yield PersistentSelect(
                    options=[("Yes - enable domain join", "yes"), ("No - workgroup only", "no")],
                    value="no",
                    id="domain_enabled",
                    classes="field",
                )
                with Horizontal(classes="stage-nav"):
                    yield Button("Next", id="next_domain", variant="primary", classes="nav-button")
            with VerticalScroll(id="stage-cred", classes="stage"):
                yield Static("Stage 3: Domain join account (UPN user@domain or DOMAIN\\user). Must have rights to create and join computer objects in the target OU. A delegated account with that right is sufficient - Domain Admin works but is not required.")
                yield Static("Join account username")
                yield Input(str(self.existing_vault.get("vault_domain_join_username") or ""), id="join_user", classes="field")
                yield Static("Join account password")
                yield Input("", password=True, id="join_pass", classes="field")
                with Horizontal(classes="stage-nav"):
                    yield Button("Back", id="back_cred", classes="nav-button")
                    yield Button("Next", id="next_cred", variant="primary", classes="nav-button")
            with VerticalScroll(id="stage-dns", classes="stage"):
                yield Static("Stage 4: Site DNS server(s) that answer AD records (comma-separated). May or may not be the DC.")
                yield Static("─" * 80)
                yield Static("Domain FQDN (e.g. corp.example.com)")
                yield Input("", id="domain_fqdn", classes="field")
                yield Static("Site DNS server IP(s)")
                yield Input("", id="dns_servers", classes="field")
                with Horizontal(classes="stage-nav"):
                    yield Button("Back", id="back_dns", classes="nav-button")
                    yield Button("Discover", id="next_dns", variant="primary", classes="nav-button")
            with VerticalScroll(id="stage-confirm", classes="stage"):
                yield Static("Stage 5: Confirm discovered domain settings. The join account's OU rights are verified, then services are applied.")
                yield Static("Domain controller")
                yield PersistentSelect(options=[("(discover first)", "")], value="", id="sel_dc", classes="field")
                yield Static("Target OU for new computer objects")
                yield PersistentSelect(options=[("(discover first)", "")], value="", id="sel_ou", classes="field")
                with Horizontal(classes="stage-nav"):
                    yield Button("Back", id="back_confirm", classes="nav-button")
                    yield Button("Verify + Finish", id="next_confirm", variant="success", classes="nav-button")
            with VerticalScroll(id="stage-network", classes="stage"):
                yield Static("Stage 2: Deployer network (PXE/DHCP/DNS service). Clients use the deployer as their ONLY DNS; it forwards to the site DNS. Pre-filled from the address set during field deployment.")
                yield Static("Deployer IP (current offline IP)")
                yield Input("", id="net_ip", classes="field")
                yield Static("CIDR prefix (e.g. 24)")
                yield Input("24", id="net_prefix", classes="field")
                yield Static("Gateway")
                yield Input("", id="net_gateway", classes="field")
                yield Static("DHCP range start")
                yield Input("", id="net_dhcp_start", classes="field")
                yield Static("DHCP range end")
                yield Input("", id="net_dhcp_end", classes="field")
                yield Static("Upstream/general DNS (non-AD lookups)")
                yield Input("", id="net_dns", classes="field")
                with Horizontal(classes="stage-nav"):
                    yield Button("Back", id="back_network", classes="nav-button")
                    yield Button("Next", id="next_network", variant="primary", classes="nav-button")
            with VerticalScroll(id="stage-done", classes="stage"):
                yield Static("Setup complete. The deployer is ready.", id="done_title")
                yield Static("", id="done_summary")
        yield Log(id="log", highlight=True, auto_scroll=True)
        yield Footer()

    # -- lifecycle --------------------------------------------------------
    def on_mount(self) -> None:
        self.append_log("Offline deployer setup started.")
        self._prefill_network_from_interface()
        self._refresh_controls()
        self._update_progress()
        self.set_focus(self.query_one("#domain_enabled", Select))

    def _detect_interface(self) -> dict[str, str]:
        """Read eth0's live IPv4/prefix and the default gateway (set by the
        field-deploy script) so the network stage is pre-filled correctly."""
        info: dict[str, str] = {}
        try:
            out = subprocess.run(
                ["ip", "-4", "-o", "addr", "show", "eth0"],
                capture_output=True, text=True, check=False,
            ).stdout
            for tok in out.split():
                if "/" in tok and tok.count(".") == 3:
                    ip, _, prefix = tok.partition("/")
                    if prefix.isdigit() and not ip.startswith("169.254"):
                        info["ip"], info["prefix"] = ip, prefix
                        break
        except Exception:  # noqa: BLE001
            pass
        try:
            parts = subprocess.run(
                ["ip", "route", "show", "default"],
                capture_output=True, text=True, check=False,
            ).stdout.split()
            if "via" in parts:
                info["gateway"] = parts[parts.index("via") + 1]
        except Exception:  # noqa: BLE001
            pass
        return info

    def _prefill_network_from_interface(self) -> None:
        net = self._detect_interface()
        if not net.get("ip"):
            self.append_log("[WARN] Could not detect an IPv4 address on eth0; fill network fields manually.")
            return
        ip, prefix = net["ip"], net.get("prefix", "24")
        self.query_one("#net_ip", Input).value = ip
        self.query_one("#net_prefix", Input).value = prefix
        if net.get("gateway"):
            self.query_one("#net_gateway", Input).value = net["gateway"]
        self.append_log(f"Detected deployer address {ip}/{prefix} on eth0 (from field deployment).")

        # Derive a convenience DHCP pool inside the subnet. The upstream/general
        # DNS field is intentionally left blank here: the gateway is rarely a
        # resolver, so we backfill it from the site DNS after discovery instead.
        try:
            network = ipaddress.ip_network(f"{ip}/{prefix}", strict=False)
            hosts = list(network.hosts())
            if len(hosts) >= 210:
                self.query_one("#net_dhcp_start", Input).value = str(hosts[99])   # .100-ish
                self.query_one("#net_dhcp_end", Input).value = str(hosts[199])    # .200-ish
        except ValueError:
            pass

    def append_log(self, message: str) -> None:
        # Safe to call from worker threads: marshal back onto the UI thread.
        if threading.current_thread() is threading.main_thread():
            self.query_one("#log", Log).write_line(message)
        else:
            self.call_from_thread(self.query_one("#log", Log).write_line, message)

    def set_status(self, message: str) -> None:
        if threading.current_thread() is threading.main_thread():
            self.query_one("#status", Static).update(message)
        else:
            self.call_from_thread(self.query_one("#status", Static).update, message)

    def switch_stage(self, stage_id: str, label: str) -> None:
        self.query_one("#main-switcher", ContentSwitcher).current = stage_id
        self.current_stage = stage_id
        self.set_status(label)
        self._refresh_controls()
        self._update_progress()
        focusables = self._stage_focusables()
        if focusables:
            self.set_focus(focusables[0])
            if isinstance(focusables[0], Select):
                focusables[0].expanded = False

    def _update_progress(self) -> None:
        idx = {"stage-domain": 1, "stage-network": 2, "stage-cred": 3, "stage-dns": 4, "stage-confirm": 5, "stage-done": 5}
        self.query_one("#stage_progress", ProgressBar).update(progress=idx.get(self.current_stage, 1))

    def _refresh_controls(self) -> None:
        legend = self.query_one("#control_legend", Static)
        suffix = " | Quit: Esc then q" if not self.quit_armed else " | Quit armed: press q now"
        legend.update(f"Fill fields, then focus a button and press Enter.{suffix}")

    def _stage_focusables(self) -> list[Any]:
        stage = self.query_one(f"#{self.current_stage}")
        widgets: list[Any] = []
        for widget in stage.query("Input, Select, Button"):
            if isinstance(widget, (Input, Select, Button)) and not widget.disabled:
                widgets.append(widget)
        return widgets

    def _stage_buttons(self) -> list[Button]:
        stage = self.query_one(f"#{self.current_stage}")
        buttons: list[Button] = []
        for widget in stage.query("Button"):
            if isinstance(widget, Button) and not widget.disabled:
                buttons.append(widget)
        return buttons

    def _resolve_focus_owner(self, focused: object, fields: list[Any]) -> Any:
        if focused in fields:
            return focused
        node = focused
        # If focus is in a child (e.g., Select overlay), walk up to an owning focusable.
        while node is not None and hasattr(node, "parent"):
            node = getattr(node, "parent")
            if node in fields:
                return node
        return None

    def _ensure_focus_visible_target(self) -> None:
        fields = self._stage_focusables()
        if not fields:
            return
        owner = self._resolve_focus_owner(self.focused, fields)
        if owner is None:
            self.set_focus(fields[0])

    def _input(self, widget_id: str) -> str:
        return self.query_one(f"#{widget_id}", Input).value.strip()

    def _select(self, widget_id: str) -> str:
        value = self.query_one(f"#{widget_id}", Select).value
        return "" if value is None else str(value)

    # -- navigation -------------------------------------------------------
    def action_focus_next_field(self) -> None:
        self._ensure_focus_visible_target()
        fields = self._stage_focusables()
        if not fields:
            return
        current = self._resolve_focus_owner(self.focused, fields)
        if current in fields:
            idx = fields.index(current)
            self.set_focus(fields[(idx + 1) % len(fields)])
        else:
            self.set_focus(fields[0])

    def action_focus_prev_field(self) -> None:
        self._ensure_focus_visible_target()
        fields = self._stage_focusables()
        if not fields:
            return
        current = self._resolve_focus_owner(self.focused, fields)
        if current in fields:
            idx = fields.index(current)
            self.set_focus(fields[(idx - 1) % len(fields)])
        else:
            self.set_focus(fields[-1])

    def action_focus_button_right(self) -> None:
        buttons = self._stage_buttons()
        if len(buttons) < 2:
            return
        current = self.focused
        if current in buttons:
            idx = buttons.index(current)
            self.set_focus(buttons[(idx + 1) % len(buttons)])

    def action_focus_button_left(self) -> None:
        buttons = self._stage_buttons()
        if len(buttons) < 2:
            return
        current = self.focused
        if current in buttons:
            idx = buttons.index(current)
            self.set_focus(buttons[(idx - 1) % len(buttons)])

    def _move_open_select(self, select: Select, direction: int) -> None:
        options = [opt for _, opt in select._options if opt is not Select.NULL]
        if not options:
            return
        current = select.value
        try:
            idx = options.index(current)
        except ValueError:
            idx = 0
        next_idx = (idx + direction) % len(options)
        select.value = options[next_idx]
        # Keep dropdown open while navigating with arrows.
        select.action_show_overlay()

    def on_key(self, event: events.Key) -> None:
        if event.key in {"escape"}:
            # Mac and Windows terminals both send "escape" here.
            if isinstance(self.focused, Select) and bool(self.focused.expanded):
                # Let Select close its own overlay.
                return
            self.quit_armed = True
            self._refresh_controls()
            self.append_log("Quit armed. Press q to quit.")
            event.stop()
            return
        if event.key in {"q"} and self.quit_armed:
            self.exit()
            event.stop()
            return

        # Up/Down navigate fields globally, except when a Select dropdown
        # is expanded (in that case, navigate the open dropdown's options).
        if event.key in {"down"}:
            self.quit_armed = False
            self._refresh_controls()
            if isinstance(self.focused, Select) and bool(self.focused.expanded):
                self._move_open_select(self.focused, 1)
                event.stop()
                return
            self.action_focus_next_field()
            event.stop()
            return
        if event.key in {"up"}:
            self.quit_armed = False
            self._refresh_controls()
            if isinstance(self.focused, Select) and bool(self.focused.expanded):
                self._move_open_select(self.focused, -1)
                event.stop()
                return
            self.action_focus_prev_field()
            event.stop()
            return
        if event.key in {"left"} and isinstance(self.focused, Button):
            self.quit_armed = False
            self._refresh_controls()
            self.action_focus_button_left()
            event.stop()
            return
        if event.key in {"right"} and isinstance(self.focused, Button):
            self.quit_armed = False
            self._refresh_controls()
            self.action_focus_button_right()
            event.stop()
            return

    # -- stage handlers ---------------------------------------------------
    def _enter_network_stage(self) -> None:
        """Network is now Stage 2. In workgroup mode it is the final step
        (Apply + Finish); with domain join it is followed by discovery (Next)."""
        btn = self.query_one("#next_network", Button)
        if self._select("domain_enabled") == "yes":
            btn.label = "Next"
            btn.variant = "primary"
            self.switch_stage("stage-network", "Stage 2/5: Deployer network (PXE/DHCP/DNS).")
        else:
            btn.label = "Apply + Finish"
            btn.variant = "success"
            self.switch_stage("stage-network", "Stage 2/5: Deployer network (workgroup mode).")

    @on(Button.Pressed, "#next_domain")
    def on_next_domain(self) -> None:
        self._enter_network_stage()

    @on(Button.Pressed, "#back_cred")
    def on_back_cred(self) -> None:
        self._enter_network_stage()

    @on(Button.Pressed, "#next_cred")
    def on_next_cred(self) -> None:
        try:
            user = self._input("join_user")
            password = self._input("join_pass")
            if not user or not password:
                raise RuntimeError("Both username and password are required.")
            ensure_vault_pass(self.vault_pass)
            write_vault(
                {"vault_domain_join_username": user, "vault_domain_join_password": password},
                self.vault_file,
                self.vault_pass,
            )
            self.append_log("Delegated join credential encrypted into the deployer vault.")
            # Derive a domain hint from a UPN suffix to prefill the DNS stage.
            if "@" in user:
                self.query_one("#domain_fqdn", Input).value = user.split("@", 1)[1]
            self.switch_stage("stage-dns", "Stage 4/5: Site DNS + AD discovery.")
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 3 failed: {exc}")

    @on(Button.Pressed, "#back_dns")
    def on_back_dns(self) -> None:
        self.switch_stage("stage-cred", "Stage 3/5: Delegated join credential.")

    @on(Button.Pressed, "#next_dns")
    def on_next_dns(self) -> None:
        # Validate inputs on the UI thread (fast), then run the network-bound
        # discovery in a worker thread so the TUI never freezes.
        try:
            domain_fqdn = self._input("domain_fqdn")
            dns_servers = [s.strip() for s in self._input("dns_servers").replace(",", " ").split() if s.strip()]
            if not domain_fqdn:
                raise RuntimeError("Domain FQDN is required.")
            if "\\" in domain_fqdn or "@" in domain_fqdn:
                raise RuntimeError(
                    f"'{domain_fqdn}' looks like a username, not a domain. Enter the "
                    "domain DNS name here (e.g. corp.example.com); the join account "
                    "was already entered in Stage 3."
                )
            if "." not in domain_fqdn or " " in domain_fqdn:
                raise RuntimeError(
                    f"'{domain_fqdn}' is not a valid domain FQDN. Use the dotted DNS "
                    "name, e.g. corp.example.com."
                )
            if not dns_servers:
                raise RuntimeError("At least one site DNS server IP is required.")
            for ip in dns_servers:
                ipaddress.ip_address(ip)
            vault = load_vault(self.vault_file, self.vault_pass)
            user = vault.get("vault_domain_join_username", "")
            password = vault.get("vault_domain_join_password", "")
            if not user or not password:
                raise RuntimeError("Join credential missing from vault; return to Stage 3.")
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 4 failed: {exc}")
            return

        self._set_busy("#next_dns", True, "Discovering...")
        self.set_status("Stage 4/5: Discovering AD services (working, please wait) ...")
        self.append_log(f"Confirming site DNS answers AD SRV for {domain_fqdn} ...")
        self._discover_worker(dns_servers, domain_fqdn, user, password)

    @work(thread=True, exclusive=True)
    def _discover_worker(self, dns_servers: list[str], domain_fqdn: str, user: str, password: str) -> None:
        try:
            ad_discovery.site_dns_answers_ad(dns_servers, domain_fqdn)
            self.call_from_thread(self.append_log, "Site DNS answers AD SRV. Binding to a DC and reading the directory ...")
            result = ad_discovery.full_preflight(dns_servers, domain_fqdn, user, password, ou_dn=None)
            result["dns_servers"] = dns_servers
            result["domain_fqdn"] = result.get("domain_fqdn") or domain_fqdn
        except Exception as exc:  # noqa: BLE001
            self.call_from_thread(self.append_log, f"[ERROR] Stage 4 failed: {exc}")
            self.call_from_thread(self._set_busy, "#next_dns", False, "Discover")
            self.call_from_thread(self.set_status, "Stage 4/5: Site DNS + AD discovery.")
            return
        self.call_from_thread(self._discovery_succeeded, result)

    def _discovery_succeeded(self, result: dict[str, Any]) -> None:
        self.discovery = result
        dcs = result.get("domain_controllers") or [result.get("bound_dc", "")]
        ous = result.get("organizational_units") or []
        self.query_one("#sel_dc", Select).set_options([(d, d) for d in dcs] or [("(none)", "")])
        self.query_one("#sel_ou", Select).set_options([(o, o) for o in ous] or [("(none discovered)", "")])
        if dcs:
            self.query_one("#sel_dc", Select).value = dcs[0]
        if ous:
            self.query_one("#sel_ou", Select).value = ous[0]
        self.append_log(
            f"Discovered domain={result.get('domain_fqdn')} netbios={result.get('domain_netbios')} "
            f"DCs={len(dcs)} OUs={len(ous)}."
        )
        # If the user left the upstream/general DNS blank in Stage 2, default it
        # to the site DNS (a real resolver) rather than forcing a guess earlier.
        net_dns = self.query_one("#net_dns", Input)
        site_dns = result.get("dns_servers", [])
        if not net_dns.value.strip() and site_dns:
            net_dns.value = site_dns[0]
            self.append_log(f"Upstream/general DNS defaulted to site DNS {site_dns[0]}.")
        self._set_busy("#next_dns", False, "Discover")
        self.switch_stage("stage-confirm", "Stage 5/5: Confirm domain + verify OU rights.")

    def _set_busy(self, button_id: str, busy: bool, label: str) -> None:
        """Toggle a stage's primary button into a disabled 'working' state and
        back, so long-running steps show progress and can't be re-triggered."""
        btn = self.query_one(button_id, Button)
        btn.disabled = busy
        btn.label = label

    @on(Button.Pressed, "#back_confirm")
    def on_back_confirm(self) -> None:
        self.switch_stage("stage-dns", "Stage 4/5: Site DNS + AD discovery.")

    @on(Button.Pressed, "#next_confirm")
    def on_next_confirm(self) -> None:
        # Validate selections + the upstream DNS on the UI thread, then do the
        # LDAP verify + service apply in a worker so the UI stays responsive.
        try:
            dc = self._select("sel_dc")
            ou = self._select("sel_ou")
            if not dc or not ou:
                raise RuntimeError("Select both a domain controller and a target OU.")
            upstream = self._require_upstream_dns()
            dns_servers = self.discovery["dns_servers"]
            domain_fqdn = self.discovery["domain_fqdn"]
            vault = load_vault(self.vault_file, self.vault_pass)
            user = vault["vault_domain_join_username"]
            password = vault["vault_domain_join_password"]
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 5 failed: {exc}")
            return

        self._set_busy("#next_confirm", True, "Finishing...")
        self.set_status("Stage 5/5: Verifying rights and applying services (working) ...")
        self._confirm_worker(dc, ou, dns_servers, domain_fqdn, user, password, upstream)

    @work(thread=True, exclusive=True)
    def _confirm_worker(
        self, dc: str, ou: str, dns_servers: list[str], domain_fqdn: str,
        user: str, password: str, upstream: str,
    ) -> None:
        try:
            self.append_log(f"Verifying create-computer rights on {ou} ...")
            conn = ad_discovery.ldap_bind(dc, user, password, dns_servers=dns_servers)
            try:
                ad_discovery.check_ou_create_rights(conn, ou)
            finally:
                try:
                    conn.unbind()
                except Exception:  # noqa: BLE001
                    pass
            self.append_log("OU create-computer rights confirmed.")

            try:
                dc_ip = ad_discovery.resolve_host(dns_servers, dc)
            except ad_discovery.DiscoveryError:
                dc_ip = self.discovery.get("domain_controller_ip", "")

            self._write_site_config(
                enabled=True,
                domain_fqdn=domain_fqdn,
                netbios=self.discovery.get("domain_netbios", ""),
                ou_path=ou,
                domain_controller=dc,
                domain_controller_ip=dc_ip,
                dns_servers=dns_servers,
            )
            self._render_join_credential(user, password)
            self.append_log("Wrote domain.json/naming.json and rendered the [join] credential.")
            # Network inputs were captured back in Stage 2; render the PXE/DHCP/DNS
            # service now that the discovered domain + site DNS are known.
            self._apply_services(domain_enabled=True, upstream=upstream)
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 5 failed: {exc}")
            self.call_from_thread(self._set_busy, "#next_confirm", False, "Verify + Finish")
            self.call_from_thread(self.set_status, "Stage 5/5: Confirm domain + verify OU rights.")
            return
        self.call_from_thread(self._finish_setup_ui)

    # -- network capture + service application -----------------------------
    def _collect_network(self) -> dict[str, Any]:
        # Upstream/general DNS is finalized + liveness-checked later in
        # _apply_services (it may be backfilled from the site DNS after
        # discovery), so it is allowed to be blank at this point.
        ip = self._input("net_ip")
        prefix = int(self._input("net_prefix"))
        gateway = self._input("net_gateway")
        dhcp_start = self._input("net_dhcp_start")
        dhcp_end = self._input("net_dhcp_end")
        for label, value in [("IP", ip), ("gateway", gateway), ("DHCP start", dhcp_start), ("DHCP end", dhcp_end)]:
            try:
                ipaddress.ip_address(value)
            except ValueError as exc:
                raise RuntimeError(f"{label} '{value}' is not a valid IP address.") from exc
        network = ipaddress.ip_network(f"{ip}/{prefix}", strict=False)
        if ipaddress.ip_address(gateway) not in network:
            raise RuntimeError(f"Gateway {gateway} is outside {network}.")
        return {
            "ip": ip, "prefix": prefix, "gateway": gateway,
            "dhcp_start": dhcp_start, "dhcp_end": dhcp_end,
            "upstream_dns": self._input("net_dns"),
        }

    def _require_upstream_dns(self) -> str:
        """Validate the upstream/general DNS field (UI thread) and return it."""
        upstream = self._input("net_dns")
        if not upstream:
            raise RuntimeError("Upstream/general DNS is required (an IP that answers DNS).")
        try:
            ipaddress.ip_address(upstream)
        except ValueError as exc:
            raise RuntimeError(f"Upstream/general DNS '{upstream}' is not a valid IP address.") from exc
        return upstream

    def _apply_services(self, domain_enabled: bool, upstream: str) -> None:
        # Runs in a worker thread. Verify the upstream DNS (TCP/53 - not ICMP
        # ping, not a recursive query - proves a DNS service is listening), then
        # render dnsmasq and restart services. UI updates go via thread-safe
        # append_log/set_status; the final stage switch is marshalled by callers.
        self.net["upstream_dns"] = upstream
        self.append_log(f"Verifying upstream DNS {upstream} answers on port 53 ...")
        ad_discovery.dns_server_responds(upstream)
        self.append_log(f"Upstream DNS {upstream} is responding.")

        net = self.net
        site_dns = self.discovery.get("dns_servers", []) if domain_enabled else []
        self._render_dnsmasq(
            net["ip"], net["prefix"], net["gateway"],
            net["dhcp_start"], net["dhcp_end"], net["upstream_dns"],
            domain_enabled, site_dns,
        )
        self._restart_services()
        self.append_log("dnsmasq re-rendered; nginx/dnsmasq/smbd restarted.")
        self._final_checks(net["ip"], domain_enabled)

    def _finish_setup_ui(self) -> None:
        self.set_status("Setup complete.")
        self.query_one("#done_summary", Static).update(self._done_summary_text())
        self.switch_stage("stage-done", "Setup complete. Press q to quit.")

    def _done_summary_text(self) -> str:
        """Operator next-steps shown on the final screen: where the deployer is
        listening, what clients will get, a browser self-test, and how to PXE
        boot the workstations."""
        net = self.net or {}
        ip = net.get("ip", "?")
        dhcp_start = net.get("dhcp_start", "?")
        dhcp_end = net.get("dhcp_end", "?")
        return (
            "\n"
            f"Deployer IP        : {ip}\n"
            f"DHCP range         : {dhcp_start} - {dhcp_end}  (workstations lease an address from here)\n"
            f"HTTP self-test     : http://{ip}/ipxe/boot.ipxe\n"
            "                     Open that URL in a browser - it should return the iPXE boot script.\n"
            "                     If it downloads/displays text, HTTP hosting is working.\n"
            "\n"
            "Next step - PXE boot your workstations:\n"
            "  1. Put each workstation on this same offline network/VLAN as the deployer.\n"
            "  2. In firmware (UEFI), enable network/PXE boot over IPv4 and set it first in the boot order.\n"
            "  3. Power them on. They will DHCP from this deployer, chainload iPXE over HTTP,\n"
            "     and begin the Windows deployment automatically - no per-machine input needed.\n"
            "\n"
            "Press q to quit."
        )

    @on(Button.Pressed, "#back_network")
    def on_back_network(self) -> None:
        self.switch_stage("stage-domain", "Stage 1/5: Enable domain join?")

    @on(Button.Pressed, "#next_network")
    def on_next_network(self) -> None:
        try:
            self.net = self._collect_network()
            domain_enabled = self._select("domain_enabled") == "yes"
            if domain_enabled:
                self.append_log("Network settings captured; continuing to domain join.")
                self.switch_stage("stage-cred", "Stage 3/5: Delegated join credential.")
                return
            # Workgroup mode: this is the final step, so apply services now.
            upstream = self._require_upstream_dns()
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 2 failed: {exc}")
            return

        self._set_busy("#next_network", True, "Applying...")
        self.set_status("Stage 2/5: Applying deployer services (working) ...")
        self._workgroup_finish_worker(upstream)

    @work(thread=True, exclusive=True)
    def _workgroup_finish_worker(self, upstream: str) -> None:
        try:
            self._write_site_config(enabled=False)
            self.append_log("Wrote domain.json (enabled: false). No join credential rendered.")
            self._apply_services(domain_enabled=False, upstream=upstream)
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 2 failed: {exc}")
            self.call_from_thread(self._set_busy, "#next_network", False, "Apply + Finish")
            self.call_from_thread(self.set_status, "Stage 2/5: Deployer network (workgroup mode).")
            return
        self.call_from_thread(self._finish_setup_ui)

    # -- side effects -----------------------------------------------------
    def _write_site_config(
        self,
        enabled: bool,
        domain_fqdn: str = "",
        netbios: str = "",
        ou_path: str = "",
        domain_controller: str = "",
        domain_controller_ip: str = "",
        dns_servers: list[str] | None = None,
    ) -> None:
        self.site_path.mkdir(parents=True, exist_ok=True)
        domain = {
            "enabled": enabled,
            "domain_fqdn": domain_fqdn,
            "domain_netbios": netbios,
            "ou_path": ou_path,
            "domain_controller": domain_controller,
            "domain_controller_ip": domain_controller_ip,
            "dns_servers": dns_servers or [],
        }
        (self.site_path / "domain.json").write_text(json.dumps(domain, indent=2) + "\n", encoding="utf-8")
        naming = {"source": "service_tag", "max_length": 15}
        (self.site_path / "naming.json").write_text(json.dumps(naming, indent=2) + "\n", encoding="utf-8")

    def _render_join_credential(self, user: str, password: str) -> None:
        self.join_path.mkdir(parents=True, exist_ok=True)
        os.chmod(self.join_path, 0o700)
        cred = {"username": user, "password": password}
        cred_file = self.join_path / "join.cred"
        cred_file.write_text(json.dumps(cred) + "\n", encoding="utf-8")
        os.chmod(cred_file, 0o600)

    def _render_dnsmasq(
        self,
        ip: str,
        prefix: int,
        gateway: str,
        dhcp_start: str,
        dhcp_end: str,
        upstream_dns: str,
        domain_enabled: bool,
        site_dns: list[str],
    ) -> None:
        netmask = str(ipaddress.ip_network(f"{ip}/{prefix}", strict=False).netmask)
        lines = [
            "interface=eth0",
            "bind-interfaces",
            "",
            "no-resolv",
            f"address=/{self.offline_hostname}/{ip}",
            f"address=/{self.offline_hostname_fqdn}/{ip}",
            f"server={upstream_dns}",
        ]
        domain_fqdn = self.discovery.get("domain_fqdn", "")
        if domain_enabled and domain_fqdn:
            for dns_ip in site_dns:
                lines.append(f"server=/{domain_fqdn}/{dns_ip}")
        lines += [
            "",
            f"dhcp-range={dhcp_start},{dhcp_end},{netmask},12h",
            f"dhcp-option=6,{ip}",
            "",
            "enable-tftp",
            "tftp-root=/srv/tftp",
            "",
            "dhcp-match=set:bios,option:client-arch,0",
            "dhcp-match=set:efi-x86_64,option:client-arch,7",
            "dhcp-match=set:efi-x86_64,option:client-arch,9",
            "dhcp-userclass=set:ipxe,iPXE",
            "",
            f"dhcp-boot=tag:ipxe,http://{self.offline_hostname}/ipxe/autoexec.ipxe",
            "dhcp-boot=tag:!ipxe,tag:bios,undionly.kpxe",
            "dhcp-boot=tag:!ipxe,tag:efi-x86_64,ipxeboot/x86_64-sb/shimx64.efi",
            "",
        ]
        Path("/etc/dnsmasq.d/deploy-pxe.conf").write_text("\n".join(lines), encoding="utf-8")

    def _restart_services(self) -> None:
        for svc in ("dnsmasq", "smbd", "nginx"):
            proc = subprocess.run(["systemctl", "restart", svc], capture_output=True, text=True, check=False)
            if proc.returncode != 0:
                raise RuntimeError(f"Failed to restart {svc}: {proc.stderr.strip()}")

    def _final_checks(self, ip: str, domain_enabled: bool) -> None:
        proc = subprocess.run(["getent", "hosts", self.offline_hostname], capture_output=True, text=True, check=False)
        if proc.returncode == 0 and ip in proc.stdout:
            self.append_log(f"getent hosts {self.offline_hostname} -> {proc.stdout.strip()}")
        else:
            self.append_log(f"[WARN] {self.offline_hostname} did not resolve to {ip} via the local resolver yet.")

        # Stale-IP scan across shipped artifacts.
        stale = self._scan_stale_ip(ip)
        if stale:
            self.append_log(f"[WARN] Possible stale IP references found in: {', '.join(stale)}")

        if domain_enabled:
            dc = self.discovery.get("domain_controller", "")
            dns_servers = self.discovery.get("dns_servers", [])
            if dc and dns_servers:
                try:
                    dc_ip = ad_discovery.resolve_host(dns_servers, dc)
                    self.append_log(f"DC {dc} resolves through the deployer path -> {dc_ip}.")
                except ad_discovery.DiscoveryError as exc:
                    self.append_log(f"[WARN] DC resolution check failed: {exc}")

    def _scan_stale_ip(self, current_ip: str) -> list[str]:
        candidates = [
            "/srv/deploy/ipxe/autoexec.ipxe",
            "/srv/deploy/ipxe/boot.ipxe",
            "/etc/dnsmasq.d/deploy-pxe.conf",
        ]
        flagged: list[str] = []
        import re

        ip_re = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")
        for path_str in candidates:
            p = Path(path_str)
            if not p.exists():
                continue
            text = p.read_text(encoding="utf-8", errors="ignore")
            for found in ip_re.findall(text):
                if found != current_ip and not found.startswith("0.") and found not in ("255.255.255.0",):
                    flagged.append(f"{p.name}:{found}")
        return flagged


def main() -> int:
    OfflineSetupApp().run()
    return 0


if __name__ == "__main__":
    sys.exit(main())
