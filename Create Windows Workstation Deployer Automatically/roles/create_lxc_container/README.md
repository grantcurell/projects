# Create LXC Container Role

Reusable role for creating Proxmox LXC containers with consistent configuration.

## Purpose

This role provides a standardized way to create LXC containers on Proxmox for various services (PowerDNS, Traefik, Authentik, etc.).

## Variables

All variables must be provided via `lxc_container` dictionary:

```yaml
lxc_container:
  vmid: 105
  hostname: "powerdns"
  ostemplate: "local:vztmpl/ubuntu-24.04-standard_24.04-1_amd64.tar.zst"
  cores: 2
  memory_mb: 4096
  swap_mb: 0
  rootfs_gb: 30
  unprivileged: true
  nesting: true
  bridge: "vmbr0"
  vlan_tag: 10
  hwaddr: "BC:24:11:60:1A:1B"
  ip: "172.27.10.9"
  cidr: 24
  gateway: "172.27.10.1"
```

## Dependencies

- `community.proxmox` collection (version >=1.0.0,<2.0.0)
- Proxmox API access configured in `proxmox` variables

## Usage

```yaml
- name: Create PowerDNS LXC container
  hosts: proxmox
  gather_facts: false
  roles:
    - role: create_lxc_container
      vars:
        lxc_container:
          vmid: 105
          hostname: "powerdns"
```
