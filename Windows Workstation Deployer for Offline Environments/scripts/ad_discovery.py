#!/usr/bin/env python3
"""Active Directory discovery + permission preflight for the offline deployer.

The deployer is a workgroup Linux appliance. It NEVER joins the domain and never
runs djoin. It only:
  * queries the operator-provided site DNS server(s) for AD SRV records to find DCs
    (the site DNS may or may not be the domain controller),
  * binds over LDAP/LDAPS with the delegated join credential to read non-secret
    domain metadata (domain FQDN, NetBIOS name, base DN, OUs, DC list), and
  * verifies (non-mutating) that the delegated account can create computer objects
    in the selected OU.

No credentials are ever persisted by this module. Callers pass them in memory.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import ipaddress
import socket

import dns.resolver  # type: ignore
import ldap3  # type: ignore
from ldap3 import Connection, Server, Tls, ALL, SUBTREE
import ssl


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------
@dataclass
class DomainMetadata:
    domain_fqdn: str = ""
    domain_netbios: str = ""
    base_dn: str = ""
    domain_controllers: list[str] = field(default_factory=list)
    organizational_units: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "domain_fqdn": self.domain_fqdn,
            "domain_netbios": self.domain_netbios,
            "base_dn": self.base_dn,
            "domain_controllers": list(self.domain_controllers),
            "organizational_units": list(self.organizational_units),
        }


class DiscoveryError(RuntimeError):
    """Raised for any discovery/validation failure with an operator-facing message."""


# ---------------------------------------------------------------------------
# DNS (against the operator-provided site DNS servers)
# ---------------------------------------------------------------------------
def _resolver(dns_servers: list[str], timeout: float = 5.0) -> dns.resolver.Resolver:
    if not dns_servers:
        raise DiscoveryError("No site DNS server(s) provided; cannot run AD discovery.")
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = list(dns_servers)
    resolver.lifetime = timeout
    resolver.timeout = timeout
    return resolver


def dns_server_responds(server: str, timeout: float = 4.0) -> None:
    """Confirm a host is actually a DNS server by connecting to TCP port 53.

    We deliberately do NOT issue a recursive lookup: an isolated AD DNS server
    (no internet access or root hints) times out trying to recurse on external
    names, which makes a perfectly healthy DC look dead. A TCP/53 connection
    proves a DNS service is listening without triggering recursion. ICMP ping is
    also avoided - DNS servers frequently drop ICMP while still serving DNS.
    Raises DiscoveryError if nothing is listening on port 53.
    """
    try:
        with socket.create_connection((server, 53), timeout=timeout):
            return
    except OSError as exc:
        raise DiscoveryError(
            f"DNS server {server} is not listening on port 53 ({exc})."
        ) from exc


def resolve_srv(dns_servers: list[str], srv_name: str) -> list[tuple[str, int]]:
    """Return [(target_host, port), ...] for an SRV record, sorted by priority/weight."""
    resolver = _resolver(dns_servers)
    try:
        answer = resolver.resolve(srv_name, "SRV")
    except Exception as exc:  # noqa: BLE001
        raise DiscoveryError(f"SRV lookup failed for {srv_name}: {exc}") from exc
    records = sorted(answer, key=lambda r: (r.priority, -r.weight))
    return [(str(r.target).rstrip("."), int(r.port)) for r in records]


def resolve_host(dns_servers: list[str], hostname: str) -> str:
    """Resolve an A record for hostname using the site DNS server(s)."""
    resolver = _resolver(dns_servers)
    try:
        answer = resolver.resolve(hostname, "A")
    except Exception as exc:  # noqa: BLE001
        raise DiscoveryError(f"A lookup failed for {hostname}: {exc}") from exc
    for record in answer:
        return str(record)
    raise DiscoveryError(f"No A record returned for {hostname}.")


def site_dns_answers_ad(dns_servers: list[str], domain_fqdn: str) -> list[str]:
    """Confirm the site DNS serves AD SRV records; return discovered DC hostnames.

    Raises DiscoveryError if the provided DNS does not resolve _ldap._tcp.<domain>.
    """
    srv = f"_ldap._tcp.{domain_fqdn}"
    targets = resolve_srv(dns_servers, srv)
    if not targets:
        raise DiscoveryError(
            f"The DNS server(s) {dns_servers} did not resolve {srv}. "
            "This site's AD DNS may be on a different server than the one entered."
        )
    return [host for host, _port in targets]


def discover_dcs(dns_servers: list[str], domain_fqdn: str) -> list[str]:
    """Discover domain controllers via the standard AD SRV records."""
    discovered: list[str] = []
    for srv in (
        f"_ldap._tcp.dc._msdcs.{domain_fqdn}",
        f"_ldap._tcp.{domain_fqdn}",
        f"_kerberos._tcp.{domain_fqdn}",
    ):
        try:
            for host, _port in resolve_srv(dns_servers, srv):
                if host not in discovered:
                    discovered.append(host)
        except DiscoveryError:
            continue
    if not discovered:
        raise DiscoveryError(
            f"No domain controllers discovered for {domain_fqdn} via the provided DNS server(s)."
        )
    return discovered


# ---------------------------------------------------------------------------
# LDAP / LDAPS
# ---------------------------------------------------------------------------
def ldap_bind(
    dc_host: str,
    username: str,
    password: str,
    use_ssl: bool = True,
    dns_servers: list[str] | None = None,
    timeout: float = 8.0,
) -> Connection:
    """Bind to a DC with the delegated credential. Tries LDAPS, then LDAP.

    If dns_servers is provided and dc_host is a hostname, it is resolved via the
    site DNS rather than the deployer's system resolver. This is critical on a
    freshly-deployed deployer whose /etc/resolv.conf still points at an
    unreachable build-network resolver - otherwise ldap3's hostname lookup hangs
    indefinitely. connect/receive timeouts guarantee the bind never blocks
    forever.
    """
    target = dc_host
    if dns_servers:
        try:
            ipaddress.ip_address(dc_host)  # already an IP -> use directly
        except ValueError:
            try:
                target = resolve_host(dns_servers, dc_host)
            except DiscoveryError:
                target = dc_host  # let the connect fail fast under the timeout
    last_exc: Exception | None = None
    attempts = [(use_ssl, 636 if use_ssl else 389)]
    if use_ssl:
        attempts.append((False, 389))  # fall back to plain LDAP if LDAPS unavailable
    for ssl_flag, port in attempts:
        try:
            tls = Tls(validate=ssl.CERT_NONE) if ssl_flag else None
            server = Server(
                target, port=port, use_ssl=ssl_flag, get_info=ALL, tls=tls,
                connect_timeout=timeout,
            )
            conn = Connection(
                server,
                user=username,
                password=password,
                authentication=ldap3.NTLM if "\\" in username else ldap3.SIMPLE,
                auto_bind=True,
                receive_timeout=timeout,
            )
            return conn
        except Exception as exc:  # noqa: BLE001
            last_exc = exc
            continue
    raise DiscoveryError(f"LDAP bind to {dc_host} failed for {username}: {last_exc}")


def discover_domain_metadata(conn: Connection, dns_servers: list[str]) -> DomainMetadata:
    """Read non-secret domain metadata from a bound LDAP connection."""
    info = conn.server.info
    if info is None or not info.other:
        raise DiscoveryError("LDAP bind succeeded but RootDSE info was unavailable.")

    def _first(key: str) -> str:
        values = info.other.get(key) or []
        return str(values[0]) if values else ""

    base_dn = _first("defaultNamingContext") or _first("rootDomainNamingContext")
    if not base_dn:
        raise DiscoveryError("Could not determine defaultNamingContext from the DC.")

    domain_fqdn = ".".join(
        part[3:] for part in base_dn.split(",") if part.lower().startswith("dc=")
    )

    netbios = _query_netbios(conn, base_dn)
    ous = _list_ous(conn, base_dn)
    dcs = []
    if domain_fqdn:
        try:
            dcs = discover_dcs(dns_servers, domain_fqdn)
        except DiscoveryError:
            dcs = []

    return DomainMetadata(
        domain_fqdn=domain_fqdn,
        domain_netbios=netbios,
        base_dn=base_dn,
        domain_controllers=dcs,
        organizational_units=ous,
    )


def _query_netbios(conn: Connection, base_dn: str) -> str:
    config_dn = "CN=Partitions,CN=Configuration," + base_dn
    try:
        conn.search(
            config_dn,
            "(&(objectClass=crossRef)(nCName=" + base_dn + "))",
            search_scope=SUBTREE,
            attributes=["nETBIOSName"],
        )
        for entry in conn.entries:
            value = entry.entry_attributes_as_dict.get("nETBIOSName") or []
            if value:
                return str(value[0])
    except Exception:  # noqa: BLE001
        return ""
    return ""


def _list_ous(conn: Connection, base_dn: str) -> list[str]:
    try:
        conn.search(
            base_dn,
            "(objectClass=organizationalUnit)",
            search_scope=SUBTREE,
            attributes=["distinguishedName"],
        )
    except Exception as exc:  # noqa: BLE001
        raise DiscoveryError(f"Failed to enumerate OUs under {base_dn}: {exc}") from exc
    ous = []
    for entry in conn.entries:
        dn = str(entry.entry_dn)
        if dn and dn not in ous:
            ous.append(dn)
    return sorted(ous)


def check_ou_create_rights(conn: Connection, ou_dn: str) -> bool:
    """Non-mutating check that the bound account can create computer objects in ou_dn.

    Reads allowedChildClassesEffective on the OU; no test object is created in AD.
    """
    try:
        ok = conn.search(
            ou_dn,
            "(objectClass=*)",
            search_scope=ldap3.BASE,
            attributes=["allowedChildClassesEffective"],
        )
    except Exception as exc:  # noqa: BLE001
        raise DiscoveryError(f"Could not read effective rights on {ou_dn}: {exc}") from exc
    if not ok or not conn.entries:
        raise DiscoveryError(f"OU {ou_dn} was not found or is not readable by the join account.")
    effective = conn.entries[0].entry_attributes_as_dict.get("allowedChildClassesEffective") or []
    classes = {str(c).lower() for c in effective}
    if "computer" not in classes:
        raise DiscoveryError(
            f"The delegated account lacks 'Create Computer Object' rights on {ou_dn}. "
            "Delegate that permission (scoped to the workstation OU) and retry."
        )
    return True


def full_preflight(
    dns_servers: list[str],
    domain_fqdn: str,
    username: str,
    password: str,
    ou_dn: str | None = None,
) -> dict[str, Any]:
    """Run the complete discovery + permission preflight. Returns a result dict.

    Raises DiscoveryError at the first failing gate with an operator-facing message.
    """
    dcs = site_dns_answers_ad(dns_servers, domain_fqdn)
    bind_target = dcs[0]
    conn = ldap_bind(bind_target, username, password, dns_servers=dns_servers)
    try:
        metadata = discover_domain_metadata(conn, dns_servers)
        if ou_dn:
            check_ou_create_rights(conn, ou_dn)
        result = metadata.to_dict()
        result["bound_dc"] = bind_target
        if metadata.domain_fqdn:
            try:
                result["domain_controller_ip"] = resolve_host(dns_servers, bind_target)
            except DiscoveryError:
                result["domain_controller_ip"] = ""
        return result
    finally:
        try:
            conn.unbind()
        except Exception:  # noqa: BLE001
            pass
