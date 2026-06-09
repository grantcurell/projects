#!/usr/bin/env python3
"""Non-interactive offline deployer configuration (runs ON the deployer LXC).

This is the headless equivalent of the offline setup TUI's apply step. It writes
the same artifacts the TUI would (`domain.json`, `naming.json`, the `[join]`
credential, and the dnsmasq PXE/DNS config) from values supplied on the command
line, then restarts services. It is used by the automated offline test to bring a
freshly-restored deployer to a known-good state without operator interaction.

The render logic is intentionally identical to scripts/offline-deployer-tui.py
(`_write_site_config`, `_render_join_credential`, `_render_dnsmasq`) so the
automated path and the interactive path produce byte-compatible output.

The join-account password is read from the JOIN_PASS environment variable only,
never from argv.
"""
from __future__ import annotations

import argparse
import ipaddress
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG_PATH = "/etc/windows-deployer/offline-config.yml"


def load_offline_config() -> dict[str, Any]:
    path = Path(os.environ.get("WINDEPLOY_OFFLINE_CONFIG", DEFAULT_CONFIG_PATH))
    if not path.exists():
        raise RuntimeError(
            f"Offline config {path} not found. The LXC role installs it during the online build."
        )
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise RuntimeError(f"Invalid offline config in {path}.")
    required = ["offline_hostname", "offline_hostname_fqdn", "site_path", "join_secret_path"]
    missing = [k for k in required if not data.get(k)]
    if missing:
        raise RuntimeError(f"Offline config is missing required keys (no defaults): {missing}")
    return data


def write_site_config(
    site_path: Path,
    enabled: bool,
    domain_fqdn: str,
    netbios: str,
    ou_path: str,
    domain_controller: str,
    domain_controller_ip: str,
    dns_servers: list[str],
    naming_source: str,
    naming_max_length: int,
) -> None:
    site_path.mkdir(parents=True, exist_ok=True)
    domain = {
        "enabled": enabled,
        "domain_fqdn": domain_fqdn,
        "domain_netbios": netbios,
        "ou_path": ou_path,
        "domain_controller": domain_controller,
        "domain_controller_ip": domain_controller_ip,
        "dns_servers": dns_servers or [],
    }
    (site_path / "domain.json").write_text(json.dumps(domain, indent=2) + "\n", encoding="utf-8")
    naming = {"source": naming_source, "max_length": naming_max_length}
    (site_path / "naming.json").write_text(json.dumps(naming, indent=2) + "\n", encoding="utf-8")


def render_join_credential(join_path: Path, user: str, password: str) -> None:
    join_path.mkdir(parents=True, exist_ok=True)
    os.chmod(join_path, 0o700)
    cred = {"username": user, "password": password}
    cred_file = join_path / "join.cred"
    cred_file.write_text(json.dumps(cred) + "\n", encoding="utf-8")
    os.chmod(cred_file, 0o600)


def render_dnsmasq(
    offline_hostname: str,
    offline_hostname_fqdn: str,
    ip: str,
    prefix: int,
    dhcp_start: str,
    dhcp_end: str,
    upstream_dns: str,
    domain_enabled: bool,
    domain_fqdn: str,
    site_dns: list[str],
) -> None:
    netmask = str(ipaddress.ip_network(f"{ip}/{prefix}", strict=False).netmask)
    lines = [
        "interface=eth0",
        "bind-interfaces",
        "",
        "no-resolv",
        f"address=/{offline_hostname}/{ip}",
        f"address=/{offline_hostname_fqdn}/{ip}",
        f"server={upstream_dns}",
    ]
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
        f"dhcp-boot=tag:ipxe,http://{offline_hostname}/ipxe/autoexec.ipxe",
        "dhcp-boot=tag:!ipxe,tag:bios,undionly.kpxe",
        "dhcp-boot=tag:!ipxe,tag:efi-x86_64,ipxeboot/x86_64-sb/shimx64.efi",
        "",
    ]
    Path("/etc/dnsmasq.d/deploy-pxe.conf").write_text("\n".join(lines), encoding="utf-8")


def restart_services() -> None:
    for svc in ("dnsmasq", "smbd", "nginx"):
        proc = subprocess.run(["systemctl", "restart", svc], capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            raise RuntimeError(f"Failed to restart {svc}: {proc.stderr.strip()}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Headless offline deployer configuration.")
    parser.add_argument("--domain-enabled", choices=["true", "false"], required=True)
    parser.add_argument("--domain-fqdn", default="")
    parser.add_argument("--netbios", default="")
    parser.add_argument("--ou", default="")
    parser.add_argument("--dc-host", default="")
    parser.add_argument("--dc-ip", default="")
    parser.add_argument("--dns-servers", default="", help="comma/space separated site DNS IPs")
    parser.add_argument("--join-user", default="")
    parser.add_argument("--naming-source", default="service_tag")
    parser.add_argument("--naming-max-length", type=int, default=15)
    parser.add_argument("--ip", required=True)
    parser.add_argument("--prefix", type=int, required=True)
    parser.add_argument("--dhcp-start", required=True)
    parser.add_argument("--dhcp-end", required=True)
    parser.add_argument("--upstream-dns", required=True)
    args = parser.parse_args()

    cfg = load_offline_config()
    site_path = Path(cfg["site_path"])
    join_path = Path(cfg["join_secret_path"])
    offline_hostname = str(cfg["offline_hostname"])
    offline_hostname_fqdn = str(cfg["offline_hostname_fqdn"])

    domain_enabled = args.domain_enabled == "true"
    dns_servers = [s.strip() for s in args.dns_servers.replace(",", " ").split() if s.strip()]

    if domain_enabled:
        for required_label, required_value in [
            ("--domain-fqdn", args.domain_fqdn),
            ("--ou", args.ou),
            ("--join-user", args.join_user),
        ]:
            if not required_value:
                raise SystemExit(f"{required_label} is required when --domain-enabled true.")
        if not dns_servers:
            raise SystemExit("--dns-servers is required when --domain-enabled true.")
        join_pass = os.environ.get("JOIN_PASS", "")
        if not join_pass:
            raise SystemExit("JOIN_PASS environment variable is required when --domain-enabled true.")

    for label, value in [
        ("--ip", args.ip),
        ("--dhcp-start", args.dhcp_start),
        ("--dhcp-end", args.dhcp_end),
        ("--upstream-dns", args.upstream_dns),
    ]:
        try:
            ipaddress.ip_address(value)
        except ValueError as exc:
            raise SystemExit(f"{label} is not a valid IP: {exc}")

    write_site_config(
        site_path,
        enabled=domain_enabled,
        domain_fqdn=args.domain_fqdn,
        netbios=args.netbios,
        ou_path=args.ou,
        domain_controller=args.dc_host,
        domain_controller_ip=args.dc_ip,
        dns_servers=dns_servers if domain_enabled else [],
        naming_source=args.naming_source,
        naming_max_length=args.naming_max_length,
    )

    if domain_enabled:
        render_join_credential(join_path, args.join_user, os.environ["JOIN_PASS"])

    render_dnsmasq(
        offline_hostname=offline_hostname,
        offline_hostname_fqdn=offline_hostname_fqdn,
        ip=args.ip,
        prefix=args.prefix,
        dhcp_start=args.dhcp_start,
        dhcp_end=args.dhcp_end,
        upstream_dns=args.upstream_dns,
        domain_enabled=domain_enabled,
        domain_fqdn=args.domain_fqdn,
        site_dns=dns_servers,
    )
    restart_services()

    print(
        json.dumps(
            {
                "ok": True,
                "domain_enabled": domain_enabled,
                "site_path": str(site_path),
                "domain_fqdn": args.domain_fqdn,
            },
            separators=(",", ":"),
        )
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
