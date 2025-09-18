# How to Configure DNS64

- [How to Configure DNS64](#how-to-configure-dns64)
  - [Configuration](#configuration)
  - [Unbound configuration Explanation](#unbound-configuration-explanation)
    - [/etc/unbound/unbound.conf.d/root-auto-trust-anchor-file.conf](#etcunboundunboundconfdroot-auto-trust-anchor-fileconf)
    - [/etc/unbound/unbound.conf.d/logging.conf](#etcunboundunboundconfdloggingconf)
    - [/etc/unbound/unbound.conf.d/remote-control.conf](#etcunboundunboundconfdremote-controlconf)
    - [/etc/unbound/unbound.conf.d/local-resolver.conf](#etcunboundunboundconfdlocal-resolverconf)
    - [/etc/unbound/unbound.conf.d/dns64.conf](#etcunboundunboundconfddns64conf)
    - [/etc/unbound/unbound.conf.d/testlab-internal.conf](#etcunboundunboundconfdtestlab-internalconf)
    - [/etc/unbound/unbound.conf](#etcunboundunboundconf)
    - [Cross-file interaction and operational notes](#cross-file-interaction-and-operational-notes)
  - [Key Configurations](#key-configurations)

## Configuration

```
user@unbound01:~$ find /etc/unbound/ -type f -exec sh -c 'for file; do echo "===== $file ====="; cat "$file"; done' sh {} +
===== /etc/unbound/unbound.conf.d/root-auto-trust-anchor-file.conf =====
server:
    # The following line will configure unbound to perform cryptographic
    # DNSSEC validation using the root trust anchor.
    auto-trust-anchor-file: "/var/lib/unbound/root.key"
===== /etc/unbound/unbound.conf.d/logging.conf =====
server:
  # log every incoming query (qname, qtype, client)
  log-queries: yes
  # optional but handy: log answers and local/cache actions
  log-replies: yes
  log-local-actions: yes

  # send logs to syslog/journald (default on many distros)
  use-syslog: yes
  # keep verbosity modest; raise if you need more detail
  verbosity: 1
===== /etc/unbound/unbound.conf.d/remote-control.conf =====
remote-control:
  control-enable: yes
  # by default the control interface is is 127.0.0.1 and ::1 and port 8953
  # it is possible to use a unix socket too
  control-interface: /run/unbound.ctl
===== /etc/unbound/unbound.conf.d/local-resolver.conf =====
server:
  port: 53
  interface: 0.0.0.0
  interface: ::0

  do-ip4: yes
  do-ip6: yes

  # Allow localhost and LANs (v4 + v6):
  access-control: 127.0.0.0/8 allow
  access-control: ::1 allow

  access-control: 192.168.1.0/24 allow   # for dhcp17 (192.168.1.107/24)
  access-control: 192.168.2.0/24 allow
  access-control: 192.168.3.0/24 allow

  access-control: fd00:101:1::/64 allow
  access-control: 2001:4870:e00b:b800::/56 allow
  access-control: 2001:4870:e00b:b900::/56 allow
===== /etc/unbound/unbound.conf.d/dns64.conf =====
server:
  # enable DNS64 module before validator
  module-config: "dns64 validator iterator"

  # use the NAT64 prefix that your network routes
  dns64-prefix: 64:ff9b::/96        # <-- change if your core uses a custom /96

  # Ignore real AAAA for all domains; always synthesize AAAA from A
  dns64-ignore-aaaa: "."

  # good hygiene on IPv6 paths (prevents UDP/EDNS blackholes)
  edns-buffer-size: 1232
  max-udp-size: 1232
  do-tcp: yes
===== /etc/unbound/unbound.conf.d/testlab-internal.conf =====
server:
  # It's a private, unsigned zone — don't try to DNSSEC-validate it
  private-domain:  "testlab.lab."
  domain-insecure: "testlab.lab."

stub-zone:
  name: "testlab.lab."
  stub-addr: 192.168.1.21
  stub-addr: 192.168.1.22
===== /etc/unbound/unbound.conf =====
# Unbound configuration file for Debian.
#
# See the unbound.conf(5) man page.
#
# See /usr/share/doc/unbound/examples/unbound.conf for a commented
# reference config file.
#
server:
    # Local A Records
    local-data: "ipv4.me. IN A 36.150.108.196"
    local-data: "ipv4.me. IN A 101.205.144.103"

    local-data: "v4.ipv6test.app. IN A 18.65.25.117"
    local-data: "v4.ipv6test.app. IN A 18.65.25.115"
    local-data: "v4.ipv6test.app. IN A 18.65.25.77"
    local-data: "v4.ipv6test.app. IN A 18.65.25.110"

# The following line includes additional configuration files from the
# /etc/unbound/unbound.conf.d directory.
include-toplevel: "/etc/unbound/unbound.conf.d/-.conf"
```

## Unbound configuration Explanation

### /etc/unbound/unbound.conf.d/root-auto-trust-anchor-file.conf

- `server:`
    - Starts a `server` block. Directives under this header set global resolver behavior.
- `auto-trust-anchor-file: "/var/lib/unbound/root.key"`
  - Enables DNSSEC validation by telling Unbound where to find (and maintain via RFC 5011) the root zone trust anchor key.
  - On start, Unbound loads the key(s) from this file; it will also update the file over time when trust anchors roll.
  - If this file is missing or unreadable, Unbound will still resolve but will be unable to validate signatures; you’ll see warnings and the AD (Authenticated Data) bit will not be set on answers.

### /etc/unbound/unbound.conf.d/logging.conf

- `log-queries: yes`
  - Emits a log line for each received client query, including the queried name and type and the client address.
  - Useful for debugging and auditing; can be very verbose on busy resolvers.
- `log-replies: yes`
  - Logs the answer path/results (e.g., where the response came from, response code, whether from cache or upstream).
  - Helps correlate queries to responses and observe cache effectiveness.
- `log-local-actions: yes`
  - Logs notable local resolver actions (e.g., "refuse", "deny", "local data", "serve expired", "prefetch").
  - Good for understanding why Unbound chose a particular response source.
- `use-syslog: yes`
  - Directs Unbound to log via syslog (on systemd systems, this appears in journald).
  - If `logfile:` were set instead, logs would go to that file; here, you’re explicitly opting for syslog.
- `verbosity: 1`
  - Sets the minimum log level. Rough guide:
    - 0 = only errors
    - 1 = operational info (starts/stops) and messages triggered by logging toggles
    - higher values increase debugging detail
  - With `log-queries` and `log-replies` enabled, level 1 is typically sufficient.

### /etc/unbound/unbound.conf.d/remote-control.conf

- `remote-control:`
  - Begins a `remote-control` block. Options here manage the `unbound-control` administrative interface.
- `  control-enable: yes`
  - Enables the control channel so you can run `unbound-control status`, `flush`, `reload`, etc.
- `  control-interface: /run/unbound.ctl`
  - Uses a Unix domain socket for the control channel instead of TCP.
  - With a Unix socket, TLS client/server certificates are not used; access is governed by filesystem ownership/permissions on the socket path.
  - This avoids exposing a TCP port and simplifies local-only administration.

### /etc/unbound/unbound.conf.d/local-resolver.conf

- `  port: 53`
  - Sets the UDP/TCP listening port for the resolver. 53 is the DNS standard. This is the default, but being explicit is harmless and can aid readability.
- `  interface: 0.0.0.0`
  - Binds the IPv4 wildcard on all local IPv4 addresses. Unbound will accept client queries arriving on any IPv4 interface.
- `  interface: ::0`
  - Binds the IPv6 wildcard on all local IPv6 addresses. Unbound will accept client queries on any IPv6 interface.
- `do-ip4: yes`
  - Enables IPv4 for both listening and upstream resolver traffic. If set to `no`, Unbound would not accept IPv4 client queries nor talk to IPv4 upstreams.
- `do-ip6: yes`
  - Enables IPv6 for listening and upstreams. Needed if you want the resolver to accept queries over IPv6 and/or contact IPv6 authoritative/forwarder servers.
- `access-control: 127.0.0.0/8 allow`
  - Permits clients in the IPv4 loopback range to query and receive recursion. Without matching `allow` (or `allow_snoop`) rules, Unbound denies recursion by default.
- `access-control: ::1 allow`
  - Permits the IPv6 loopback address.
- `access-control: 192.168.1.0/24 allow   # for dhcp17 (192.168.1.107/24)`
  - Allows clients in the RFC1918 /24 192.168.1.0–192.168.1.255.
  - The trailing comment notes a specific host in that subnet for context.
- `access-control: 192.168.2.0/24 allow`
  - Allows clients in 192.168.2.0/24.
- `  access-control: 192.168.3.0/24 allow`
  - Allows clients in 192.168.3.0/24.
- `  access-control: fd00:101:1::/64 allow`
  - Allows clients in the ULA (Unique Local Address) IPv6 prefix fd00:101:1::/64.
- `  access-control: 2001:4870:e00b:b800::/56 allow`
  - Allows clients in this global IPv6 /56. All /64s within b800::/56 are permitted.
- `  access-control: 2001:4870:e00b:b900::/56 allow`
  - Allows clients in the adjacent global IPv6 /56 b900::/56.

Notes for this file:

- If a client IP (v4 or v6) falls outside these `allow` ranges, Unbound will refuse recursion (typically replying REFUSED).
- Binding both IPv4 and IPv6 wildcards means the ACLs are your main gatekeeper; your firewall should also allow/limit access as appropriate.

### /etc/unbound/unbound.conf.d/dns64.conf

- `  module-config: "dns64 validator iterator"`
  - Sets the internal module pipeline order: first the DNS64 synthesizer, then DNSSEC validator, then the iterator (the resolver engine).
  - With this order, Unbound can synthesize AAAA records from A records for IPv6-only clients/NAT64 environments. Synthesized AAAA records are not DNSSEC-signed; the validator will mark them as insecure (AD bit not set) while still validating other data.
- `  dns64-prefix: 64:ff9b::/96        # <-- change if your core uses a custom /96`
  - Configures the address prefix used when synthesizing AAAA from A.
  - `64:ff9b::/96` is the RFC 6052 "Well-Known Prefix". If your NAT64 uses a different /96, set it here so synthesized addresses are routable through your NAT64 gateway.
- `  dns64-ignore-aaaa: "."`
  - Tells Unbound to ignore existing AAAA records for all names (the dot is the root, i.e., "match everything") and always synthesize AAAA from A using the configured prefix.
  - This forces all IPv6 connections to traverse NAT64 even when a host is natively reachable over IPv6, which can be desirable for testing or policy but removes direct IPv6 connectivity and can degrade performance to dual-stack destinations.
- `  edns-buffer-size: 1232`
  - Caps the EDNS0 UDP payload size Unbound advertises to clients to 1232 bytes.
  - 1232 is a safe default for IPv6 paths (1280 minimum MTU minus IPv6/UDP/UDP options overhead), reducing fragmentation and timeouts on misconfigured networks.
- `  max-udp-size: 1232`
  - Caps the size Unbound will accept upstream over UDP. Keeps both sides aligned to avoid oversized responses getting dropped on the path.
- `  do-tcp: yes`
  - Ensures TCP is enabled so that when answers won’t fit in 1232 bytes (or TC=1 is set), Unbound can retry over TCP to complete resolution.

Notes for this file:

- DNS64 combined with DNSSEC has inherent limitations: synthesized AAAA cannot be validated. Clients relying on the AD bit should not expect it on synthesized answers.
- If you want DNS64 only when no real AAAA exists, omit `dns64-ignore-aaaa` or restrict its scope to domains where you truly need forced synthesis.

### /etc/unbound/unbound.conf.d/testlab-internal.conf

- `  private-domain:  "testlab.lab."`
  - Marks `testlab.lab.` as a private zone. Whitelists a domain so Unbound is allowed to return RFC1918/ULA addresses for names under that domain without stripping them out for "DNS-rebinding protection."
- `  domain-insecure: "testlab.lab."`
  - Disables DNSSEC validation for `testlab.lab.` and all its descendants. Declares a "negative trust anchor" for that domain. Unbound will not attempt DNSSEC validation for anything at or below testlab.lab. and will treat it as insecure (AD bit not set), regardless of what the parent says or whether signatures are present/missing.
- `stub-zone:`
  - Begins a stub zone definition. For names at or below `name:`, Unbound treats the listed IPs as the authoritative sources and queries them directly (no public recursion).
- `  name: "testlab.lab."`
  - Declares the apex of the internal zone. The trailing dot indicates a fully-qualified domain.
- `  stub-addr: 192.168.2.21`
  - First authoritative server address for `testlab.lab.`. Unbound will send queries directly here.
- `  stub-addr: 192.168.2.22`
  - Second authoritative server address for redundancy. Port defaults to 53; you can append `@port` if needed (e.g., `192.168.2.22@5353`).

Notes for this file:

- `stub-zone` differs from `forward-zone`: with a stub, Unbound does not rely on the upstream to recurse—it treats the listed IPs as authorities for `testlab.lab.` and goes straight to them.
- Because `domain-insecure` is set for this zone, DNSSEC validation is skipped under `testlab.lab.`, which is correct for an unsigned/private zone.
- With your global DNS64 settings (`module-config: "dns64 validator iterator"` and `dns64-ignore-aaaa: "."`), AAAA queries inside `testlab.lab.` will be synthesized from A records using `64:ff9b::/96`. The synthesized AAAA will not carry the AD bit, even if the A set validated elsewhere.
- If you later want native AAAA from `testlab.lab.` to be used when present, remove or scope down `dns64-ignore-aaaa` so Unbound does not force synthesis for that zone.
- After saving this file, run `unbound-checkconf` and then `unbound-control reload` to apply it.


### /etc/unbound/unbound.conf

- `    local-data: "ipv4.me. IN A 36.150.108.196"`
  - First A record for `ipv4.me.`. Multiple A records create a set.
- `    local-data: "ipv4.me. IN A 101.205.144.103"`
  - Second A record for `ipv4.me.`. Clients will receive both, and selection/order depends on client behavior and any response shuffling.
- `    local-data: "v4.ipv6test.app. IN A 18.65.25.117"`
  - First A record for `v4.ipv6test.app.`.
- `    local-data: "v4.ipv6test.app. IN A 18.65.25.115"`
  - Second A record for `v4.ipv6test.app.`.
- `    local-data: "v4.ipv6test.app. IN A 18.65.25.77"`
  - Third A record for `v4.ipv6test.app.`.
- `    local-data: "v4.ipv6test.app. IN A 18.65.25.110"`
  - Fourth A record for `v4.ipv6test.app.`.
  - With four A records, clients may load-balance across them; Unbound can also randomize RRset order unless otherwise configured.
- `include-toplevel: "/etc/unbound/unbound.conf.d/-.conf"`
  - Includes all files matching the glob at the top configuration scope.
  - Unlike an `include` placed inside a `server:` block, `include-toplevel` allows included files to define their own top-level blocks (`server:`, `remote-control:`, `forward-zone:`, etc.) as you’ve done in the `unbound.conf.d` directory.
  - The effective configuration is the union of this file and all included files; if the same option appears multiple times in the same scope, later entries generally override earlier ones.

### Cross-file interaction and operational notes

* Listener and ACLs

  * `interface` and `port` (local-resolver.conf) define where Unbound listens; `access-control` rules govern who can recurse. Ensure your OS firewall matches that intent.
* DNSSEC with DNS64
  * `auto-trust-anchor-file` enables DNSSEC validation for public zones. Synthesized AAAA from DNS64 cannot be DNSSEC-validated, so clients will see the AD bit unset on those AAAA answers; other data (e.g., A records, NS/DNSKEY) can still validate.
  * For `testlab.lab.`, `domain-insecure: "testlab.lab."` disables DNSSEC validation entirely under that subtree, so answers there will not be validated and the AD bit will be unset even for A records. This avoids SERVFAIL for an unsigned internal zone.
* Forcing NAT64
  * `dns64-ignore-aaaa: "."` means even dual-stack destinations are accessed via NAT64. If you want native IPv6 to remain in use when available, remove that line or scope it only to domains that require forced synthesis.
* Stubbed private zone
  * The `stub-zone` for `testlab.lab.` makes Unbound query your internal authoritative servers (`192.168.1.21`, `192.168.1.22`) directly instead of performing public recursion or using a forwarder. If those IPs are unreachable, lookups under `testlab.lab.` fail fast (no fallback to the public DNS tree).
  * `private-domain: "testlab.lab."` allows RFC1918/ULA answers to be returned for that suffix without DNS-rebinding filtering (only relevant if `private-address:` filtering is enabled).
  * With your global DNS64 settings, AAAA queries under `testlab.lab.` will be synthesized from A using `64:ff9b::/96` and will not carry the AD bit.
* Local overrides
  * `local-data` entries make Unbound authoritative for those exact names; upstream data for those names is ignored.
  * Active in your config: `ipv4.me.` and `v4.ipv6test.app.` are served from `local-data` (A answers come from your file; AAAA are synthesized by DNS64).

## Key Configurations

- module-config: "dns64 validator iterator" makes the DNS64 module run first on replies, then DNSSEC validation, then the iterator (normal resolution). Because DNS64 runs up front, Unbound can fetch A records and synthesize AAAA before the validator evaluates the final response.
- dns64-prefix: `64:ff9b::/96` is the well-known NAT64 prefix used to embed IPv4 addresses into IPv6 addresses for synthesized AAAA answers.
- dns64-ignore-aaaa: "." forces Unbound to ignore real AAAA records for all domains and always synthesize AAAA from A. This is intentionally more aggressive than RFC 6147’s default behavior and is why dual-stack destinations still traverse NAT64.
- edns-buffer-size: 1232 and max-udp-size: 1232 minimize IPv6 path fragmentation issues and nudge large answers to TCP; do-tcp: yes enables that fallback so oversized DNS responses complete reliably.
- access-control entries allow your localhost, LAN IPv4 ranges, and ULA/GUA IPv6 prefixes to perform recursion against this resolver.
- Unbound listens on 0.0.0.0 and ::0 on port 53, so clients can reach it natively over IPv6; no NAT64 is required for DNS queries to the resolver itself.
- stub-zone for testlab.lab. tells Unbound to contact 192.168.1.21 and 192.168.1.22 directly as the authorities for that internal zone instead of performing public recursion or forwarding. Only queries under testlab.lab. are affected; public domains in your diagrams are unrelated.
- private-domain: "testlab.lab." and domain-insecure: "testlab.lab." together declare that testlab.lab. is an internal, unsigned zone: Unbound will accept RFC1918/ULA answers for it (no rebind filtering for that suffix) and will skip DNSSEC validation under that subtree.
