#!/usr/bin/env python3
from __future__ import annotations

from datetime import datetime
from pathlib import Path
import ipaddress
import json
import socket
import shutil
import subprocess
import sys
from typing import Any

import winrm
import yaml
from proxmoxer import ProxmoxAPI
from textual import on
from textual import events
from textual.app import App, ComposeResult
from textual.containers import Vertical, Horizontal, VerticalScroll
from textual.widgets import Footer, Input as TextInput, Button, Static, Log, Select, ContentSwitcher, ProgressBar


ROOT = Path(__file__).resolve().parents[1]
GROUP_VARS_PATH = ROOT / "inventories" / "windows-deployer" / "group_vars" / "all.yml"
HOSTS_PATH = ROOT / "inventories" / "windows-deployer" / "hosts.yml"
BOOTSTRAP_PATH = ROOT / "scripts" / "bootstrap-controller.sh"
RUN_FULL_DEPLOY_PATH = ROOT / "scripts" / "run-full-deploy.sh"


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


class SetupApp(App[None]):
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

    def __init__(self) -> None:
        super().__init__()
        self.group_vars = load_yaml(GROUP_VARS_PATH)
        self.hosts = load_yaml(HOSTS_PATH)
        self.bridges: list[str] = [str(get_in(self.group_vars, ["deployer", "lxc", "bridge"]) or "vmbr0")]
        self.selected_template_name: str | None = None
        node_default = str(get_in(self.group_vars, ["proxmox", "node"]) or "")
        storage_default = str(get_in(self.group_vars, ["proxmox", "defaults", "storage_pool"]) or "")
        template_storage_default = str(get_in(self.group_vars, ["proxmox", "defaults", "template_storage"]) or "")
        self.available_nodes: list[str] = [v for v in [node_default] if v]
        self.available_storages: list[str] = [v for v in [storage_default, template_storage_default] if v]
        self.current_stage = "stage-proxmox-auth"
        self.quit_armed = False
        self.launch_deploy_after_exit = False

    def compose(self) -> ComposeResult:
        yield Static("Stage 1/7: Validate Proxmox credentials.", id="status")
        yield Static("Controls: Tab/Shift+Tab move fields, arrows navigate fields/options, Enter opens/selects dropdown options, q = Quit.", id="help")
        yield Static("", id="control_legend")
        yield ProgressBar(total=7, show_eta=False, show_percentage=True, id="stage_progress")
        with ContentSwitcher(initial="stage-proxmox-auth", id="main-switcher"):
            with VerticalScroll(id="stage-proxmox-auth", classes="stage"):
                yield Static("Stage 1: Validate Proxmox host reachability and API username/password first.")
                yield Static("Proxmox Host (IP/FQDN)")
                yield Input(str(get_in(self.group_vars, ["proxmox", "host"]) or ""), id="px_host", classes="field")
                yield Static("Proxmox SSH User (usually root)")
                yield Input(str(get_in(self.hosts, ["all", "children", "proxmox_nodes", "hosts", "pve", "ansible_user"]) or "root"), id="px_ssh_user", classes="field")
                yield Static("Proxmox SSH Password")
                yield Input(str(get_in(self.hosts, ["all", "children", "proxmox_nodes", "hosts", "pve", "ansible_ssh_pass"]) or ""), password=True, id="px_ssh_pass", classes="field")
                yield Static("Skip TLS verify for Proxmox API?")
                yield PersistentSelect(options=[("Yes (lab/self-signed)", "true"), ("No (strict cert validation)", "false")], value="true" if bool(get_in(self.group_vars, ["proxmox", "insecure_skip_tls_verify"])) else "false", id="px_skip_tls", classes="field")
                with Horizontal(classes="stage-nav"):
                    yield Button("Next", id="next_auth", variant="primary", classes="nav-button")
            with VerticalScroll(id="stage-proxmox-node", classes="stage"):
                yield Static("Stage 2: Select the Proxmox node first.")
                yield Static("Proxmox Node Name")
                yield PersistentSelect(
                    options=[(n, n) for n in self.available_nodes] or [("No nodes discovered yet", "")],
                    value=self.available_nodes[0] if self.available_nodes else "",
                    id="px_node",
                    classes="field",
                )
                with Horizontal(classes="stage-nav"):
                    yield Button("Back", id="back_node", classes="nav-button")
                    yield Button("Next", id="next_node", variant="primary", classes="nav-button")
            with VerticalScroll(id="stage-proxmox-storage", classes="stage"):
                yield Static("Stage 3: Select storage values available on the selected node and validate template/bridge.")
                yield Static("LXC Storage Pool (must exist)")
                yield PersistentSelect(
                    options=[(s, s) for s in self.available_storages] or [("No storages discovered yet", "")],
                    value=(str(get_in(self.group_vars, ["proxmox", "defaults", "storage_pool"]) or "") if str(get_in(self.group_vars, ["proxmox", "defaults", "storage_pool"]) or "") in self.available_storages else (self.available_storages[0] if self.available_storages else "")),
                    id="px_storage_pool",
                    classes="field",
                )
                yield Static("Template Storage (must exist)")
                yield PersistentSelect(
                    options=[(s, s) for s in self.available_storages] or [("No storages discovered yet", "")],
                    value=(str(get_in(self.group_vars, ["proxmox", "defaults", "template_storage"]) or "") if str(get_in(self.group_vars, ["proxmox", "defaults", "template_storage"]) or "") in self.available_storages else (self.available_storages[0] if self.available_storages else "")),
                    id="px_template_storage",
                    classes="field",
                )
                with Horizontal(classes="stage-nav"):
                    yield Button("Back", id="back_storage", classes="nav-button")
                    yield Button("Next", id="next_storage", variant="primary", classes="nav-button")
            with VerticalScroll(id="stage-golden", classes="stage"):
                yield Static("Stage 4: Golden image VM running + WinRM port + WinRM credential validation.")
                yield Static("Golden Image VMID (must be running)")
                yield Input(str(get_in(self.group_vars, ["windows", "goldimage", "vmid"]) or ""), id="gold_vmid", classes="field")
                yield Static("Golden Image IP (WinRM)")
                yield Input(str(get_in(self.group_vars, ["windows", "goldimage", "ip"]) or ""), id="gold_ip", classes="field")
                yield Static("Golden Image Username (WinRM)")
                yield Input(str(get_in(self.group_vars, ["windows", "goldimage", "username"]) or ""), id="gold_user", classes="field")
                yield Static("Golden Image Password")
                yield Input(str(get_in(self.group_vars, ["windows", "goldimage", "password"]) or ""), password=True, id="gold_pass", classes="field")
                with Horizontal(classes="stage-nav"):
                    yield Button("Back", id="back_golden", classes="nav-button")
                    yield Button("Next", id="next_golden", variant="primary", classes="nav-button")
            with VerticalScroll(id="stage-builder", classes="stage"):
                yield Static("Stage 5: WinPE builder VM running + WinRM credential validation.")
                yield Static(
                    "What this VM is for: this is the Windows build workstation that creates deployment artifacts "
                    "(for example, WinPE boot files and related build outputs) used by the deployer workflow. "
                    "This can be any windows machine that is not the gold image."
                )
                yield Static(
                    "What it must have: it must be powered on, reachable from this controller, and allow WinRM "
                    "authentication with the credentials below."
                )
                yield Static(
                    "Where it fits: after Proxmox/golden-image validation and before final deployer-network setup; "
                    "if this stage fails, artifact build and later deployment steps cannot proceed."
                )
                yield Static("WinPE Builder VMID (must be running)")
                yield Input(str(get_in(self.group_vars, ["windows", "winpe_builder", "vmid"]) or ""), id="builder_vmid", classes="field")
                yield Static("WinPE Builder IP (WinRM)")
                yield Input(str(get_in(self.group_vars, ["windows", "winpe_builder", "ip"]) or ""), id="builder_ip", classes="field")
                yield Static("WinPE Builder Username (WinRM)")
                yield Input(str(get_in(self.group_vars, ["windows", "winpe_builder", "username"]) or ""), id="builder_user", classes="field")
                yield Static("WinPE Builder Password")
                yield Input(str(get_in(self.group_vars, ["windows", "winpe_builder", "password"]) or ""), password=True, id="builder_pass", classes="field")
                with Horizontal(classes="stage-nav"):
                    yield Button("Back", id="back_builder", classes="nav-button")
                    yield Button("Next", id="next_builder", variant="primary", classes="nav-button")
            with VerticalScroll(id="stage-network", classes="stage"):
                yield Static("Stage 6: Deployer networking + DHCP safety checks + inventory write + bootstrap.")
                yield Static("The deployer LXC is the container you will export and use to deploy windows workstations elsewhere")
                yield Static("Deployer LXC VMID (must be unused)")
                yield Input(str(get_in(self.group_vars, ["deployer", "lxc", "vmid"]) or ""), id="dep_vmid", classes="field")
                yield Static("Deployer LXC Hostname")
                yield Input(str(get_in(self.group_vars, ["deployer", "lxc", "hostname"]) or ""), id="dep_hostname", classes="field")
                yield Static("Deployer LXC IP")
                yield Input(str(get_in(self.group_vars, ["deployer", "lxc", "ip"]) or ""), id="dep_ip", classes="field")
                yield Static("Deployer CIDR Prefix (example 24)")
                yield Input(str(get_in(self.group_vars, ["deployer", "lxc", "cidr_prefix"]) or ""), id="dep_prefix", classes="field")
                yield Static("Default Gateway (must be reachable)")
                yield Input(str(get_in(self.group_vars, ["deployer", "lxc", "gateway"]) or ""), id="dep_gateway", classes="field")
                yield Static("Deployer Bridge (live list from Proxmox after Stage 1)")
                yield PersistentSelect(options=[(b, b) for b in self.bridges], value=self.bridges[0], id="dep_bridge", classes="field")
                yield Static("Deployer MAC Address")
                yield Input(str(get_in(self.group_vars, ["deployer", "lxc", "hwaddr"]) or ""), id="dep_mac", classes="field")
                yield Static("Deployer LXC password (used for LXC root access and helper automation)")
                yield Input(str(get_in(self.group_vars, ["deployer", "lxc", "password"]) or ""), password=True, id="dep_password", classes="field")
                yield Static("Deployer Disk Size (GB) - must fit your deploy.wim plus growth margin")
                yield Input(str(get_in(self.group_vars, ["deployer", "lxc", "rootfs_gb"]) or ""), id="dep_disk_gb", classes="field")
                yield Static("DHCP Range Start")
                yield Input(str(get_in(self.group_vars, ["deployer", "network", "dhcp_start"]) or ""), id="dep_dhcp_start", classes="field")
                yield Static("DHCP Range End")
                yield Input(str(get_in(self.group_vars, ["deployer", "network", "dhcp_end"]) or ""), id="dep_dhcp_end", classes="field")
                yield Static("DNS Server for DHCP clients")
                yield Input(str(get_in(self.group_vars, ["deployer", "network", "dns_server"]) or ""), id="dep_dns", classes="field")
                yield Static("Auto reboot after successful deployment? (on target workstation VM in WinPE)")
                yield PersistentSelect(options=[("Yes, reboot target workstation automatically", "true"), ("No, keep target workstation in WinPE after apply", "false")], value="true" if bool(get_in(self.group_vars, ["windows", "deploy", "auto_reboot"])) else "false", id="dep_auto_reboot", classes="field")
                with Horizontal(classes="stage-nav"):
                    yield Button("Back", id="back_network", classes="nav-button")
                    yield Button("Run Setup", id="finish_setup_btn", variant="success", classes="nav-button")
            with Vertical(id="stage-deploy", classes="stage"):
                with Horizontal(classes="deploy-center"):
                    yield Button("DEPLOY", id="deploy_now")

        yield Log(id="log", highlight=True, auto_scroll=True)
        yield Footer()

    def on_mount(self) -> None:
        self.append_log("Wizard started. Complete each stage and click validate.")
        self._refresh_controls()
        self._update_progress()
        self.set_focus(self.query_one("#px_host", Input))

    def append_log(self, message: str) -> None:
        self.query_one("#log", Log).write_line(message)

    def set_status(self, message: str) -> None:
        self.query_one("#status", Static).update(message)

    def switch_stage(self, stage_id: str, stage_label: str) -> None:
        self.query_one("#main-switcher", ContentSwitcher).current = stage_id
        self.current_stage = stage_id
        self.set_status(stage_label)
        self._refresh_controls()
        self._update_progress()
        next_target = self._stage_focusables()[0] if self._stage_focusables() else None
        if next_target is not None:
            self.set_focus(next_target)
            if isinstance(next_target, Select):
                # Keep dropdown closed on stage switch; user must explicitly open it.
                next_target.expanded = False

    def _update_progress(self) -> None:
        stage_map = {
            "stage-proxmox-auth": 1,
            "stage-proxmox-node": 2,
            "stage-proxmox-storage": 3,
            "stage-golden": 4,
            "stage-builder": 5,
            "stage-network": 6,
            "stage-deploy": 7,
        }
        progress = self.query_one("#stage_progress", ProgressBar)
        progress.update(progress=stage_map.get(self.current_stage, 1))

    def _refresh_controls(self) -> None:
        legend = self.query_one("#control_legend", Static)
        armed_suffix = " | Quit: Esc then q" if not self.quit_armed else " | Quit armed: press q now"
        if self.current_stage == "stage-proxmox-auth":
            legend.update(f"Now: fill fields, then highlight Next button and press Enter.{armed_suffix}")
        elif self.current_stage == "stage-proxmox-node":
            legend.update(f"Now: open node dropdown with Enter, choose with arrows, Enter to accept, then Enter on Next button.{armed_suffix}")
        elif self.current_stage == "stage-proxmox-storage":
            legend.update(f"Now: choose storage/template via dropdowns, then highlight Next button and press Enter.{armed_suffix}")
        elif self.current_stage == "stage-golden":
            legend.update(f"Now: fill fields, then highlight Next button and press Enter. Use Back button to return.{armed_suffix}")
        elif self.current_stage == "stage-builder":
            legend.update(f"Now: fill fields, then highlight Next button and press Enter. Use Back button to return.{armed_suffix}")
        elif self.current_stage == "stage-network":
            legend.update(f"Now: highlight Run Setup button and press Enter to run validation + bootstrap.{armed_suffix}")
        else:
            legend.update(f"Now: highlight DEPLOY and press Enter to exit setup and start run-full-deploy.sh.{armed_suffix}")

    def _stage_focusables(self) -> list[Input | Select | Button]:
        stage = self.query_one(f"#{self.current_stage}")
        widgets: list[Input | Select | Button] = []
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

    def _resolve_focus_owner(self, focused: object, fields: list[Input | Select | Button]) -> Input | Select | Button | None:
        if focused in fields:
            return focused  # type: ignore[return-value]
        node = focused
        # If focus is in a child (e.g., Select overlay), walk up to an owning focusable.
        while node is not None and hasattr(node, "parent"):
            node = getattr(node, "parent")
            if node in fields:
                return node  # type: ignore[return-value]
        return None

    def _ensure_focus_visible_target(self) -> None:
        fields = self._stage_focusables()
        if not fields:
            return
        owner = self._resolve_focus_owner(self.focused, fields)
        if owner is None:
            self.set_focus(fields[0])

    def action_focus_next_field(self) -> None:
        if self.current_stage == "stage-deploy":
            self.set_focus(self.query_one("#deploy_now", Button))
            return
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
        if self.current_stage == "stage-deploy":
            self.set_focus(self.query_one("#deploy_now", Button))
            return
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
        if self.current_stage == "stage-deploy":
            self.set_focus(self.query_one("#deploy_now", Button))
            return
        buttons = self._stage_buttons()
        if len(buttons) < 2:
            return
        current = self.focused
        if current in buttons:
            idx = buttons.index(current)
            self.set_focus(buttons[(idx + 1) % len(buttons)])

    def action_focus_button_left(self) -> None:
        if self.current_stage == "stage-deploy":
            self.set_focus(self.query_one("#deploy_now", Button))
            return
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

    def _input(self, widget_id: str) -> str:
        return self.query_one(f"#{widget_id}", Input).value.strip()

    def _select(self, widget_id: str) -> str:
        value = self.query_one(f"#{widget_id}", Select).value
        return "" if value is None else str(value)

    def _must_ipv4(self, value: str, label: str) -> None:
        try:
            ipaddress.IPv4Address(value)
        except ValueError as exc:
            raise RuntimeError(f"{label} is not a valid IPv4 address: {value}") from exc

    def _run(self, argv: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
        return subprocess.run(argv, cwd=str(cwd or ROOT), text=True, capture_output=True, check=False)

    def _connect_proxmox_api(self, host: str, user: str, password: str, skip_tls: bool) -> ProxmoxAPI:
        realm_user = user if "@" in user else f"{user}@pam"
        try:
            api = ProxmoxAPI(host, user=realm_user, password=password, verify_ssl=not skip_tls)
            _ = api.version.get()
            return api
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"Proxmox API login failed for {realm_user}@{host}: {exc}") from exc

    def _tcp_open(self, host: str, port: int, timeout_sec: float = 2.0) -> bool:
        try:
            with socket.create_connection((host, port), timeout=timeout_sec):
                return True
        except OSError:
            return False

    def _ping_host(self, host: str) -> bool:
        ping = self._run(["ping", "-c", "1", "-W", "2", host], cwd=ROOT)
        if ping.returncode == 0:
            return True
        # Some environments block raw ICMP in unprivileged shells; fallback to TCP probes.
        return self._tcp_open(host, 22) or self._tcp_open(host, 8006)

    def _validate_winrm_auth(self, ip: str, user: str, password: str) -> None:
        endpoint = f"http://{ip}:5985/wsman"
        session = winrm.Session(endpoint, auth=(user, password), transport="ntlm", server_cert_validation="ignore")
        response = session.run_ps("Write-Output 'WINRM_OK'")
        if response.status_code != 0:
            stderr = response.std_err.decode("utf-8", errors="ignore").strip()
            raise RuntimeError(f"WinRM authentication failed for {user}@{ip}. {stderr}")

    def _validate_vmid_running(self, api: ProxmoxAPI, node: str, vmid: int) -> str:
        # Validate VM presence/status cluster-wide; do not assume all VMs are on the configured node.
        try:
            resources = api.cluster.resources.get(type="vm")
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"Could not query cluster VM resources while checking VMID {vmid}: {exc}") from exc

        vm = next((item for item in resources if int(item.get("vmid", -1)) == vmid and str(item.get("type")) == "qemu"), None)
        if vm is None:
            raise RuntimeError(f"VMID {vmid} was not found in cluster qemu resources.")

        vm_node = str(vm.get("node", "unknown"))
        vm_status = str(vm.get("status", "unknown"))
        if vm_status != "running":
            raise RuntimeError(f"VMID {vmid} is not running (node: {vm_node}, state: {vm_status}).")
        return vm_node

    def _list_bridges(self, api: ProxmoxAPI, node: str) -> list[str]:
        try:
            networks = api.nodes(node).network.get()
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"Failed to list node network interfaces via Proxmox API: {exc}") from exc
        bridges = [str(n.get("iface")) for n in networks if str(n.get("type", "")).lower() == "bridge" and n.get("iface")]
        if not bridges:
            raise RuntimeError("No network bridges were returned from Proxmox host.")
        return bridges

    def _ensure_ubuntu_template(self, api: ProxmoxAPI, node: str, template_storage: str, preferred_name: str) -> str:
        try:
            rows = api.nodes(node).storage(template_storage).content.get(content="vztmpl")
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"Unable to list templates in storage {template_storage} via API: {exc}") from exc
        names: list[str] = []
        for row in rows:
            volid = str(row.get("volid", ""))
            if ":" in volid:
                names.append(volid.split(":", 1)[1].replace("vztmpl/", ""))

        chosen = preferred_name
        if chosen not in names:
            try:
                available_rows = api.nodes(node).aplinfo.get(section="system", storage=template_storage)
            except Exception as exc:  # noqa: BLE001
                raise RuntimeError(f"Unable to query available templates via API: {exc}") from exc
            ubuntu_candidates = [str(r.get("template", "")) for r in available_rows if str(r.get("template", "")).startswith("ubuntu-24.04-standard")]
            if not ubuntu_candidates:
                raise RuntimeError("Could not find an ubuntu-24.04-standard template in Proxmox API template catalog.")
            chosen = sorted(ubuntu_candidates)[-1]
            self.append_log(f"Preferred template not found; selected latest available: {chosen}")
            try:
                _ = api.nodes(node).aplinfo.post(storage=template_storage, template=chosen)
            except Exception as exc:  # noqa: BLE001
                raise RuntimeError(
                    f"Template download via API failed for {chosen}: {exc}. "
                    f"You can manually pre-download and rerun setup."
                ) from exc
        return chosen

    def _validate_storage_and_node(self, api: ProxmoxAPI, node: str, storage_pool: str, template_storage: str) -> None:
        try:
            nodes_info = api.nodes.get()
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"Could not query Proxmox nodes via API: {exc}") from exc
        nodes = [str(item.get("node", "")) for item in nodes_info]
        if node not in nodes:
            raise RuntimeError(f"Configured node '{node}' not found in Proxmox nodes: {nodes}")

        try:
            storages_info = api.storage.get()
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"Could not query Proxmox storages via API: {exc}") from exc
        storages = [str(item.get("storage", "")) for item in storages_info]
        missing = [name for name in [storage_pool, template_storage] if name not in storages]
        if missing:
            raise RuntimeError(f"Storage validation failed. Missing storages: {missing}. Available: {storages}")

    def _validate_dhcp_unused(self, start_ip: str, end_ip: str) -> None:
        start = ipaddress.IPv4Address(start_ip)
        end = ipaddress.IPv4Address(end_ip)
        if int(end) < int(start):
            raise RuntimeError("DHCP range end must be greater than or equal to range start.")
        if (int(end) - int(start)) > 128:
            raise RuntimeError("DHCP validation range is too large (>129 IPs). Use a tighter range.")

        used: list[str] = []
        for ip_int in range(int(start), int(end) + 1):
            ip = str(ipaddress.IPv4Address(ip_int))
            ping = self._run(["ping", "-c", "1", "-W", "1", ip], cwd=ROOT)
            if ping.returncode == 0:
                used.append(ip)
        if used:
            raise RuntimeError(f"DHCP range contains addresses that appear in use: {', '.join(used)}")

    def _persist_and_bootstrap(self) -> None:
        gv_backup = backup_file(GROUP_VARS_PATH)
        hosts_backup = backup_file(HOSTS_PATH)
        dump_yaml(GROUP_VARS_PATH, self.group_vars)
        dump_yaml(HOSTS_PATH, self.hosts)
        self.append_log(f"Inventory files updated. Backups: {gv_backup.name}, {hosts_backup.name}")
        self.append_log("Running bootstrap-controller.sh...")
        run = self._run([str(BOOTSTRAP_PATH)], cwd=ROOT)
        if run.returncode != 0:
            raise RuntimeError(f"Bootstrap failed.\n{run.stdout}\n{run.stderr}")
        self.append_log("Bootstrap completed successfully.")
        self.append_log("Run the full deployment workflow with:")
        self.append_log("  ./scripts/run-full-deploy.sh")
        self.append_log("Alternative:")
        self.append_log("  ansible-playbook -i inventories/windows-deployer/hosts.yml playbooks/site.yml")
        self.set_status("Stage 6 complete. Continue to Stage 7 to deploy.")
        self.switch_stage("stage-deploy", "Stage 7/7: Press DEPLOY to exit and start full deployment.")

    @on(Button.Pressed, "#next_auth")
    def on_next_auth(self) -> None:
        self.validate_proxmox_auth_stage()

    @on(Button.Pressed, "#back_node")
    def on_back_node(self) -> None:
        self.back_to_proxmox_auth()

    @on(Button.Pressed, "#next_node")
    def on_next_node(self) -> None:
        self.validate_proxmox_node_stage()

    @on(Button.Pressed, "#back_storage")
    def on_back_storage(self) -> None:
        self.back_to_proxmox_node()

    @on(Button.Pressed, "#next_storage")
    def on_next_storage(self) -> None:
        self.validate_proxmox_stage()

    @on(Button.Pressed, "#back_golden")
    def on_back_golden(self) -> None:
        self.back_to_proxmox_storage()

    @on(Button.Pressed, "#next_golden")
    def on_next_golden(self) -> None:
        self.validate_golden_stage()

    @on(Button.Pressed, "#back_builder")
    def on_back_builder(self) -> None:
        self.back_to_golden()

    @on(Button.Pressed, "#next_builder")
    def on_next_builder(self) -> None:
        self.validate_builder_stage()

    @on(Button.Pressed, "#back_network")
    def on_back_network(self) -> None:
        self.back_to_builder()

    @on(Button.Pressed, "#finish_setup_btn")
    def on_finish_setup_btn(self) -> None:
        self.finish_setup()

    @on(Button.Pressed, "#deploy_now")
    def on_deploy_now(self) -> None:
        self.launch_deploy_after_exit = True
        self.append_log("DEPLOY confirmed. Exiting setup and starting run-full-deploy.sh...")
        self.exit()

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
        # is expanded (in that case, let the Select consume arrows).
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

        # Enter behavior is explicit: users trigger stage changes by focusing
        # the Back/Next buttons and pressing Enter on those buttons.

    def validate_proxmox_auth_stage(self) -> None:
        try:
            host = self._input("px_host")
            ssh_user = self._input("px_ssh_user")
            ssh_pass = self._input("px_ssh_pass")
            skip_tls = self._select("px_skip_tls") == "true"
            if not host or not ssh_user or not ssh_pass:
                raise RuntimeError("Host, username, and password are required.")

            if not self._ping_host(host):
                raise RuntimeError(f"Proxmox host {host} is not pingable/reachable from the controller.")
            self.append_log(f"Proxmox host {host} reachability check passed.")

            if not self._tcp_open(host, 22):
                raise RuntimeError(f"Proxmox host {host} is not reachable on TCP/22 (SSH).")
            if not self._tcp_open(host, 8006):
                raise RuntimeError(f"Proxmox host {host} is not reachable on TCP/8006 (API).")
            self.append_log(f"Proxmox API endpoint reachability check passed for {host}:8006.")

            api = self._connect_proxmox_api(host, ssh_user, ssh_pass, skip_tls)
            self.append_log("Proxmox API credentials validated.")

            nodes_info = api.nodes.get()
            self.available_nodes = sorted({str(item.get("node", "")).strip() for item in nodes_info if str(item.get("node", "")).strip()})
            if not self.available_nodes:
                raise RuntimeError("No nodes were returned from Proxmox API.")

            node_select = self.query_one("#px_node", Select)
            node_select.set_options([(n, n) for n in self.available_nodes])
            preferred_node = str(get_in(self.group_vars, ["proxmox", "node"]) or "")
            node_select.value = preferred_node if preferred_node in self.available_nodes else self.available_nodes[0]

            self.append_log(f"Discovered nodes: {', '.join(self.available_nodes)}")
            self.set_status("Stage 1 passed. Continue to Stage 2.")
            self.switch_stage("stage-proxmox-node", "Stage 2/7: Select Proxmox node.")
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 1 failed: {exc}")
            self.set_status("Stage 1 failed. Fix fields and try again.")

    def validate_proxmox_node_stage(self) -> None:
        try:
            host = self._input("px_host")
            ssh_user = self._input("px_ssh_user")
            ssh_pass = self._input("px_ssh_pass")
            node = self._select("px_node")
            skip_tls = self._select("px_skip_tls") == "true"
            if not host or not ssh_user or not ssh_pass or not node:
                raise RuntimeError("Host, username, password, and node are required.")

            api = self._connect_proxmox_api(host, ssh_user, ssh_pass, skip_tls)
            storages_info = api.nodes(node).storage.get()
            self.available_storages = sorted({str(item.get("storage", "")).strip() for item in storages_info if str(item.get("storage", "")).strip()})
            if not self.available_storages:
                raise RuntimeError(f"No storages were returned for node {node}.")

            storage_select = self.query_one("#px_storage_pool", Select)
            storage_select.set_options([(s, s) for s in self.available_storages])
            preferred_storage = str(get_in(self.group_vars, ["proxmox", "defaults", "storage_pool"]) or "")
            storage_select.value = preferred_storage if preferred_storage in self.available_storages else self.available_storages[0]

            template_storage_select = self.query_one("#px_template_storage", Select)
            template_storage_select.set_options([(s, s) for s in self.available_storages])
            preferred_template_storage = str(get_in(self.group_vars, ["proxmox", "defaults", "template_storage"]) or "")
            template_storage_select.value = preferred_template_storage if preferred_template_storage in self.available_storages else self.available_storages[0]

            self.append_log(f"Node selected: {node}")
            self.append_log(f"Node {node} storages: {', '.join(self.available_storages)}")
            self.set_status("Stage 2 passed. Continue to Stage 3.")
            self.switch_stage("stage-proxmox-storage", "Stage 3/7: Select and validate storage/template values.")
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 2 failed: {exc}")
            self.set_status("Stage 2 failed. Fix fields and try again.")

    def validate_proxmox_stage(self) -> None:
        try:
            host = self._input("px_host")
            ssh_user = self._input("px_ssh_user")
            ssh_pass = self._input("px_ssh_pass")
            node = self._select("px_node")
            storage_pool = self._select("px_storage_pool")
            template_storage = self._select("px_template_storage")
            skip_tls = self._select("px_skip_tls") == "true"
            if not host or not ssh_user or not ssh_pass or not node or not storage_pool or not template_storage:
                raise RuntimeError("All Proxmox fields are required.")

            api = self._connect_proxmox_api(host, ssh_user, ssh_pass, skip_tls)
            self.append_log("Proxmox API credentials revalidated.")

            self._validate_storage_and_node(api, node, storage_pool, template_storage)
            self.append_log("Node and storage validation succeeded.")

            current_template = str(get_in(self.group_vars, ["proxmox", "defaults", "ostemplate"]) or "")
            template_name = self._ensure_ubuntu_template(api, node, template_storage, current_template)
            self.selected_template_name = template_name
            self.append_log(f"LXC template ensured: {template_name}")
            self.append_log("Proxmox API token provisioning is handled by Ansible during deployment.")

            self.bridges = self._list_bridges(api, node)
            bridge_select = self.query_one("#dep_bridge", Select)
            bridge_select.set_options([(b, b) for b in self.bridges])
            if self.bridges:
                bridge_select.value = self.bridges[0]
            self.append_log(f"Discovered bridges: {', '.join(self.bridges)}")

            self.set_status("Stage 3 passed. Continue to Stage 4.")
            self.switch_stage("stage-golden", "Stage 4/7: Validate golden image VM over WinRM.")
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 3 failed: {exc}")
            self.set_status("Stage 3 failed. Fix fields and try again.")

    def back_to_proxmox_auth(self) -> None:
        self.switch_stage("stage-proxmox-auth", "Stage 1/7: Validate Proxmox credentials.")

    def back_to_proxmox_node(self) -> None:
        self.switch_stage("stage-proxmox-node", "Stage 2/7: Select Proxmox node.")

    def back_to_proxmox_storage(self) -> None:
        self.switch_stage("stage-proxmox-storage", "Stage 3/7: Select node-scoped storage/template values.")

    def validate_golden_stage(self) -> None:
        try:
            vmid = int(self._input("gold_vmid"))
            ip = self._input("gold_ip")
            user = self._input("gold_user")
            password = self._input("gold_pass")
            host = self._input("px_host")
            ssh_user = self._input("px_ssh_user")
            ssh_pass = self._input("px_ssh_pass")
            node = self._select("px_node")
            skip_tls = self._select("px_skip_tls") == "true"

            self._must_ipv4(ip, "Golden image IP")
            api = self._connect_proxmox_api(host, ssh_user, ssh_pass, skip_tls)
            vm_node = self._validate_vmid_running(api, node, vmid)
            if vm_node != node:
                self.append_log(f"Golden image VMID {vmid} is running on node {vm_node} (configured node is {node}).")
            else:
                self.append_log(f"Golden image VMID {vmid} is running.")

            if not self._tcp_open(ip, 5985):
                raise RuntimeError(f"WinRM port 5985 is not open on golden image VM at {ip}.")
            self.append_log("Golden image WinRM port 5985 reachable.")

            self._validate_winrm_auth(ip, user, password)
            self.append_log("Golden image WinRM credentials validated successfully.")

            self.set_status("Stage 4 passed. Continue to Stage 5.")
            self.switch_stage("stage-builder", "Stage 5/7: Validate WinPE builder VM over WinRM.")
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 4 failed: {exc}")
            self.set_status("Stage 4 failed. Fix fields and try again.")

    def back_to_golden(self) -> None:
        self.switch_stage("stage-golden", "Stage 4/7: Validate golden image VM over WinRM.")

    def validate_builder_stage(self) -> None:
        try:
            vmid = int(self._input("builder_vmid"))
            ip = self._input("builder_ip")
            user = self._input("builder_user")
            password = self._input("builder_pass")
            host = self._input("px_host")
            ssh_user = self._input("px_ssh_user")
            ssh_pass = self._input("px_ssh_pass")
            node = self._select("px_node")
            skip_tls = self._select("px_skip_tls") == "true"

            self._must_ipv4(ip, "Builder IP")
            api = self._connect_proxmox_api(host, ssh_user, ssh_pass, skip_tls)
            vm_node = self._validate_vmid_running(api, node, vmid)
            if vm_node != node:
                self.append_log(f"WinPE builder VMID {vmid} is running on node {vm_node} (configured node is {node}).")
            else:
                self.append_log(f"WinPE builder VMID {vmid} is running.")

            if not self._tcp_open(ip, 5985):
                raise RuntimeError(f"WinRM port 5985 is not open on WinPE builder VM at {ip}.")
            self.append_log("WinPE builder WinRM port 5985 reachable.")

            self._validate_winrm_auth(ip, user, password)
            self.append_log("WinPE builder WinRM credentials validated successfully.")

            self.set_status("Stage 5 passed. Continue to Stage 6.")
            self.switch_stage("stage-network", "Stage 6/7: Validate deployer networking, write files, run bootstrap.")
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 5 failed: {exc}")
            self.set_status("Stage 5 failed. Fix fields and try again.")

    def back_to_builder(self) -> None:
        self.switch_stage("stage-builder", "Stage 5/7: Validate WinPE builder VM over WinRM.")

    def finish_setup(self) -> None:
        try:
            host = self._input("px_host")
            ssh_user = self._input("px_ssh_user")
            ssh_pass = self._input("px_ssh_pass")
            storage_pool = self._select("px_storage_pool")
            template_storage = self._select("px_template_storage")
            node = self._select("px_node")
            skip_tls = self._select("px_skip_tls") == "true"
            dep_vmid = int(self._input("dep_vmid"))
            dep_host = self._input("dep_hostname")
            dep_ip = self._input("dep_ip")
            dep_prefix = int(self._input("dep_prefix"))
            dep_gateway = self._input("dep_gateway")
            dep_bridge = self._select("dep_bridge")
            dep_mac = self._input("dep_mac")
            dep_password = self._input("dep_password")
            dep_disk_gb = int(self._input("dep_disk_gb"))
            dep_dhcp_start = self._input("dep_dhcp_start")
            dep_dhcp_end = self._input("dep_dhcp_end")
            dep_dns = self._input("dep_dns")
            auto_reboot = self._select("dep_auto_reboot") == "true"
            api = self._connect_proxmox_api(host, ssh_user, ssh_pass, skip_tls)

            gold_vmid = int(self._input("gold_vmid"))
            gold_ip = self._input("gold_ip")
            gold_user = self._input("gold_user")
            gold_pass = self._input("gold_pass")
            builder_vmid = int(self._input("builder_vmid"))
            builder_ip = self._input("builder_ip")
            builder_user = self._input("builder_user")
            builder_pass = self._input("builder_pass")

            for label, ip in [
                ("Deployer IP", dep_ip),
                ("Gateway", dep_gateway),
                ("DHCP start", dep_dhcp_start),
                ("DHCP end", dep_dhcp_end),
                ("DNS server", dep_dns),
            ]:
                self._must_ipv4(ip, label)
            if not dep_host or not dep_bridge or not dep_mac or not dep_password:
                raise RuntimeError("All deployer fields are required.")

            if dep_disk_gb < 80:
                raise RuntimeError("Deployer disk size is too small. Use at least 80 GB so deploy.wim and logs fit safely.")
            self.append_log("Deployer disk size check passed (>= 80 GB).")

            if not self._ping_host(dep_gateway):
                raise RuntimeError(f"Gateway {dep_gateway} does not appear reachable from the setup host.")
            self.append_log(f"Gateway {dep_gateway} reachability check passed.")

            existing_vmids = {int(item.get("vmid")) for item in api.cluster.resources.get(type="vm") if item.get("vmid") is not None}
            if dep_vmid in existing_vmids:
                raise RuntimeError(f"Deployer VMID {dep_vmid} is already in use. Choose an unused VMID.")
            self.append_log(f"Deployer VMID {dep_vmid} appears unused.")

            network = ipaddress.IPv4Network(f"{dep_ip}/{dep_prefix}", strict=False)
            if ipaddress.IPv4Address(dep_gateway) not in network:
                raise RuntimeError(f"Gateway {dep_gateway} is outside deployer subnet {network}.")
            if ipaddress.IPv4Address(dep_dhcp_start) not in network or ipaddress.IPv4Address(dep_dhcp_end) not in network:
                raise RuntimeError(f"DHCP range must be inside deployer subnet {network}.")
            self.append_log(f"Subnet consistency checks passed ({network}).")

            self._validate_dhcp_unused(dep_dhcp_start, dep_dhcp_end)
            self.append_log("DHCP range appears unused (ping/neighbor checks passed).")

            template_name = self.selected_template_name or self._ensure_ubuntu_template(api, node, template_storage, str(get_in(self.group_vars, ["proxmox", "defaults", "ostemplate"]) or ""))

            # Write all updates.
            set_in(self.group_vars, ["proxmox", "host"], host)
            set_in(self.group_vars, ["proxmox", "user"], ssh_user)
            set_in(self.group_vars, ["proxmox", "root_password"], ssh_pass)
            set_in(self.group_vars, ["proxmox", "node"], node)
            set_in(self.group_vars, ["proxmox", "insecure_skip_tls_verify"], skip_tls)
            # Token fields are intentionally left unchanged here.
            # Token lifecycle is owned by Ansible playbooks during deployment.
            set_in(self.group_vars, ["proxmox", "defaults", "storage_pool"], storage_pool)
            set_in(self.group_vars, ["proxmox", "defaults", "template_storage"], template_storage)
            set_in(self.group_vars, ["proxmox", "defaults", "ostemplate"], template_name)
            set_in(self.group_vars, ["windows", "goldimage", "vmid"], gold_vmid)
            set_in(self.group_vars, ["windows", "goldimage", "ip"], gold_ip)
            set_in(self.group_vars, ["windows", "goldimage", "username"], gold_user)
            set_in(self.group_vars, ["windows", "goldimage", "password"], gold_pass)
            set_in(self.group_vars, ["windows", "winpe_builder", "vmid"], builder_vmid)
            set_in(self.group_vars, ["windows", "winpe_builder", "ip"], builder_ip)
            set_in(self.group_vars, ["windows", "winpe_builder", "username"], builder_user)
            set_in(self.group_vars, ["windows", "winpe_builder", "password"], builder_pass)
            set_in(self.group_vars, ["deployer", "lxc", "vmid"], dep_vmid)
            set_in(self.group_vars, ["deployer", "lxc", "hostname"], dep_host)
            set_in(self.group_vars, ["deployer", "lxc", "ip"], dep_ip)
            set_in(self.group_vars, ["deployer", "lxc", "cidr"], f"{dep_ip}/{dep_prefix}")
            set_in(self.group_vars, ["deployer", "lxc", "cidr_prefix"], dep_prefix)
            set_in(self.group_vars, ["deployer", "lxc", "gateway"], dep_gateway)
            set_in(self.group_vars, ["deployer", "lxc", "bridge"], dep_bridge)
            set_in(self.group_vars, ["deployer", "lxc", "hwaddr"], dep_mac)
            set_in(self.group_vars, ["deployer", "lxc", "password"], dep_password)
            set_in(self.group_vars, ["deployer", "lxc", "rootfs_gb"], dep_disk_gb)
            set_in(self.group_vars, ["deployer", "lxc", "disk"], f"{storage_pool}:{dep_disk_gb}")
            set_in(self.group_vars, ["deployer", "lxc", "storage"], storage_pool)
            set_in(self.group_vars, ["deployer", "network", "server_ip"], dep_ip)
            set_in(self.group_vars, ["deployer", "network", "dhcp_start"], dep_dhcp_start)
            set_in(self.group_vars, ["deployer", "network", "dhcp_end"], dep_dhcp_end)
            set_in(self.group_vars, ["deployer", "network", "dns_server"], dep_dns)
            set_in(self.group_vars, ["windows", "deploy", "auto_reboot"], auto_reboot)

            set_in(self.hosts, ["all", "children", "proxmox_nodes", "hosts", "pve", "ansible_host"], host)
            set_in(self.hosts, ["all", "children", "proxmox_nodes", "hosts", "pve", "ansible_user"], ssh_user)
            set_in(self.hosts, ["all", "children", "proxmox_nodes", "hosts", "pve", "ansible_ssh_pass"], ssh_pass)
            set_in(self.hosts, ["all", "children", "goldimage", "hosts", "goldimage_vm", "ansible_host"], gold_ip)
            set_in(self.hosts, ["all", "children", "goldimage", "hosts", "goldimage_vm", "ansible_user"], gold_user)
            set_in(self.hosts, ["all", "children", "goldimage", "hosts", "goldimage_vm", "ansible_password"], gold_pass)
            set_in(self.hosts, ["all", "children", "winpe_builder", "hosts", "winserv2025", "ansible_host"], builder_ip)
            set_in(self.hosts, ["all", "children", "winpe_builder", "hosts", "winserv2025", "ansible_user"], builder_user)
            set_in(self.hosts, ["all", "children", "winpe_builder", "hosts", "winserv2025", "ansible_password"], builder_pass)
            set_in(self.hosts, ["all", "children", "deployer_lxc", "hosts", "win-deploy-lxc", "ansible_host"], host)
            set_in(self.hosts, ["all", "children", "deployer_lxc", "hosts", "win-deploy-lxc", "ansible_user"], ssh_user)
            set_in(self.hosts, ["all", "children", "deployer_lxc", "hosts", "win-deploy-lxc", "ansible_password"], ssh_pass)
            set_in(self.hosts, ["all", "children", "deployer_lxc", "hosts", "win-deploy-lxc", "proxmox_vmid"], dep_vmid)

            self._persist_and_bootstrap()
        except Exception as exc:  # noqa: BLE001
            self.append_log(f"[ERROR] Stage 6 failed: {exc}")
            self.set_status("Stage 6 failed. Fix values and retry.")


def main() -> int:
    app = SetupApp()
    app.run()
    if app.launch_deploy_after_exit:
        completed = subprocess.run(["bash", str(RUN_FULL_DEPLOY_PATH)], cwd=str(ROOT), check=False)
        return int(completed.returncode)
    return 0


if __name__ == "__main__":
    sys.exit(main())
