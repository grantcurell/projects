#!/usr/bin/env python3
"""Interactive Textual wizard that builds a validated config.yaml for Configure-WindowsServer.ps1.

Only the handful of values that are genuinely environment-specific are prompted. Everything
else (execution paths, functional levels, NTDS paths, DNS forwarders, time, DHCP scope,
Proxmox checks, optional features, service accounts) is inherited from the chosen baseline,
and the values that depend on the core inputs (NetBIOS, client DNS, reverse zone, DHCP
server identity) are derived automatically.
"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import ipaddress
import re
import shutil
import subprocess
import sys
from typing import Any

import yaml
from textual import events, on, work
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import (
    Button,
    ContentSwitcher,
    Footer,
    Input as TextInput,
    Log,
    ProgressBar,
    Select,
    Static,
)


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE_PATH = ROOT / "config.example.yaml"
OUTPUT_PATH = ROOT / "config.yaml"

STAGE_ORDER = [
    "stage-baseline",
    "stage-core",
    "stage-write",
    "stage-done",
]

STAGE_LABELS = {
    "stage-baseline": "Stage 1/4: Choose configuration baseline.",
    "stage-core": "Stage 2/4: Core settings for this server.",
    "stage-write": "Stage 3/4: Write config.yaml and validate.",
    "stage-done": "Stage 4/4: Setup complete.",
}

FIELD_DIVIDER = "─" * 48


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"Invalid YAML object in {path}")
    return data


def dump_yaml(path: Path, data: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False, default_flow_style=False), encoding="utf-8")


def get_in(obj: dict[str, Any], path: list[str]) -> Any:
    cur: Any = obj
    for key in path:
        if not isinstance(cur, dict) or key not in cur:
            return None
        cur = cur[key]
    return cur


def set_in(obj: dict[str, Any], path: list[str], value: Any) -> None:
    cur: dict[str, Any] = obj
    for key in path[:-1]:
        if key not in cur or not isinstance(cur[key], dict):
            cur[key] = {}
        cur = cur[key]
    cur[path[-1]] = value


def backup_file(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = path.with_suffix(path.suffix + f".bak.{stamp}")
    shutil.copy2(path, backup)
    return backup


def ipv4_in_subnet(address: str, network_id: str, prefix_length: int) -> bool:
    network = ipaddress.IPv4Network(f"{network_id}/{prefix_length}", strict=False)
    return ipaddress.IPv4Address(address) in network


def must_ipv4(value: str, label: str) -> None:
    try:
        ipaddress.IPv4Address(value.strip())
    except ValueError as exc:
        raise RuntimeError(f"{label} is not a valid IPv4 address: {value}") from exc


class PersistentSelect(Select):
    def on_focus(self) -> None:
        self.expanded = False

    def _cycle_option(self, direction: int) -> None:
        options = [opt for _, opt in self._options if opt is not Select.NULL]
        if not options:
            return
        try:
            idx = options.index(self.value)
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
    def on_key(self, event: events.Key) -> None:
        app = self.app
        if event.key == "q" and hasattr(app, "quit_armed") and bool(getattr(app, "quit_armed")):
            app.exit()
            event.stop()
            return
        if event.key == "escape" and not self.selection.is_empty:
            self.cursor_position = self.cursor_position
            event.stop()
            event.prevent_default()
            return


def labeled_field(title: str, description: str, widget: Any):
    """Title, divider, help text, then the input widget."""
    yield Static(title, classes="field-title")
    yield Static(FIELD_DIVIDER, classes="field-divider")
    yield Static(description, classes="field-help")
    yield widget


class IdentityConfigWizard(App[None]):
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
    #stage-write, #stage-done {
        align: center middle;
    }
    .write-center {
        width: 1fr;
        height: 1fr;
        align: center middle;
    }
    #write_now {
        width: 36;
        height: 5;
        border: round #22c55e;
        background: #14532d;
        color: #ffffff;
        text-style: bold;
    }
    .field {
        margin-bottom: 1;
    }
    .field-title {
        text-style: bold;
        margin-top: 1;
    }
    .field-divider {
        color: $text-muted;
        height: 1;
    }
    .field-help {
        color: $text-muted;
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

    def __init__(self) -> None:
        super().__init__()
        if not EXAMPLE_PATH.exists():
            raise RuntimeError(f"Missing template: {EXAMPLE_PATH}")
        self.cfg = load_yaml(EXAMPLE_PATH)
        self.baseline_path = EXAMPLE_PATH
        self.current_stage = "stage-baseline"
        self.quit_armed = False
        self.write_succeeded = False

    def compose(self) -> ComposeResult:
        yield Static(STAGE_LABELS["stage-baseline"], id="status")
        yield Static(
            "Controls: Tab/Shift+Tab move fields, arrows navigate fields/options, Enter opens/selects dropdown options, q = Quit.",
            id="help",
        )
        yield Static("", id="control_legend")
        yield ProgressBar(total=len(STAGE_ORDER), show_eta=False, show_percentage=True, id="stage_progress")
        with ContentSwitcher(initial="stage-baseline", id="main-switcher"):
            with VerticalScroll(id="stage-baseline", classes="stage"):
                yield Static("Choose where to start. Existing config.yaml is offered only when present.")
                yield Static("Baseline source")
                baseline_options: list[tuple[str, str]] = [("config.example.yaml (recommended for new builds)", "example")]
                if OUTPUT_PATH.exists():
                    baseline_options.insert(0, ("Existing config.yaml (edit current file)", "existing"))
                yield PersistentSelect(options=baseline_options, value=baseline_options[0][1], id="baseline_source", classes="field")
                with Horizontal(classes="stage-nav"):
                    yield Button("Next", id="next_baseline", variant="primary", classes="nav-button")

            with VerticalScroll(id="stage-core", classes="stage"):
                net = self.cfg.get("network", {})
                ipv4 = net.get("ipv4", {})
                ad = self.cfg.get("activeDirectory", {})
                yield Static(
                    "The only values that are specific to this server. Everything else (paths, "
                    "functional levels, DNS forwarders, time, DHCP scope, Proxmox checks, and "
                    "optional features) uses the tested defaults from the baseline you picked."
                )
                yield from labeled_field(
                    "Computer name (hostname)",
                    "Windows hostname for this domain controller. 1-15 characters; letters, digits, hyphens.",
                    Input(str(net.get("computerName") or ""), id="net_hostname", classes="field"),
                )
                yield from labeled_field(
                    "Static IPv4 address",
                    "The fixed IP this server owns. Also used as its DNS server IP and DHCP server IP.",
                    Input(str(ipv4.get("address") or ""), id="net_ip", classes="field"),
                )
                yield from labeled_field(
                    "IPv4 prefix length",
                    "Subnet size in CIDR bits (e.g. 24 = 255.255.255.0).",
                    Input(str(ipv4.get("prefixLength") or ""), id="net_prefix", classes="field"),
                )
                yield from labeled_field(
                    "Default gateway",
                    "Router address for this subnet. Must be inside the server's subnet.",
                    Input(str(ipv4.get("defaultGateway") or ""), id="net_gw", classes="field"),
                )
                yield from labeled_field(
                    "AD domain FQDN",
                    "New forest root domain, e.g. corp.example.com. NetBIOS name is derived from the first label.",
                    Input(str(ad.get("domainName") or ""), id="ad_domain", classes="field"),
                )
                with Horizontal(classes="stage-nav"):
                    yield Button("Back", id="back_core", classes="nav-button")
                    yield Button("Next", id="next_core", variant="primary", classes="nav-button")

            with Vertical(id="stage-write", classes="stage"):
                with Horizontal(classes="write-center"):
                    yield Button("Back", id="back_write", classes="nav-button")
                    yield Button("WRITE CONFIG\n[dim](press enter)[/dim]", id="write_now")

            with VerticalScroll(id="stage-done", classes="stage"):
                yield Static("Configuration complete. config.yaml is ready.", id="done_title")
                yield Static("", id="done_summary")

        yield Log(id="log", highlight=True, auto_scroll=True)
        yield Footer()

    def on_mount(self) -> None:
        self.append_log("Wizard started. Complete each stage; Next validates before advancing.")
        self._refresh_controls()
        self._update_progress()
        self.set_focus(self.query_one("#baseline_source", PersistentSelect))

    def append_log(self, message: str) -> None:
        self.query_one("#log", Log).write_line(message)

    def set_status(self, message: str) -> None:
        self.query_one("#status", Static).update(message)

    def _input(self, widget_id: str) -> str:
        return self.query_one(f"#{widget_id}", Input).value.strip()

    def _select(self, widget_id: str) -> str:
        value = self.query_one(f"#{widget_id}", Select).value
        return "" if value is None else str(value)

    def switch_stage(self, stage_id: str) -> None:
        self.query_one("#main-switcher", ContentSwitcher).current = stage_id
        self.current_stage = stage_id
        self.set_status(STAGE_LABELS[stage_id])
        self._refresh_controls()
        self._update_progress()
        focusables = self._stage_focusables()
        if stage_id == "stage-write":
            self.set_focus(self.query_one("#write_now", Button))
        elif focusables:
            self.set_focus(focusables[0])
            if isinstance(focusables[0], Select):
                focusables[0].expanded = False

    def _update_progress(self) -> None:
        idx = STAGE_ORDER.index(self.current_stage) + 1
        self.query_one("#stage_progress", ProgressBar).update(progress=idx)

    def _refresh_controls(self) -> None:
        armed_suffix = " | Quit: Esc then q" if not self.quit_armed else " | Quit armed: press q now"
        if self.current_stage == "stage-done":
            legend = f"Setup complete. Press q to exit.{armed_suffix}"
        elif self.current_stage == "stage-write":
            legend = f"Now: highlight WRITE CONFIG and press Enter to write config.yaml and run validation.{armed_suffix}"
        else:
            legend = f"Fill fields, then highlight Next and press Enter to validate this stage.{armed_suffix}"
        self.query_one("#control_legend", Static).update(legend)

    def _ensure_focus_visible_target(self) -> None:
        fields = self._stage_focusables()
        if not fields:
            return
        owner = self._resolve_focus_owner(self.focused, fields)
        if owner is None:
            self.set_focus(fields[0])

    def _stage_focusables(self) -> list[Input | Select | Button]:
        stage = self.query_one(f"#{self.current_stage}")
        widgets: list[Input | Select | Button] = []
        for widget in stage.query("Input, Select, Button"):
            if isinstance(widget, (Input, Select, Button)) and not widget.disabled:
                widgets.append(widget)
        return widgets

    def _stage_buttons(self) -> list[Button]:
        stage = self.query_one(f"#{self.current_stage}")
        return [w for w in stage.query("Button") if isinstance(w, Button) and not w.disabled]

    def _resolve_focus_owner(self, focused: object, fields: list[Input | Select | Button]) -> Input | Select | Button | None:
        if focused in fields:
            return focused  # type: ignore[return-value]
        node = focused
        while node is not None and hasattr(node, "parent"):
            node = getattr(node, "parent")
            if node in fields:
                return node  # type: ignore[return-value]
        return None

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

    def action_focus_button_left(self) -> None:
        buttons = self._stage_buttons()
        if len(buttons) < 2:
            return
        if self.focused in buttons:
            idx = buttons.index(self.focused)
            self.set_focus(buttons[(idx - 1) % len(buttons)])

    def action_focus_button_right(self) -> None:
        buttons = self._stage_buttons()
        if len(buttons) < 2:
            return
        if self.focused in buttons:
            idx = buttons.index(self.focused)
            self.set_focus(buttons[(idx + 1) % len(buttons)])

    def _move_open_select(self, select: Select, direction: int) -> None:
        options = [opt for _, opt in select._options if opt is not Select.NULL]
        if not options:
            return
        try:
            idx = options.index(select.value)
        except ValueError:
            idx = 0
        select.value = options[(idx + direction) % len(options)]
        select.action_show_overlay()

    def _require_text(self, value: str, label: str) -> None:
        if not value.strip():
            raise RuntimeError(f"{label} is required.")

    def _validate_gateway_in_subnet(self, gateway: str, address: str, prefix: int) -> None:
        if not ipv4_in_subnet(gateway, address, prefix):
            network = ipaddress.IPv4Network(f"{address}/{prefix}", strict=False)
            raise RuntimeError(f"Default gateway must be inside the server subnet ({network}).")

    def _validate_hostname(self, value: str) -> None:
        if len(value) < 1 or len(value) > 15:
            raise RuntimeError("Hostname must be 1-15 characters.")
        if not re.match(r"^[A-Za-z0-9-]+$", value):
            raise RuntimeError("Hostname may contain only letters, digits, and hyphens.")

    def _validate_domain(self, value: str) -> None:
        ad = self.cfg.get("activeDirectory", {})
        if "." not in value and not bool(ad.get("allowSingleLabelDomain")):
            raise RuntimeError("Single-label domains are not allowed. Use a dotted FQDN (e.g. corp.example.com).")
        if value.lower().endswith(".local") and not bool(ad.get("allowDotLocal")):
            raise RuntimeError(".local domains are discouraged and not allowed by this config.")

    def _derive_netbios(self, domain: str) -> str:
        first_label = domain.split(".")[0]
        cleaned = re.sub(r"[^A-Za-z0-9-]", "", first_label).upper()
        netbios = cleaned[:15]
        if not netbios:
            raise RuntimeError("Could not derive a NetBIOS name from the domain FQDN.")
        return netbios

    def validate_baseline_stage(self) -> None:
        try:
            source = self._select("baseline_source")
            if source == "existing":
                if not OUTPUT_PATH.exists():
                    raise RuntimeError("config.yaml was selected but the file does not exist.")
                self.baseline_path = OUTPUT_PATH
            else:
                self.baseline_path = EXAMPLE_PATH
            self.cfg = load_yaml(self.baseline_path)
            self.cfg.pop("environment", None)
            self.append_log(f"Loaded baseline from {self.baseline_path.name}.")
            self._reseed_core_fields()
            self.switch_stage("stage-core")
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 1 failed: {exc}")
            self.set_status("Stage 1 failed. Fix selection and try again.")

    def _reseed_core_fields(self) -> None:
        """Repopulate the core inputs from the freshly loaded baseline."""
        net = self.cfg.get("network", {})
        ipv4 = net.get("ipv4", {})
        ad = self.cfg.get("activeDirectory", {})
        self.query_one("#net_hostname", Input).value = str(net.get("computerName") or "")
        self.query_one("#net_ip", Input).value = str(ipv4.get("address") or "")
        self.query_one("#net_prefix", Input).value = str(ipv4.get("prefixLength") or "")
        self.query_one("#net_gw", Input).value = str(ipv4.get("defaultGateway") or "")
        self.query_one("#ad_domain", Input).value = str(ad.get("domainName") or "")

    def validate_core_stage(self) -> None:
        try:
            hostname = self._input("net_hostname")
            ip = self._input("net_ip")
            prefix_raw = self._input("net_prefix")
            gw = self._input("net_gw")
            domain = self._input("ad_domain")

            self._validate_hostname(hostname)
            must_ipv4(ip, "Static IPv4 address")
            must_ipv4(gw, "Default gateway")
            try:
                prefix = int(prefix_raw)
            except ValueError as exc:
                raise RuntimeError("IPv4 prefix length must be a whole number between 1 and 32.") from exc
            if prefix < 1 or prefix > 32:
                raise RuntimeError("IPv4 prefix length must be between 1 and 32.")
            self._validate_gateway_in_subnet(gw, ip, prefix)
            self._validate_domain(domain)

            forwarders = [str(f) for f in (get_in(self.cfg, ["dns", "forwarders"]) or [])]
            allow_self = bool(get_in(self.cfg, ["dns", "allowForwardersPointingToSelf"]))
            if not allow_self and ip in forwarders:
                raise RuntimeError(
                    f"The baseline's DNS forwarders include this server's IP ({ip}). "
                    "Pick a different static IP or edit the baseline's dns.forwarders."
                )

            netbios = self._derive_netbios(domain)

            # Core network identity (entered).
            set_in(self.cfg, ["network", "enabled"], True)
            set_in(self.cfg, ["network", "computerName"], hostname)
            set_in(self.cfg, ["network", "ipv4", "address"], ip)
            set_in(self.cfg, ["network", "ipv4", "prefixLength"], prefix)
            set_in(self.cfg, ["network", "ipv4", "defaultGateway"], gw)
            # Derived: a DC resolves against itself before promotion, loopback after.
            set_in(self.cfg, ["network", "ipv4", "dnsClientServersBeforePromotion"], [ip])
            set_in(self.cfg, ["network", "ipv4", "dnsClientServersAfterPromotion"], ["127.0.0.1"])

            # Active Directory (entered + derived NetBIOS).
            set_in(self.cfg, ["activeDirectory", "enabled"], True)
            set_in(self.cfg, ["activeDirectory", "domainName"], domain)
            set_in(self.cfg, ["activeDirectory", "netbiosName"], netbios)

            # Derived DNS: reverse zone for the server's /24 and the records to validate.
            set_in(self.cfg, ["dns", "enabled"], True)
            rev_net = re.sub(r"\.\d+$", ".0", ip) + "/24"
            set_in(self.cfg, ["dns", "reverseLookupZones"], [{"networkId": rev_net, "replicationScope": "Forest"}])
            set_in(
                self.cfg,
                ["dns", "requiredRecordsToValidate"],
                [
                    {"name": domain, "type": "A"},
                    {"name": f"_ldap._tcp.dc._msdcs.{domain}", "type": "SRV"},
                ],
            )

            # Derived DHCP server identity (scope itself is inherited from the baseline).
            set_in(self.cfg, ["dhcp", "serverDnsName"], f"{hostname.lower()}.{domain.lower()}")
            set_in(self.cfg, ["dhcp", "serverIpAddress"], ip)

            self.append_log(f"Core settings validated. NetBIOS derived as '{netbios}'.")
            self.switch_stage("stage-write")
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 2 failed: {exc}")
            self.set_status("Stage 2 failed. Fix fields and try again.")

    def _run_powershell_validation(self, config_path: Path) -> str:
        ps_script = f"""
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
. '{ROOT / "lib" / "Config.ps1"}'
$loaded = Import-ProjectConfig -ConfigPath '{config_path}'
Assert-ProjectConfig -Config $loaded
Write-Output 'VALIDATION_OK'
""".strip()
        last_error = "PowerShell is not available; config.yaml was written but not validated."
        for exe in ("pwsh", "powershell"):
            proc = subprocess.run(
                [exe, "-NoProfile", "-Command", ps_script],
                cwd=str(ROOT),
                text=True,
                capture_output=True,
                check=False,
            )
            if proc.returncode == 0 and "VALIDATION_OK" in proc.stdout:
                return exe
            if proc.returncode != 0:
                last_error = (proc.stderr or proc.stdout).strip() or "PowerShell validation failed."
        raise RuntimeError(last_error)

    @work(thread=True)
    def _validate_written_config(self) -> None:
        try:
            exe = self._run_powershell_validation(OUTPUT_PATH)
            self.call_from_thread(self._on_write_validation_success, exe)
        except RuntimeError as exc:
            self.call_from_thread(self._on_write_validation_failure, str(exc))

    def _on_write_validation_success(self, exe: str) -> None:
        self.write_succeeded = True
        self.query_one("#write_now", Button).disabled = False
        self.append_log(f"Validation PASSED via {exe}. config.yaml is ready.")
        domain = str(get_in(self.cfg, ["activeDirectory", "domainName"]) or "")
        hostname = str(get_in(self.cfg, ["network", "computerName"]) or "")
        dc_ip = str(get_in(self.cfg, ["network", "ipv4", "address"]) or "")
        netbios = str(get_in(self.cfg, ["activeDirectory", "netbiosName"]) or "")
        summary = (
            f"Domain: {domain}  (NetBIOS {netbios})\n"
            f"DC hostname: {hostname}\n"
            f"Static IP: {dc_ip}\n"
            f"Config file: {OUTPUT_PATH}\n\n"
            "Next on the Windows Server (elevated PowerShell):\n"
            f"  .\\Configure-WindowsServer.ps1 -ConfigPath .\\config.yaml -PlanOnly\n"
            f"  .\\Configure-WindowsServer.ps1 -ConfigPath .\\config.yaml"
        )
        self.query_one("#done_summary", Static).update(summary)
        self.switch_stage("stage-done")

    def _on_write_validation_failure(self, message: str) -> None:
        self.query_one("#write_now", Button).disabled = False
        self.append_log(f"[WARN] {message}")
        self.set_status("config.yaml written; fix validation errors before running the server script.")

    def write_config(self) -> None:
        try:
            write_btn = self.query_one("#write_now", Button)
            if write_btn.disabled:
                return
            write_btn.disabled = True
            if OUTPUT_PATH.exists():
                backup = backup_file(OUTPUT_PATH)
                self.append_log(f"Backed up existing config.yaml to {backup.name}.")
            dump_yaml(OUTPUT_PATH, self.cfg)
            self.append_log(f"Wrote {OUTPUT_PATH.name}. Running PowerShell validation...")
            self.set_status("Validating config.yaml (this may take a moment)...")
            self._validate_written_config()
        except Exception as exc:  # noqa: BLE001
            self.query_one("#write_now", Button).disabled = False
            self.append_log(f"[ERROR] Write failed: {exc}")
            self.set_status("Write failed. Review the log and try again.")

    @on(Button.Pressed, "#next_baseline")
    def on_next_baseline(self) -> None:
        self.validate_baseline_stage()

    @on(Button.Pressed, "#back_core")
    def on_back_core(self) -> None:
        self.switch_stage("stage-baseline")

    @on(Button.Pressed, "#next_core")
    def on_next_core(self) -> None:
        self.validate_core_stage()

    @on(Button.Pressed, "#back_write")
    def on_back_write(self) -> None:
        self.switch_stage("stage-core")

    @on(Button.Pressed, "#write_now")
    def on_write_now(self) -> None:
        self.write_config()

    def on_key(self, event: events.Key) -> None:
        if event.key == "escape":
            if isinstance(self.focused, Select) and bool(self.focused.expanded):
                return
            self.quit_armed = True
            self._refresh_controls()
            self.append_log("Quit armed. Press q to quit.")
            event.stop()
            return
        if event.key == "q" and self.quit_armed:
            self.exit()
            event.stop()
            return
        if event.key == "down":
            self.quit_armed = False
            self._refresh_controls()
            if isinstance(self.focused, Select) and bool(self.focused.expanded):
                self._move_open_select(self.focused, 1)
                event.stop()
                return
            self.action_focus_next_field()
            event.stop()
            return
        if event.key == "up":
            self.quit_armed = False
            self._refresh_controls()
            if isinstance(self.focused, Select) and bool(self.focused.expanded):
                self._move_open_select(self.focused, -1)
                event.stop()
                return
            self.action_focus_prev_field()
            event.stop()
            return
        if event.key == "left" and isinstance(self.focused, Button):
            self.quit_armed = False
            self._refresh_controls()
            self.action_focus_button_left()
            event.stop()
            return
        if event.key == "right" and isinstance(self.focused, Button):
            self.quit_armed = False
            self._refresh_controls()
            self.action_focus_button_right()
            event.stop()
            return


def main() -> int:
    try:
        IdentityConfigWizard().run()
    except KeyboardInterrupt:
        return 130
    except Exception as exc:  # noqa: BLE001
        print(f"Fatal: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
