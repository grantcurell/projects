#!/usr/bin/env python3
"""Active Directory discovery + permission preflight for the offline deployer.

The deployer is a workgroup Linux appliance. It NEVER joins the domain and never
runs djoin. It only:
  * queries the operator-provided site DNS server(s) for AD SRV records to find DCs
    (the site DNS may or may not be the domain controller),
  * binds over LDAP with the delegated join credential to read non-secret domain
    metadata (domain FQDN, NetBIOS name, base DN, OUs, DC list), and
  * verifies (non-mutating) that the delegated account can create computer objects
    in the selected OU.

Binding uses Kerberos (SASL/GSSAPI). This is the only method that satisfies a
default-hardened AD DC: such DCs require LDAP signing and very often have no
LDAPS certificate installed, so SIMPLE/NTLM binds over plain LDAP are refused
with ``strongerAuthRequired`` and LDAPS is unavailable. GSSAPI negotiates an
integrity/confidentiality layer (signing/sealing) over plain LDAP/389, exactly
like Windows itself. The TGT is obtained directly from the supplied
username/password, so no prior ``kinit``/ticket cache is required.

No credentials are ever persisted by this module. Callers pass them in memory.
"""
from __future__ import annotations

import ipaddress
import os
import socket
import tempfile
from dataclasses import dataclass, field
from typing import Any

import dns.resolver  # type: ignore
import ldap  # type: ignore
import ldap.sasl  # type: ignore


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
# LDAP via Kerberos (SASL/GSSAPI)
# ---------------------------------------------------------------------------
class LdapConn:
    """Lightweight handle around a bound python-ldap connection + RootDSE info."""

    def __init__(self, handle: Any, base_dn: str, rootdse: dict[str, str],
                 dc_fqdn: str, dc_ip: str) -> None:
        self.handle = handle
        self.base_dn = base_dn
        self.rootdse = rootdse
        self.dc_fqdn = dc_fqdn
        self.dc_ip = dc_ip

    def unbind(self) -> None:
        try:
            self.handle.unbind_s()
        except Exception:  # noqa: BLE001
            pass


def _ldap_err(exc: Exception) -> str:
    """Extract the most useful message from a python-ldap exception."""
    if getattr(exc, "args", None) and isinstance(exc.args[0], dict):
        detail = exc.args[0]
        return str(detail.get("info") or detail.get("desc") or detail)
    return str(exc)


def _decode(value: Any) -> str:
    return value.decode("utf-8", "replace") if isinstance(value, (bytes, bytearray)) else str(value)


def _realm_from_domain(domain_fqdn: str) -> str:
    return domain_fqdn.strip(".").upper()


def _kerberos_principal(username: str, realm: str) -> str:
    """Turn DOMAIN\\sam, sam, or user@REALM into a Kerberos principal."""
    user = (username or "").strip()
    if not user:
        raise DiscoveryError("No domain username provided.")
    if "@" in user:
        return user
    sam = user.split("\\")[-1].split("/")[-1]
    return f"{sam}@{realm}"


def _write_krb5_conf(realm: str, domain_fqdn: str, kdc_ip: str) -> str:
    """Write a self-contained krb5.conf pinned to the discovered KDC.

    DNS-based KDC/realm discovery is disabled because the offline deployer's
    system resolver is not pointed at the domain DNS; we hand krb5 the KDC IP
    directly. rdns=false stops the library from reverse-resolving the KDC IP
    (which would also need DNS) when building the service principal name.
    """
    dom = domain_fqdn.strip(".").lower()
    conf = (
        "[libdefaults]\n"
        f"    default_realm = {realm}\n"
        "    dns_lookup_realm = false\n"
        "    dns_lookup_kdc = false\n"
        "    rdns = false\n"
        "    udp_preference_limit = 0\n"
        "[realms]\n"
        f"    {realm} = {{\n"
        f"        kdc = {kdc_ip}\n"
        f"        admin_server = {kdc_ip}\n"
        "    }\n"
        "[domain_realm]\n"
        f"    .{dom} = {realm}\n"
        f"    {dom} = {realm}\n"
    )
    path = os.path.join(tempfile.gettempdir(), "windep-krb5.conf")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(conf)
    return path


def _ensure_hosts_entry(ip: str, fqdn: str) -> None:
    """Map the DC FQDN to its IP in /etc/hosts.

    cyrus-sasl builds the GSSAPI service principal (ldap/<fqdn>) from, and opens
    the TCP socket to, the LDAP URI host. We must therefore connect by FQDN, but
    the deployer's system resolver may not answer for the domain. Pinning the
    mapping here makes the FQDN resolve to the IP we already discovered via the
    site DNS, without changing the deployer's resolver.
    """
    fqdn_l = fqdn.lower()
    try:
        with open("/etc/hosts", "r", encoding="utf-8") as handle:
            lines = handle.read().splitlines()
    except OSError:
        return
    kept = [
        line for line in lines
        if not (len(line.split()) >= 2
                and any(part.lower() == fqdn_l for part in line.split()[1:]))
    ]
    kept.append(f"{ip}\t{fqdn}")
    try:
        with open("/etc/hosts", "w", encoding="utf-8") as handle:
            handle.write("\n".join(kept) + "\n")
    except OSError:
        pass


def _acquire_ticket(principal: str, password: str, krb5_conf: str) -> None:
    """Obtain a TGT for principal from the password and store it in a private
    credential cache that the subsequent SASL bind will use."""
    import gssapi  # type: ignore  # lazy: only needed at bind time
    from gssapi.raw import acquire_cred_with_password, store_cred_into  # type: ignore

    os.environ["KRB5_CONFIG"] = krb5_conf
    ccache = os.path.join(tempfile.gettempdir(), "windep-krb5cc")
    os.environ["KRB5CCNAME"] = "FILE:" + ccache
    try:
        name = gssapi.Name(principal, gssapi.NameType.user)
        creds = acquire_cred_with_password(
            name, password.encode("utf-8"), usage="initiate"
        ).creds
        store_cred_into(
            {"ccache": "FILE:" + ccache}, creds, usage="initiate", overwrite=True
        )
    except Exception as exc:  # noqa: BLE001
        raise DiscoveryError(
            f"Kerberos authentication failed for {principal}: {exc}. "
            "Verify the username and password, and that the domain controller is "
            "reachable on port 88 (Kerberos)."
        ) from exc


def ldap_bind(
    dc_host: str,
    username: str,
    password: str,
    use_ssl: bool = True,  # retained for API compatibility; GSSAPI is always used
    dns_servers: list[str] | None = None,
    timeout: int = 8,
    domain_fqdn: str | None = None,
) -> LdapConn:
    """Bind to a DC using Kerberos (SASL/GSSAPI) with the delegated credential.

    ``dc_host`` must be the DC's FQDN (as returned by SRV discovery) so the
    Kerberos service principal ``ldap/<fqdn>`` can be formed. The KDC IP is
    resolved via the operator-provided site DNS; the deployer's own resolver is
    not relied upon.
    """
    if not dc_host:
        raise DiscoveryError("No domain controller host provided for LDAP bind.")
    try:
        ipaddress.ip_address(dc_host)
        raise DiscoveryError(
            f"A domain controller FQDN is required for Kerberos discovery; got IP '{dc_host}'."
        )
    except ValueError:
        pass  # dc_host is a hostname, as required

    dc_fqdn = dc_host
    domain = (domain_fqdn or "").strip(".")
    if not domain:
        if "." in dc_fqdn:
            domain = dc_fqdn.split(".", 1)[1]
        else:
            raise DiscoveryError(
                f"Cannot determine the Kerberos realm: '{dc_fqdn}' is not an FQDN "
                "and no domain was provided."
            )
    realm = _realm_from_domain(domain)
    principal = _kerberos_principal(username, realm)

    if dns_servers:
        kdc_ip = resolve_host(dns_servers, dc_fqdn)
    else:
        try:
            kdc_ip = socket.gethostbyname(dc_fqdn)
        except OSError as exc:
            raise DiscoveryError(
                f"Could not resolve {dc_fqdn}: {exc}. Provide the site DNS server(s)."
            ) from exc

    krb5_conf = _write_krb5_conf(realm, domain, kdc_ip)
    _acquire_ticket(principal, password, krb5_conf)
    _ensure_hosts_entry(kdc_ip, dc_fqdn)

    uri = f"ldap://{dc_fqdn}:389"
    try:
        handle = ldap.initialize(uri)
        handle.set_option(ldap.OPT_REFERRALS, 0)
        handle.set_option(ldap.OPT_PROTOCOL_VERSION, 3)
        handle.set_option(ldap.OPT_NETWORK_TIMEOUT, int(timeout))
        handle.set_option(ldap.OPT_TIMEOUT, int(timeout))
        # Require a SASL security layer (signing) so we never fall back to an
        # unsigned/cleartext channel against a DC that demands signing.
        handle.set_option(ldap.OPT_X_SASL_SSF_MIN, 1)
        handle.sasl_interactive_bind_s("", ldap.sasl.gssapi(""))
    except ldap.LDAPError as exc:  # type: ignore[attr-defined]
        raise DiscoveryError(
            f"LDAP GSSAPI bind to {dc_fqdn} failed for {principal}: {_ldap_err(exc)}"
        ) from exc

    rootdse = _read_rootdse(handle)
    base_dn = rootdse.get("defaultNamingContext") or rootdse.get("rootDomainNamingContext") or ""
    return LdapConn(handle, base_dn, rootdse, dc_fqdn, kdc_ip)


def _read_rootdse(handle: Any) -> dict[str, str]:
    try:
        results = handle.search_s(
            "", ldap.SCOPE_BASE, "(objectClass=*)",
            ["defaultNamingContext", "rootDomainNamingContext", "dnsHostName"],
        )
    except ldap.LDAPError as exc:  # type: ignore[attr-defined]
        raise DiscoveryError(f"LDAP bind succeeded but RootDSE was unreadable: {_ldap_err(exc)}") from exc
    out: dict[str, str] = {}
    for _dn, attrs in results:
        if not isinstance(attrs, dict):
            continue
        for key, values in attrs.items():
            if values:
                out[key] = _decode(values[0])
    return out


def discover_domain_metadata(conn: LdapConn, dns_servers: list[str]) -> DomainMetadata:
    """Read non-secret domain metadata from a bound LDAP connection."""
    base_dn = conn.base_dn
    if not base_dn:
        raise DiscoveryError("LDAP bind succeeded but defaultNamingContext was unavailable.")

    domain_fqdn = ".".join(
        part[3:] for part in base_dn.split(",") if part.lower().startswith("dc=")
    )

    netbios = _query_netbios(conn, base_dn)
    ous = _list_ous(conn, base_dn)
    dcs: list[str] = []
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


def _query_netbios(conn: LdapConn, base_dn: str) -> str:
    config_dn = "CN=Partitions,CN=Configuration," + base_dn
    try:
        results = conn.handle.search_s(
            config_dn, ldap.SCOPE_SUBTREE,
            f"(&(objectClass=crossRef)(nCName={base_dn}))", ["nETBIOSName"],
        )
    except ldap.LDAPError:  # type: ignore[attr-defined]
        return ""
    for _dn, attrs in results:
        if isinstance(attrs, dict):
            values = attrs.get("nETBIOSName") or []
            if values:
                return _decode(values[0])
    return ""


def _list_ous(conn: LdapConn, base_dn: str) -> list[str]:
    try:
        results = conn.handle.search_s(
            base_dn, ldap.SCOPE_SUBTREE,
            "(objectClass=organizationalUnit)", ["distinguishedName"],
        )
    except ldap.LDAPError as exc:  # type: ignore[attr-defined]
        raise DiscoveryError(f"Failed to enumerate OUs under {base_dn}: {_ldap_err(exc)}") from exc
    ous: list[str] = []
    for dn, _attrs in results:
        if dn and dn not in ous:  # referrals come back with dn=None
            ous.append(dn)
    return sorted(ous)


def check_ou_create_rights(conn: LdapConn, ou_dn: str) -> bool:
    """Non-mutating check that the bound account can create computer objects in ou_dn.

    Reads allowedChildClassesEffective on the OU; no test object is created in AD.
    """
    try:
        results = conn.handle.search_s(
            ou_dn, ldap.SCOPE_BASE, "(objectClass=*)",
            ["allowedChildClassesEffective"],
        )
    except ldap.LDAPError as exc:  # type: ignore[attr-defined]
        raise DiscoveryError(f"Could not read effective rights on {ou_dn}: {_ldap_err(exc)}") from exc
    if not results:
        raise DiscoveryError(f"OU {ou_dn} was not found or is not readable by the join account.")
    effective: list[Any] = []
    for _dn, attrs in results:
        if isinstance(attrs, dict):
            effective = attrs.get("allowedChildClassesEffective") or []
        break
    classes = {_decode(item).lower() for item in effective}
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
    conn = ldap_bind(
        bind_target, username, password,
        dns_servers=dns_servers, domain_fqdn=domain_fqdn,
    )
    try:
        metadata = discover_domain_metadata(conn, dns_servers)
        if ou_dn:
            check_ou_create_rights(conn, ou_dn)
        result = metadata.to_dict()
        result["bound_dc"] = bind_target
        result["domain_controller_ip"] = conn.dc_ip or ""
        return result
    finally:
        conn.unbind()
