# No-Defaults Audit Report

## Scope

All `*.ps1` files in the repository were reviewed for hard-coded environment-specific configuration defaults.

## Findings

- **No invalid hard-coded defaults found in implementation modules** for:
  - domain names
  - hostnames
  - DNS forwarders
  - NTP servers
  - OU names
  - group names
  - service account names
  - GPO names
  - Wazuh manager addresses
  - WSUS URLs
  - scheduled task names

- **Hard-coded values that remain and are valid internal constants**:
  - Windows feature identifiers (for role installation)
  - registry key paths for Windows policy settings
  - protocol constants (`0.0.0.0/0` default route query)
  - known Windows local account label `Guest` used only for rename/disable logic
  - service names representing platform components (`CertSvc`, `WsusService`, `w32time`) where these are product constants rather than environment configuration

- **Test-only literals** remain in `tests/Pester` and are intentional:
  - synthetic IPs/domains for unit tests
  - example adapter aliases and small fixture data

## Values moved to YAML

Environment-specific values are sourced from YAML, including:

- domain and NetBIOS naming
- static IPv4/gateway/DNS client settings
- DNS forwarders and validation records
- DHCP server settings, scopes, reservations, and reconcile behavior
- external NTP peers and behavior when not PDC
- OU/group/service-account definitions
- GPO definitions and link order
- firewall profile/rule-group/custom-rule settings
- WEF/Wazuh/WSUS/PKI/backup/scanning/integration settings
- resume scheduled task name and all execution paths

## Remaining Items

- No additional invalid configuration defaults remain in implementation modules after audit.
