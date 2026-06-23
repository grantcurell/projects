#!/usr/bin/env python3
"""Interactive Textual wizard that builds a validated config.yaml for Configure-WindowsServer.ps1."""
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
from textual import events, on
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

SUPPORTED_MASKS: dict[str, int] = {
    "255.255.255.0": 24,
    "255.255.0.0": 16,
    "255.0.0.0": 8,
    "255.255.255.128": 25,
    "255.255.255.192": 26,
    "255.255.255.224": 27,
    "255.255.255.240": 28,
    "255.255.255.248": 29,
    "255.255.255.252": 30,
}

STAGE_ORDER = [
    "stage-baseline",
    "stage-environment",
    "stage-execution",
    "stage-proxmox",
    "stage-network",
    "stage-ad",
    "stage-dns",
    "stage-dhcp",
    "stage-time",
    "stage-accounts",
    "stage-optional",
    "stage-write",
]

STAGE_LABELS = {
    "stage-baseline": "Stage 1/12: Choose configuration baseline.",
    "stage-environment": "Stage 2/12: Environment metadata.",
    "stage-execution": "Stage 3/12: Execution paths and behavior.",
    "stage-proxmox": "Stage 4/12: Proxmox guest integration.",
    "stage-network": "Stage 5/12: Network and host identity.",
    "stage-ad": "Stage 6/12: Active Directory (new forest).",
    "stage-dns": "Stage 7/12: DNS.",
    "stage-dhcp": "Stage 8/12: DHCP.",
    "stage-time": "Stage 9/12: Domain time.",
    "stage-accounts": "Stage 10/12: Service accounts.",
    "stage-optional": "Stage 11/12: Optional features.",
    "stage-write": "Stage 12/12: Write config.yaml and validate.",
}


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


def ipv4_to_int(address: str) -> int:
    return int(ipaddress.IPv4Address(address))


def ipv4_in_subnet(address: str, network_id: str, prefix_length: int) -> bool:
    network = ipaddress.IPv4Network(f"{network_id}/{prefix_length}", strict=False)
    return ipaddress.IPv4Address(address) in network


def must_ipv4(value: str, label: str) -> None:
    try:
        ipaddress.IPv4Address(value.strip())
    except ValueError as exc:
        raise RuntimeError(f"{label} is not a valid IPv4 address: {value}") from exc


def must_windows_path(value: str, label: str) -> None:
    if re.match(r"^[A-Za-z]:\\", value) or value.startswith("\\\\"):
        return
    raise RuntimeError(f"{label} must be an absolute Windows path (e.g. C:\\ProgramData\\App).")


def parse_ipv4_list(raw: str, label: str) -> list[str]:
    items = [part.strip() for part in raw.split(",") if part.strip()]
    if not items:
        raise RuntimeError(f"{label}: enter at least one IPv4 address.")
    for item in items:
        must_ipv4(item, label)
    return items


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
    #stage-write {
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
        self._refresh_cfg_derived_defaults()

    def _refresh_cfg_derived_defaults(self) -> None:
        dc_ip = str(get_in(self.cfg, ["network", "ipv4", "address"]) or "")
        domain = str(get_in(self.cfg, ["activeDirectory", "domainName"]) or "")
        if dc_ip and domain:
            set_in(self.cfg, ["dhcp", "serverDnsName"], f"{get_in(self.cfg, ['network', 'computerName']) or 'dc01'}.{domain}")
            set_in(self.cfg, ["dhcp", "serverIpAddress"], dc_ip)

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

            with VerticalScroll(id="stage-environment", classes="stage"):
                env = self.cfg.get("environment", {})
                yield Static("Environment metadata (change/ticket tracking). All fields are required.")
                yield Static("Environment name")
                yield Input(str(env.get("name") or ""), id="env_name", classes="field")
                yield Static("Purpose (e.g. lab, production)")
                yield Input(str(env.get("purpose") or ""), id="env_purpose", classes="field")
                yield Static("Change/ticket ID")
                yield Input(str(env.get("changeId") or ""), id="env_change_id", classes="field")
                yield Static("Approved by")
                yield Input(str(env.get("approvedBy") or ""), id="env_approved_by", classes="field")
                yield Static("Maintenance window (ISO8601 start/end)")
                yield Input(str(env.get("maintenanceWindow") or ""), id="env_window", classes="field")
                with Horizontal(classes="stage-nav"):
                    yield Button("Back", id="back_environment", classes="nav-button")
                    yield Button("Next", id="next_environment", variant="primary", classes="nav-button")

            with VerticalScroll(id="stage-execution", classes="stage"):
                exe = self.cfg.get("execution", {})
                yield Static("Local paths on the Windows Server. Use absolute Windows paths only.")
                yield Static("State path")
                yield Input(str(exe.get("statePath") or ""), id="exec_state", classes="field")
                yield Static("Log path")
                yield Input(str(exe.get("logPath") or ""), id="exec_log", classes="field")
                yield Static("Transcript path")
                yield Input(str(exe.get("transcriptPath") or ""), id="exec_transcript", classes="field")
                yield Static("JSON operation log path")
                yield Input(str(exe.get("jsonLogPath") or ""), id="exec_json", classes="field")
                yield Static("Evidence path")
                yield Input(str(exe.get("evidencePath") or ""), id="exec_evidence", classes="field")
                yield Static("Resume scheduled task name")
                yield Input(str(exe.get("resumeScheduledTaskName") or ""), id="exec_task", classes="field")
                with Horizontal(classes="stage-nav"):
                    yield Button("Back", id="back_execution", classes="nav-button")
                    yield Button("Next", id="next_execution", variant="primary", classes="nav-button")

            with VerticalScroll(id="stage-proxmox", classes="stage"):
                pmx = self.cfg.get("proxmoxGuest", {})
                yield Static("Proxmox guest checks (VirtIO + QEMU Guest Agent). Disable if not on Proxmox.")
                yield Static("Is this server a Proxmox VM?")
                yield PersistentSelect(
                    options=[("Yes", "true"), ("No", "false")],
                    value="true" if bool(pmx.get("enabled")) else "false",
                    id="pmx_enabled",
                    classes="field",
                )
                yield Static("Require VirtIO drivers present?")
                yield PersistentSelect(
                    options=[("Yes", "true"), ("No", "false")],
                    value="true" if bool(pmx.get("requireVirtioDrivers")) else "false",
                    id="pmx_virtio",
                    classes="field",
                )
                yield Static("Require QEMU Guest Agent service?")
                yield PersistentSelect(
                    options=[("Yes", "true"), ("No", "false")],
                    value="true" if bool(pmx.get("requireQemuGuestAgent")) else "false",
                    id="pmx_qga",
                    classes="field",
                )
                yield Static("Allow silent guest-tools install if missing?")
                yield PersistentSelect(
                    options=[("No (recommended)", "false"), ("Yes", "true")],
                    value="true" if bool(pmx.get("allowSilentGuestToolsInstall")) else "false",
                    id="pmx_silent",
                    classes="field",
                )
                yield Static("Guest tools installer path (required when silent install is Yes)")
                yield Input(str(pmx.get("guestToolsInstallerPath") or ""), id="pmx_installer", classes="field")
                with Horizontal(classes="stage-nav"):
                    yield Button("Back", id="back_proxmox", classes="nav-button")
                    yield Button("Next", id="next_proxmox", variant="primary", classes="nav-button")

            with VerticalScroll(id="stage-network", classes="stage"):
                net = self.cfg.get("network", {})
                ipv4 = net.get("ipv4", {})
                yield Static("Network identity for the domain controller. Hostname must be 1-15 characters.")
                yield Static("Computer name (hostname)")
                yield Input(str(net.get("computerName") or ""), id="net_hostname", classes="field")
                yield Static("Network interface alias (e.g. Ethernet)")
                yield Input(str(net.get("interfaceAlias") or ""), id="net_iface", classes="field")
                yield Static("Time zone (e.g. UTC, Eastern Standard Time)")
                yield Input(str(net.get("timeZone") or ""), id="net_tz", classes="field")
                yield Static("Static IPv4 address")
                yield Input(str(ipv4.get("address") or ""), id="net_ip", classes="field")
                yield Static("IPv4 prefix length (1-32)")
                yield Input(str(ipv4.get("prefixLength") or ""), id="net_prefix", classes="field")
                yield Static("Default gateway")
                yield Input(str(ipv4.get("defaultGateway") or ""), id="net_gw", classes="field")
                yield Static("DNS servers BEFORE promotion (comma-separated IPv4)")
                yield Input(", ".join(ipv4.get("dnsClientServersBeforePromotion") or []), id="net_dns_before", classes="field")
                yield Static("DNS servers AFTER promotion (comma-separated IPv4; loopback is typical)")
                yield Input(", ".join(ipv4.get("dnsClientServersAfterPromotion") or []), id="net_dns_after", classes="field")
                with Horizontal(classes="stage-nav"):
                    yield Button("Back", id="back_network", classes="nav-button")
                    yield Button("Next", id="next_network", variant="primary", classes="nav-button")

            with VerticalScroll(id="stage-ad", classes="stage"):
                ad = self.cfg.get("activeDirectory", {})
                site = ad.get("site", {})
                yield Static("New forest settings. Domain FQDN must be dotted unless you explicitly allow single-label.")
                yield Static("AD domain FQDN (e.g. corp.example.com)")
                yield Input(str(ad.get("domainName") or ""), id="ad_domain", classes="field")
                yield Static("NetBIOS name (1-15 chars)")
                yield Input(str(ad.get("netbiosName") or ""), id="ad_netbios", classes="field")
                yield Static("Forest functional level")
                yield Input(str(ad.get("forestMode") or ""), id="ad_forest", classes="field")
                yield Static("Domain functional level")
                yield Input(str(ad.get("domainMode") or ""), id="ad_domain_mode", classes="field")
                yield Static("NTDS database path")
                yield Input(str(ad.get("databasePath") or ""), id="ad_db", classes="field")
                yield Static("NTDS log path")
                yield Input(str(ad.get("logPath") or ""), id="ad_log", classes="field")
                yield Static("SYSVOL path")
                yield Input(str(ad.get("sysvolPath") or ""), id="ad_sysvol", classes="field")
                yield Static("Rename the default AD site?")
                yield PersistentSelect(
                    options=[("Yes", "true"), ("No", "false")],
                    value="true" if bool(site.get("renameDefaultSite")) else "false",
                    id="ad_rename_site",
                    classes="field",
                )
                yield Static("New site name (required when rename is Yes)")
                yield Input(str(site.get("newSiteName") or ""), id="ad_site_name", classes="field")
                with Horizontal(classes="stage-nav"):
                    yield Button("Back", id="back_ad", classes="nav-button")
                    yield Button("Next", id="next_ad", variant="primary", classes="nav-button")

            with VerticalScroll(id="stage-dns", classes="stage"):
                dns = self.cfg.get("dns", {})
                dc_ip = str(get_in(self.cfg, ["network", "ipv4", "address"]) or "192.168.1.10")
                default_rev = re.sub(r"\.\d+$", ".0", dc_ip) + "/24"
                yield Static("DNS forwarders must not include this server's own IP unless explicitly allowed.")
                yield Static("DNS forwarders (comma-separated IPv4)")
                yield Input(", ".join(dns.get("forwarders") or []), id="dns_forwarders", classes="field")
                yield Static(f"Create reverse lookup zone for {default_rev}?")
                yield PersistentSelect(
                    options=[("Yes", "true"), ("No", "false")],
                    value="true" if bool(dns.get("createReverseLookupZones")) else "false",
                    id="dns_reverse",
                    classes="field",
                )
                with Horizontal(classes="stage-nav"):
                    yield Button("Back", id="back_dns", classes="nav-button")
                    yield Button("Next", id="next_dns", variant="primary", classes="nav-button")

            with VerticalScroll(id="stage-dhcp", classes="stage"):
                dhcp = self.cfg.get("dhcp", {})
                scope = (dhcp.get("scopes") or [{}])[0]
                opts = scope.get("options", {})
                yield Static("DHCP on this server. Scope fields apply when you choose to redefine scopes.")
                yield Static("Configure DHCP on this server?")
                yield PersistentSelect(
                    options=[("Yes", "true"), ("No", "false")],
                    value="true" if bool(dhcp.get("enabled")) else "false",
                    id="dhcp_enabled",
                    classes="field",
                )
                yield Static("Authorize DHCP in Active Directory?")
                yield PersistentSelect(
                    options=[("Yes", "true"), ("No", "false")],
                    value="true" if bool(dhcp.get("authorizeInActiveDirectory")) else "false",
                    id="dhcp_authorize",
                    classes="field",
                )
                yield Static("Reconcile/overwrite conflicting existing scope?")
                yield PersistentSelect(
                    options=[("No", "false"), ("Yes", "true")],
                    value="true" if bool(dhcp.get("reconcileExisting")) else "false",
                    id="dhcp_reconcile",
                    classes="field",
                )
                yield Static("DHCP server DNS name (FQDN)")
                yield Input(str(dhcp.get("serverDnsName") or ""), id="dhcp_server_name", classes="field")
                yield Static("DHCP server IP address")
                yield Input(str(dhcp.get("serverIpAddress") or ""), id="dhcp_server_ip", classes="field")
                yield Static("Redefine the primary DHCP scope now? (No keeps template scopes)")
                yield PersistentSelect(
                    options=[("No - keep baseline scopes", "false"), ("Yes - define one scope", "true")],
                    value="false",
                    id="dhcp_redefine",
                    classes="field",
                )
                yield Static("Scope name")
                yield Input(str(scope.get("name") or ""), id="dhcp_scope_name", classes="field")
                yield Static("Subnet mask")
                yield PersistentSelect(
                    options=[(mask, mask) for mask in SUPPORTED_MASKS],
                    value=str(scope.get("subnetMask") or "255.255.255.0"),
                    id="dhcp_scope_mask",
                    classes="field",
                )
                yield Static("Scope network ID (e.g. 192.168.10.0)")
                yield Input(str(scope.get("scopeId") or ""), id="dhcp_scope_id", classes="field")
                yield Static("Start of range")
                yield Input(str(scope.get("startRange") or ""), id="dhcp_start", classes="field")
                yield Static("End of range")
                yield Input(str(scope.get("endRange") or ""), id="dhcp_end", classes="field")
                yield Static("Router/gateway option (comma-separated IPv4)")
                yield Input(", ".join(opts.get("router") or []), id="dhcp_router", classes="field")
                yield Static("DNS servers option (comma-separated IPv4)")
                yield Input(", ".join(opts.get("dnsServers") or []), id="dhcp_dns", classes="field")
                yield Static("DNS domain option")
                yield Input(str(opts.get("dnsDomain") or ""), id="dhcp_domain", classes="field")
                yield Static("NTP servers option (comma-separated IPv4)")
                yield Input(", ".join(opts.get("ntpServers") or []), id="dhcp_ntp", classes="field")
                with Horizontal(classes="stage-nav"):
                    yield Button("Back", id="back_dhcp", classes="nav-button")
                    yield Button("Next", id="next_dhcp", variant="primary", classes="nav-button")

            with VerticalScroll(id="stage-time", classes="stage"):
                time_cfg = self.cfg.get("time", {})
                yield Static("Domain time (w32time). External NTP servers required when authoritative.")
                yield Static("Make this server authoritative time source for the domain?")
                yield PersistentSelect(
                    options=[("Yes", "true"), ("No", "false")],
                    value="true" if bool(time_cfg.get("authoritativeForDomain")) else "false",
                    id="time_auth",
                    classes="field",
                )
                yield Static("External NTP servers (comma-separated hostnames or IPv4)")
                yield Input(", ".join(time_cfg.get("externalNtpServers") or []), id="time_ntp", classes="field")
                yield Static("If this server is NOT the PDC emulator")
                yield PersistentSelect(
                    options=[("stop", "stop"), ("warn", "warn"), ("skip", "skip")],
                    value=str(time_cfg.get("behaviorIfNotPdc") or "stop"),
                    id="time_not_pdc",
                    classes="field",
                )
                with Horizontal(classes="stage-nav"):
                    yield Button("Back", id="back_time", classes="nav-button")
                    yield Button("Next", id="next_time", variant="primary", classes="nav-button")

            with VerticalScroll(id="stage-accounts", classes="stage"):
                svc = self.cfg.get("serviceAccounts", {})
                baseline = ", ".join(str(a.get("samAccountName") or "") for a in (svc.get("accounts") or []))
                yield Static(f"Service accounts from the baseline: {baseline or '(none)'}")
                yield Static("Create service accounts?")
                yield PersistentSelect(
                    options=[("Yes", "true"), ("No", "false")],
                    value="true" if bool(svc.get("enabled")) else "false",
                    id="svc_enabled",
                    classes="field",
                )
                yield Static("Passwords are prompted at runtime and are never stored in YAML.")
                with Horizontal(classes="stage-nav"):
                    yield Button("Back", id="back_accounts", classes="nav-button")
                    yield Button("Next", id="next_accounts", variant="primary", classes="nav-button")

            with VerticalScroll(id="stage-optional", classes="stage"):
                pki = self.cfg.get("pki", {})
                wsus = self.cfg.get("wsus", {})
                evt = self.cfg.get("eventForwarding", {})
                wz = self.cfg.get("wazuh", {})
                idi = self.cfg.get("identityIntegrations", {})
                bkp = self.cfg.get("backupRecovery", {})
                yield Static("Optional features must be explicitly on or off. Enable only what you prepared.")
                yield Static("Enable PKI (AD Certificate Services)?")
                yield PersistentSelect(
                    options=[("No", "false"), ("Yes", "true")],
                    value="true" if bool(pki.get("enabled")) else "false",
                    id="opt_pki",
                    classes="field",
                )
                yield Static("Root CA common name (when PKI enabled with root CA)")
                yield Input(str(get_in(pki, ["rootCa", "caCommonName"]) or ""), id="opt_pki_cn", classes="field")
                yield Static("Enable WSUS?")
                yield PersistentSelect(
                    options=[("No", "false"), ("Yes", "true")],
                    value="true" if bool(wsus.get("enabled")) else "false",
                    id="opt_wsus",
                    classes="field",
                )
                yield Static("WSUS content directory")
                yield Input(str(wsus.get("contentDirectory") or ""), id="opt_wsus_dir", classes="field")
                yield Static("Enable Windows Event Forwarding?")
                yield PersistentSelect(
                    options=[("No", "false"), ("Yes", "true")],
                    value="true" if bool(evt.get("enabled")) else "false",
                    id="opt_evt",
                    classes="field",
                )
                yield Static("Enable Wazuh agent?")
                yield PersistentSelect(
                    options=[("No", "false"), ("Yes", "true")],
                    value="true" if bool(wz.get("enabled")) else "false",
                    id="opt_wazuh",
                    classes="field",
                )
                yield Static("Wazuh agent MSI path (local or UNC)")
                yield Input(str(wz.get("agentMsiPath") or ""), id="opt_wazuh_msi", classes="field")
                yield Static("Wazuh manager address")
                yield Input(str(wz.get("managerAddress") or ""), id="opt_wazuh_mgr", classes="field")
                yield Static("Write identity-integration artifacts (GitLab/Keycloak/YubiKey)?")
                yield PersistentSelect(
                    options=[("No", "false"), ("Yes", "true")],
                    value="true" if bool(idi.get("enabled")) else "false",
                    id="opt_idi",
                    classes="field",
                )
                yield Static("AD backup path")
                yield Input(str(bkp.get("backupPath") or ""), id="opt_backup", classes="field")
                with Horizontal(classes="stage-nav"):
                    yield Button("Back", id="back_optional", classes="nav-button")
                    yield Button("Next", id="next_optional", variant="primary", classes="nav-button")

            with Vertical(id="stage-write", classes="stage"):
                with Horizontal(classes="write-center"):
                    yield Button("Back", id="back_write", classes="nav-button")
                    yield Button("WRITE CONFIG\n[dim](press enter)[/dim]", id="write_now")

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

    def _bool_select(self, widget_id: str) -> bool:
        return self._select(widget_id) == "true"

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
        if self.current_stage == "stage-write":
            legend = f"Now: highlight WRITE CONFIG and press Enter to write config.yaml and run validation.{armed_suffix}"
        else:
            legend = f"Now: fill fields, then highlight Next and press Enter to validate this stage.{armed_suffix}"
        self.query_one("#control_legend", Static).update(legend)

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

    def _validate_hostname(self, value: str) -> None:
        if len(value) < 1 or len(value) > 15:
            raise RuntimeError("Hostname must be 1-15 characters.")
        if not re.match(r"^[A-Za-z0-9-]+$", value):
            raise RuntimeError("Hostname may contain only letters, digits, and hyphens.")

    def _validate_netbios(self, value: str) -> None:
        if len(value) < 1 or len(value) > 15:
            raise RuntimeError("NetBIOS name must be 1-15 characters.")
        if not re.match(r"^[A-Za-z0-9-]+$", value):
            raise RuntimeError("NetBIOS name may contain only letters, digits, and hyphens.")

    def _validate_domain(self, value: str) -> None:
        ad = self.cfg.get("activeDirectory", {})
        if "." not in value and not bool(ad.get("allowSingleLabelDomain")):
            raise RuntimeError("Single-label domains are not allowed. Use a dotted FQDN (e.g. corp.example.com).")
        if value.lower().endswith(".local") and not bool(ad.get("allowDotLocal")):
            raise RuntimeError(".local domains are discouraged and not allowed by this config.")

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
            self._refresh_cfg_derived_defaults()
            self.append_log(f"Loaded baseline from {self.baseline_path.name}.")
            self.switch_stage("stage-environment")
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 1 failed: {exc}")
            self.set_status("Stage 1 failed. Fix selection and try again.")

    def validate_environment_stage(self) -> None:
        try:
            for widget_id, path, label in [
                ("env_name", ["environment", "name"], "Environment name"),
                ("env_purpose", ["environment", "purpose"], "Purpose"),
                ("env_change_id", ["environment", "changeId"], "Change/ticket ID"),
                ("env_approved_by", ["environment", "approvedBy"], "Approved by"),
                ("env_window", ["environment", "maintenanceWindow"], "Maintenance window"),
            ]:
                value = self._input(widget_id)
                self._require_text(value, label)
                set_in(self.cfg, path, value)
            self.append_log("Environment metadata validated.")
            self.switch_stage("stage-execution")
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 2 failed: {exc}")
            self.set_status("Stage 2 failed. Fix fields and try again.")

    def validate_execution_stage(self) -> None:
        try:
            mapping = [
                ("exec_state", ["execution", "statePath"], "State path"),
                ("exec_log", ["execution", "logPath"], "Log path"),
                ("exec_transcript", ["execution", "transcriptPath"], "Transcript path"),
                ("exec_json", ["execution", "jsonLogPath"], "JSON log path"),
                ("exec_evidence", ["execution", "evidencePath"], "Evidence path"),
            ]
            for widget_id, path, label in mapping:
                value = self._input(widget_id)
                self._require_text(value, label)
                must_windows_path(value, label)
                set_in(self.cfg, path, value)
            task = self._input("exec_task")
            self._require_text(task, "Resume scheduled task name")
            set_in(self.cfg, ["execution", "resumeScheduledTaskName"], task)
            self.append_log("Execution paths validated.")
            self.switch_stage("stage-proxmox")
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 3 failed: {exc}")
            self.set_status("Stage 3 failed. Fix fields and try again.")

    def validate_proxmox_stage(self) -> None:
        try:
            enabled = self._bool_select("pmx_enabled")
            set_in(self.cfg, ["proxmoxGuest", "enabled"], enabled)
            if enabled:
                set_in(self.cfg, ["proxmoxGuest", "requireVirtioDrivers"], self._bool_select("pmx_virtio"))
                set_in(self.cfg, ["proxmoxGuest", "requireQemuGuestAgent"], self._bool_select("pmx_qga"))
                silent = self._bool_select("pmx_silent")
                set_in(self.cfg, ["proxmoxGuest", "allowSilentGuestToolsInstall"], silent)
                installer = self._input("pmx_installer")
                if silent:
                    self._require_text(installer, "Guest tools installer path")
                    must_windows_path(installer, "Guest tools installer path")
                set_in(self.cfg, ["proxmoxGuest", "guestToolsInstallerPath"], installer)
            self.append_log("Proxmox guest settings validated.")
            self.switch_stage("stage-network")
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 4 failed: {exc}")
            self.set_status("Stage 4 failed. Fix fields and try again.")

    def validate_network_stage(self) -> None:
        try:
            hostname = self._input("net_hostname")
            self._validate_hostname(hostname)
            iface = self._input("net_iface")
            tz = self._input("net_tz")
            ip = self._input("net_ip")
            prefix_raw = self._input("net_prefix")
            gw = self._input("net_gw")
            dns_before = self._input("net_dns_before")
            dns_after = self._input("net_dns_after")
            for label, value in [("Interface alias", iface), ("Time zone", tz)]:
                self._require_text(value, label)
            must_ipv4(ip, "Static IPv4 address")
            must_ipv4(gw, "Default gateway")
            try:
                prefix = int(prefix_raw)
            except ValueError as exc:
                raise RuntimeError("IPv4 prefix length must be a whole number between 1 and 32.") from exc
            if prefix < 1 or prefix > 32:
                raise RuntimeError("IPv4 prefix length must be between 1 and 32.")
            before_list = parse_ipv4_list(dns_before, "DNS before promotion")
            after_list = parse_ipv4_list(dns_after, "DNS after promotion")
            set_in(self.cfg, ["network", "enabled"], True)
            set_in(self.cfg, ["network", "computerName"], hostname)
            set_in(self.cfg, ["network", "interfaceAlias"], iface)
            set_in(self.cfg, ["network", "timeZone"], tz)
            set_in(self.cfg, ["network", "ipv4", "address"], ip)
            set_in(self.cfg, ["network", "ipv4", "prefixLength"], prefix)
            set_in(self.cfg, ["network", "ipv4", "defaultGateway"], gw)
            set_in(self.cfg, ["network", "ipv4", "dnsClientServersBeforePromotion"], before_list)
            set_in(self.cfg, ["network", "ipv4", "dnsClientServersAfterPromotion"], after_list)
            self._refresh_cfg_derived_defaults()
            self.append_log("Network settings validated.")
            self.switch_stage("stage-ad")
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 5 failed: {exc}")
            self.set_status("Stage 5 failed. Fix fields and try again.")

    def validate_ad_stage(self) -> None:
        try:
            domain = self._input("ad_domain")
            netbios = self._input("ad_netbios")
            forest = self._input("ad_forest")
            domain_mode = self._input("ad_domain_mode")
            db = self._input("ad_db")
            log_path = self._input("ad_log")
            sysvol = self._input("ad_sysvol")
            rename_site = self._bool_select("ad_rename_site")
            site_name = self._input("ad_site_name")
            self._validate_domain(domain)
            self._validate_netbios(netbios)
            for label, value in [
                ("Forest functional level", forest),
                ("Domain functional level", domain_mode),
            ]:
                self._require_text(value, label)
            for label, value, path_key in [
                ("NTDS database path", db, "databasePath"),
                ("NTDS log path", log_path, "logPath"),
                ("SYSVOL path", sysvol, "sysvolPath"),
            ]:
                self._require_text(value, label)
                must_windows_path(value, label)
                set_in(self.cfg, ["activeDirectory", path_key], value)
            if rename_site:
                self._require_text(site_name, "New site name")
            set_in(self.cfg, ["activeDirectory", "enabled"], True)
            set_in(self.cfg, ["activeDirectory", "domainName"], domain)
            set_in(self.cfg, ["activeDirectory", "netbiosName"], netbios)
            set_in(self.cfg, ["activeDirectory", "forestMode"], forest)
            set_in(self.cfg, ["activeDirectory", "domainMode"], domain_mode)
            set_in(self.cfg, ["activeDirectory", "site", "renameDefaultSite"], rename_site)
            if rename_site:
                set_in(self.cfg, ["activeDirectory", "site", "newSiteName"], site_name)
            self.append_log("Active Directory settings validated.")
            self.switch_stage("stage-dns")
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 6 failed: {exc}")
            self.set_status("Stage 6 failed. Fix fields and try again.")

    def validate_dns_stage(self) -> None:
        try:
            dc_ip = str(get_in(self.cfg, ["network", "ipv4", "address"]) or "")
            domain = str(get_in(self.cfg, ["activeDirectory", "domainName"]) or "")
            forwarders = parse_ipv4_list(self._input("dns_forwarders"), "DNS forwarders")
            allow_self = bool(get_in(self.cfg, ["dns", "allowForwardersPointingToSelf"]))
            if not allow_self and dc_ip in forwarders:
                raise RuntimeError(f"Forwarders must not include this server's own IP ({dc_ip}).")
            create_reverse = self._bool_select("dns_reverse")
            set_in(self.cfg, ["dns", "enabled"], True)
            set_in(self.cfg, ["dns", "forwarders"], forwarders)
            set_in(self.cfg, ["dns", "createReverseLookupZones"], create_reverse)
            if create_reverse:
                rev_net = re.sub(r"\.\d+$", ".0", dc_ip) + "/24"
                set_in(
                    self.cfg,
                    ["dns", "reverseLookupZones"],
                    [{"networkId": rev_net, "replicationScope": "Forest"}],
                )
            set_in(
                self.cfg,
                ["dns", "requiredRecordsToValidate"],
                [
                    {"name": domain, "type": "A"},
                    {"name": f"_ldap._tcp.dc._msdcs.{domain}", "type": "SRV"},
                ],
            )
            self.append_log("DNS settings validated.")
            self.switch_stage("stage-dhcp")
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 7 failed: {exc}")
            self.set_status("Stage 7 failed. Fix fields and try again.")

    def validate_dhcp_stage(self) -> None:
        try:
            enabled = self._bool_select("dhcp_enabled")
            set_in(self.cfg, ["dhcp", "enabled"], enabled)
            set_in(self.cfg, ["roles", "dhcp", "enabled"], enabled)
            if not enabled:
                self.append_log("DHCP disabled; skipping scope validation.")
                self.switch_stage("stage-time")
                return
            set_in(self.cfg, ["dhcp", "authorizeInActiveDirectory"], self._bool_select("dhcp_authorize"))
            set_in(self.cfg, ["dhcp", "reconcileExisting"], self._bool_select("dhcp_reconcile"))
            server_name = self._input("dhcp_server_name")
            server_ip = self._input("dhcp_server_ip")
            self._require_text(server_name, "DHCP server DNS name")
            must_ipv4(server_ip, "DHCP server IP address")
            set_in(self.cfg, ["dhcp", "serverDnsName"], server_name)
            set_in(self.cfg, ["dhcp", "serverIpAddress"], server_ip)
            if self._bool_select("dhcp_redefine"):
                mask = self._select("dhcp_scope_mask")
                if mask not in SUPPORTED_MASKS:
                    raise RuntimeError("Choose a supported subnet mask.")
                prefix = SUPPORTED_MASKS[mask]
                scope_id = self._input("dhcp_scope_id")
                start = self._input("dhcp_start")
                end = self._input("dhcp_end")
                name = self._input("dhcp_scope_name")
                router = parse_ipv4_list(self._input("dhcp_router"), "Router option")
                dns_servers = parse_ipv4_list(self._input("dhcp_dns"), "DNS servers option")
                dns_domain = self._input("dhcp_domain")
                ntp_servers = parse_ipv4_list(self._input("dhcp_ntp"), "NTP servers option")
                self._require_text(name, "Scope name")
                self._require_text(dns_domain, "DNS domain option")
                must_ipv4(scope_id, "Scope network ID")
                must_ipv4(start, "Start of range")
                must_ipv4(end, "End of range")
                if not ipv4_in_subnet(start, scope_id, prefix):
                    raise RuntimeError(f"Start of range is not inside {scope_id}/{prefix}.")
                if not ipv4_in_subnet(end, scope_id, prefix):
                    raise RuntimeError(f"End of range is not inside {scope_id}/{prefix}.")
                if ipv4_to_int(end) < ipv4_to_int(start):
                    raise RuntimeError("End of range must be greater than or equal to start of range.")
                scope = {
                    "name": name,
                    "scopeId": scope_id,
                    "startRange": start,
                    "endRange": end,
                    "subnetMask": mask,
                    "leaseDuration": "8.00:00:00",
                    "state": "Active",
                    "options": {
                        "router": router,
                        "dnsServers": dns_servers,
                        "dnsDomain": dns_domain,
                        "ntpServers": ntp_servers,
                    },
                    "reservations": [],
                }
                set_in(self.cfg, ["dhcp", "scopes"], [scope])
            self.append_log("DHCP settings validated.")
            self.switch_stage("stage-time")
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 8 failed: {exc}")
            self.set_status("Stage 8 failed. Fix fields and try again.")

    def validate_time_stage(self) -> None:
        try:
            authoritative = self._bool_select("time_auth")
            set_in(self.cfg, ["time", "enabled"], True)
            set_in(self.cfg, ["time", "authoritativeForDomain"], authoritative)
            set_in(self.cfg, ["time", "behaviorIfNotPdc"], self._select("time_not_pdc"))
            if authoritative:
                ntp_raw = self._input("time_ntp")
                servers = [part.strip() for part in ntp_raw.split(",") if part.strip()]
                if not servers:
                    raise RuntimeError("At least one external NTP server is required when authoritative.")
                set_in(self.cfg, ["time", "externalNtpServers"], servers)
            self.append_log("Domain time settings validated.")
            self.switch_stage("stage-accounts")
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 9 failed: {exc}")
            self.set_status("Stage 9 failed. Fix fields and try again.")

    def validate_accounts_stage(self) -> None:
        try:
            set_in(self.cfg, ["serviceAccounts", "enabled"], self._bool_select("svc_enabled"))
            self.append_log("Service account settings validated.")
            self.switch_stage("stage-optional")
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 10 failed: {exc}")
            self.set_status("Stage 10 failed. Fix fields and try again.")

    def validate_optional_stage(self) -> None:
        try:
            pki_enabled = self._bool_select("opt_pki")
            wsus_enabled = self._bool_select("opt_wsus")
            wazuh_enabled = self._bool_select("opt_wazuh")
            set_in(self.cfg, ["pki", "enabled"], pki_enabled)
            set_in(self.cfg, ["roles", "pki", "enabled"], pki_enabled)
            if pki_enabled:
                cn = self._input("opt_pki_cn")
                self._require_text(cn, "Root CA common name")
                set_in(self.cfg, ["pki", "rootCa", "caCommonName"], cn)
            set_in(self.cfg, ["wsus", "enabled"], wsus_enabled)
            set_in(self.cfg, ["roles", "wsus", "enabled"], wsus_enabled)
            if wsus_enabled:
                wsus_dir = self._input("opt_wsus_dir")
                self._require_text(wsus_dir, "WSUS content directory")
                must_windows_path(wsus_dir, "WSUS content directory")
                set_in(self.cfg, ["wsus", "contentDirectory"], wsus_dir)
            set_in(self.cfg, ["eventForwarding", "enabled"], self._bool_select("opt_evt"))
            set_in(self.cfg, ["wazuh", "enabled"], wazuh_enabled)
            if wazuh_enabled:
                msi = self._input("opt_wazuh_msi")
                mgr = self._input("opt_wazuh_mgr")
                self._require_text(msi, "Wazuh agent MSI path")
                self._require_text(mgr, "Wazuh manager address")
                set_in(self.cfg, ["wazuh", "agentMsiPath"], msi)
                set_in(self.cfg, ["wazuh", "managerAddress"], mgr)
            set_in(self.cfg, ["identityIntegrations", "enabled"], self._bool_select("opt_idi"))
            backup = self._input("opt_backup")
            self._require_text(backup, "AD backup path")
            must_windows_path(backup, "AD backup path")
            set_in(self.cfg, ["backupRecovery", "backupPath"], backup)
            self.append_log("Optional feature settings validated.")
            self.switch_stage("stage-write")
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 11 failed: {exc}")
            self.set_status("Stage 11 failed. Fix fields and try again.")

    def _run_powershell_validation(self, config_path: Path) -> None:
        ps_script = f"""
Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'
. '{ROOT / "lib" / "Config.ps1"}'
$loaded = Import-ProjectConfig -ConfigPath '{config_path}'
Assert-ProjectConfig -Config $loaded
Write-Output 'VALIDATION_OK'
""".strip()
        for exe in ("pwsh", "powershell"):
            proc = subprocess.run(
                [exe, "-NoProfile", "-Command", ps_script],
                cwd=str(ROOT),
                text=True,
                capture_output=True,
                check=False,
            )
            if proc.returncode == 0 and "VALIDATION_OK" in proc.stdout:
                return
            if proc.returncode != 0 and exe == "powershell":
                detail = (proc.stderr or proc.stdout).strip()
                raise RuntimeError(detail or "PowerShell validation failed.")
        raise RuntimeError("PowerShell is not available; config.yaml was written but not validated.")

    def write_config(self) -> None:
        try:
            if OUTPUT_PATH.exists():
                backup = backup_file(OUTPUT_PATH)
                self.append_log(f"Backed up existing config.yaml to {backup.name}.")
            dump_yaml(OUTPUT_PATH, self.cfg)
            self.append_log(f"Wrote {OUTPUT_PATH.name}.")
            try:
                self._run_powershell_validation(OUTPUT_PATH)
                self.append_log("Validation PASSED. config.yaml is ready.")
                self.set_status("Complete. Run Configure-WindowsServer.ps1 -ConfigPath .\\config.yaml -PlanOnly")
            except RuntimeError as exc:
                self.append_log(f"[WARN] {exc}")
                self.set_status("config.yaml written; fix validation errors before running the server script.")
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Write failed: {exc}")
            self.set_status("Write failed. Review the log and try again.")

    @on(Button.Pressed, "#next_baseline")
    def on_next_baseline(self) -> None:
        self.validate_baseline_stage()

    @on(Button.Pressed, "#back_environment")
    def on_back_environment(self) -> None:
        self.switch_stage("stage-baseline")

    @on(Button.Pressed, "#next_environment")
    def on_next_environment(self) -> None:
        self.validate_environment_stage()

    @on(Button.Pressed, "#back_execution")
    def on_back_execution(self) -> None:
        self.switch_stage("stage-environment")

    @on(Button.Pressed, "#next_execution")
    def on_next_execution(self) -> None:
        self.validate_execution_stage()

    @on(Button.Pressed, "#back_proxmox")
    def on_back_proxmox(self) -> None:
        self.switch_stage("stage-execution")

    @on(Button.Pressed, "#next_proxmox")
    def on_next_proxmox(self) -> None:
        self.validate_proxmox_stage()

    @on(Button.Pressed, "#back_network")
    def on_back_network(self) -> None:
        self.switch_stage("stage-proxmox")

    @on(Button.Pressed, "#next_network")
    def on_next_network(self) -> None:
        self.validate_network_stage()

    @on(Button.Pressed, "#back_ad")
    def on_back_ad(self) -> None:
        self.switch_stage("stage-network")

    @on(Button.Pressed, "#next_ad")
    def on_next_ad(self) -> None:
        self.validate_ad_stage()

    @on(Button.Pressed, "#back_dns")
    def on_back_dns(self) -> None:
        self.switch_stage("stage-ad")

    @on(Button.Pressed, "#next_dns")
    def on_next_dns(self) -> None:
        self.validate_dns_stage()

    @on(Button.Pressed, "#back_dhcp")
    def on_back_dhcp(self) -> None:
        self.switch_stage("stage-dns")

    @on(Button.Pressed, "#next_dhcp")
    def on_next_dhcp(self) -> None:
        self.validate_dhcp_stage()

    @on(Button.Pressed, "#back_time")
    def on_back_time(self) -> None:
        self.switch_stage("stage-dhcp")

    @on(Button.Pressed, "#next_time")
    def on_next_time(self) -> None:
        self.validate_time_stage()

    @on(Button.Pressed, "#back_accounts")
    def on_back_accounts(self) -> None:
        self.switch_stage("stage-time")

    @on(Button.Pressed, "#next_accounts")
    def on_next_accounts(self) -> None:
        self.validate_accounts_stage()

    @on(Button.Pressed, "#back_optional")
    def on_back_optional(self) -> None:
        self.switch_stage("stage-accounts")

    @on(Button.Pressed, "#next_optional")
    def on_next_optional(self) -> None:
        self.validate_optional_stage()

    @on(Button.Pressed, "#back_write")
    def on_back_write(self) -> None:
        self.switch_stage("stage-optional")

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
