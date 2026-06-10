#!/usr/bin/env bash
#
# offline-deploy-deployer.sh
#
# Field tool: pushes the exported deployer LXC tarball onto an offline Proxmox
# host and starts it, so you can run the on-deployer offline-setup TUI.
#
# It walks you through:
#   1. Proxmox IP + username + password
#   2. Confirming connectivity to Proxmox
#   3. Choosing which cluster node to deploy the deployer to
#   4. Choosing which storage on that node to deploy to
#   5. Restoring + starting the deployer, then printing exactly how to finish
#      setup from the Proxmox console (where offline-setup lives).
#
set -euo pipefail

# --------------------------------------------------------------------------
# Pretty output helpers
# --------------------------------------------------------------------------
if [[ -t 1 ]]; then
  BOLD="$(printf '\033[1m')"; DIM="$(printf '\033[2m')"; RED="$(printf '\033[31m')"
  GREEN="$(printf '\033[32m')"; YELLOW="$(printf '\033[33m')"; CYAN="$(printf '\033[36m')"
  RESET="$(printf '\033[0m')"
else
  BOLD=""; DIM=""; RED=""; GREEN=""; YELLOW=""; CYAN=""; RESET=""
fi

info()  { printf '%s\n' "${CYAN}$*${RESET}"; }
ok()    { printf '%s\n' "${GREEN}$*${RESET}"; }
warn()  { printf '%s\n' "${YELLOW}$*${RESET}"; }
err()   { printf '%s\n' "${RED}$*${RESET}" >&2; }
hr()    { printf '%s\n' "${DIM}--------------------------------------------------------------------------------${RESET}"; }

die() { err "ERROR: $*"; exit 1; }

# Prompt for a numeric menu choice and re-prompt until the user enters a valid
# value in 1..max. Returns the choice on stdout (the prompt is shown on stderr by
# `read -p`, so command substitution still displays it).
read_choice() {
  local prompt="$1" max="$2" sel
  while true; do
    read -r -p "$prompt" sel || die "Input aborted."
    if [[ "$sel" =~ ^[0-9]+$ ]] && (( sel >= 1 && sel <= max )); then
      printf '%s' "$sel"
      return 0
    fi
    err "Invalid selection. Enter a number between 1 and ${max}."
  done
}

# Deployer's portable hostname + the on-deployer TUI path (matches inventory
# defaults deployer.offline.hostname / deployer.offline_tui.entrypoint).
DEPLOYER_HOSTNAME="win-deploy"
OFFLINE_TUI_PATH="/usr/local/bin/offline-setup"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

# --------------------------------------------------------------------------
# 0. Dependency + tarball discovery
# --------------------------------------------------------------------------
require_tools() {
  local missing=()
  for t in sshpass ssh scp; do
    command -v "$t" >/dev/null 2>&1 || missing+=("$t")
  done
  command -v jq >/dev/null 2>&1 || missing+=("jq")
  if (( ${#missing[@]} > 0 )); then
    err "Missing required tools: ${missing[*]}"
    err "Install them and re-run, e.g.:"
    err "  Debian/Ubuntu:  sudo apt-get install -y sshpass jq openssh-client"
    err "  RHEL/Rocky:     sudo dnf install -y sshpass jq openssh-clients"
    exit 1
  fi
}

discover_tarball() {
  # Look for the exported deployer backup in common locations, newest first.
  local candidates=()
  local d
  for d in "$PROJECT_ROOT/artifacts" "$SCRIPT_DIR" "$PWD"; do
    [[ -d "$d" ]] || continue
    while IFS= read -r f; do
      [[ -n "$f" ]] && candidates+=("$f")
    done < <(find "$d" -maxdepth 1 -type f -name 'vzdump-lxc-*.tar.zst' -printf '%T@ %p\n' 2>/dev/null | sort -rn | cut -d' ' -f2-)
  done

  if (( ${#candidates[@]} == 1 )); then
    TARBALL="${candidates[0]}"
    return 0
  fi
  if (( ${#candidates[@]} > 1 )); then
    info "Found multiple deployer tarballs:"
    local i=1
    for f in "${candidates[@]}"; do
      printf '   %s) %s (%s)\n' "$i" "$f" "$(du -h "$f" | cut -f1)"
      ((i++))
    done
    local sel
    sel="$(read_choice "Select the tarball to deploy [1-${#candidates[@]}]: " "${#candidates[@]}")"
    TARBALL="${candidates[$((sel-1))]}"
    return 0
  fi

  # None found near the script; ask for an explicit path.
  warn "No vzdump-lxc-*.tar.zst found in artifacts/, the script directory, or $PWD."
  read -r -e -p "Enter the full path to the deployer tarball: " TARBALL
  [[ -f "$TARBALL" ]] || die "File not found: $TARBALL"
}

# --------------------------------------------------------------------------
# SSH/SCP wrappers (password auth via sshpass + SSHPASS env)
# --------------------------------------------------------------------------
SSH_OPTS=(-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=10)

prox_ssh() { sshpass -e ssh "${SSH_OPTS[@]}" "${PROX_USER}@${PROX_IP}" "$@"; }
node_ssh() { sshpass -e ssh "${SSH_OPTS[@]}" "${PROX_USER}@${NODE_IP}" "$@"; }
node_scp() { sshpass -e scp "${SSH_OPTS[@]}" "$1" "${PROX_USER}@${NODE_IP}:$2"; }

# --------------------------------------------------------------------------
# 1. Prompt for Proxmox connection details
# --------------------------------------------------------------------------
prompt_connection() {
  hr
  info "${BOLD}Step 1: Proxmox connection${RESET}"
  read -r -p "Proxmox host IP/FQDN: " PROX_IP
  [[ -n "$PROX_IP" ]] || die "Proxmox host is required."
  read -r -p "Proxmox SSH username [root]: " PROX_USER
  PROX_USER="${PROX_USER:-root}"
  read -r -s -p "Proxmox password for ${PROX_USER}: " SSHPASS
  echo
  [[ -n "$SSHPASS" ]] || die "Password is required."
  export SSHPASS
}

# --------------------------------------------------------------------------
# 2. Confirm connectivity before doing anything else
# --------------------------------------------------------------------------
confirm_connectivity() {
  hr
  info "${BOLD}Step 2: Confirming connectivity to ${PROX_IP}${RESET}"

  if command -v ping >/dev/null 2>&1; then
    if ping -c1 -W2 "$PROX_IP" >/dev/null 2>&1; then
      ok "  Ping OK."
    else
      warn "  Ping failed (ICMP may be blocked) - continuing to SSH test."
    fi
  fi

  local ver
  if ! ver="$(prox_ssh 'pveversion' 2>/dev/null)"; then
    die "Could not SSH to ${PROX_USER}@${PROX_IP} or it is not a Proxmox host. Check IP/credentials and that SSH (22) is reachable."
  fi
  ok "  SSH + Proxmox OK: ${ver}"
}

# --------------------------------------------------------------------------
# 3 + 4. Select node, resolve its IP, select storage
# --------------------------------------------------------------------------
select_node() {
  hr
  info "${BOLD}Step 3: Choose the Proxmox node to deploy the deployer to${RESET}"
  local nodes_json
  nodes_json="$(prox_ssh 'pvesh get /nodes --output-format json' 2>/dev/null)" \
    || die "Failed to query cluster nodes."

  mapfile -t NODES < <(printf '%s' "$nodes_json" | jq -r '.[] | "\(.node)\t\(.status)"')
  (( ${#NODES[@]} > 0 )) || die "No nodes returned from Proxmox."

  local i=1
  for entry in "${NODES[@]}"; do
    printf "   %s) %s ${DIM}(%s)${RESET}\n" "$i" "${entry%%$'\t'*}" "${entry##*$'\t'}"
    ((i++))
  done
  local sel
  sel="$(read_choice "Select node [1-${#NODES[@]}]: " "${#NODES[@]}")"
  NODE="${NODES[$((sel-1))]%%$'\t'*}"
  ok "  Selected node: ${NODE}"

  # Resolve the chosen node's IP for scp/pct (it may differ from the entry host).
  local entry_host
  entry_host="$(prox_ssh 'hostname' 2>/dev/null || true)"
  if [[ "$NODE" == "$entry_host" ]]; then
    NODE_IP="$PROX_IP"
  else
    local status_json
    status_json="$(prox_ssh 'pvesh get /cluster/status --output-format json' 2>/dev/null)" || true
    NODE_IP="$(printf '%s' "$status_json" | jq -r --arg n "$NODE" '.[] | select(.type=="node" and .name==$n) | .ip' 2>/dev/null | head -n1)"
    [[ -n "$NODE_IP" && "$NODE_IP" != "null" ]] || die "Could not resolve an IP for node '${NODE}'. Is it online and in the cluster?"
  fi
  info "  Node '${NODE}' address: ${NODE_IP}"
}

select_storage() {
  hr
  info "${BOLD}Step 4: Choose the storage on '${NODE}' for the deployer rootfs${RESET}"
  local stor_json
  stor_json="$(prox_ssh "pvesh get /nodes/${NODE}/storage --content rootdir --output-format json" 2>/dev/null)" \
    || die "Failed to query storages on node ${NODE}."

  mapfile -t STORS < <(printf '%s' "$stor_json" \
    | jq -r '.[] | select((.active // 1)==1) | "\(.storage)\t\(((.avail // 0)/1073741824)|floor)"')
  (( ${#STORS[@]} > 0 )) || die "No container-capable (rootdir) storages found on node ${NODE}."

  local i=1
  for entry in "${STORS[@]}"; do
    printf "   %s) %s ${DIM}(%s GiB free)${RESET}\n" "$i" "${entry%%$'\t'*}" "${entry##*$'\t'}"
    ((i++))
  done
  local sel
  sel="$(read_choice "Select storage [1-${#STORS[@]}]: " "${#STORS[@]}")"
  STORAGE="${STORS[$((sel-1))]%%$'\t'*}"
  ok "  Selected storage: ${STORAGE}"
}

# --------------------------------------------------------------------------
# 5. Push + restore + start, then print finishing instructions
# --------------------------------------------------------------------------
deploy_deployer() {
  hr
  info "${BOLD}Step 5: Pushing and starting the deployer${RESET}"

  VMID="$(prox_ssh 'pvesh get /cluster/nextid' 2>/dev/null | tr -dc '0-9')"
  [[ -n "$VMID" ]] || die "Could not obtain a free VMID from Proxmox."

  local tarball_base remote_path tarball_size
  tarball_base="$(basename "$TARBALL")"
  remote_path="/var/lib/vz/dump/${tarball_base}"
  tarball_size="$(stat -c%s "$TARBALL" 2>/dev/null || echo 0)"

  printf '\n'
  info "About to deploy:"
  printf '   Tarball ...... %s (%s)\n' "$TARBALL" "$(du -h "$TARBALL" | cut -f1)"
  printf '   Node ......... %s (%s)\n' "$NODE" "$NODE_IP"
  printf '   Storage ...... %s\n' "$STORAGE"
  printf '   New VMID ..... %s\n' "$VMID"
  printf '   Hostname ..... %s\n' "$DEPLOYER_HOSTNAME"
  printf '\n'
  read -r -p "Proceed? [y/N]: " confirm
  [[ "$confirm" =~ ^[Yy]$ ]] || { warn "Aborted by user."; exit 0; }

  info "  Ensuring upload directory exists on ${NODE}..."
  node_ssh "mkdir -p /var/lib/vz/dump"

  # Space check on the upload filesystem.
  local avail
  avail="$(node_ssh "df -B1 --output=avail /var/lib/vz/dump | tail -1 | tr -dc '0-9'" 2>/dev/null || echo 0)"
  if (( avail > 0 && tarball_size > 0 && avail < tarball_size )); then
    die "Not enough space in /var/lib/vz/dump on ${NODE}: need $((tarball_size/1073741824)) GiB, have $((avail/1073741824)) GiB."
  fi

  info "  Copying tarball to ${NODE}:${remote_path} (this can take a while for large images)..."
  node_scp "$TARBALL" "$remote_path"
  ok "  Upload complete."

  info "  Restoring LXC ${VMID} from the tarball onto storage '${STORAGE}'..."
  node_ssh "pct restore ${VMID} ${remote_path} --storage ${STORAGE} --hostname ${DEPLOYER_HOSTNAME}"
  ok "  Restore complete."

  # Make sure the restored network bridge exists on this node, otherwise the
  # container cannot start. The real network is configured later by offline-setup.
  # (All JSON parsing happens locally; Proxmox nodes do not ship jq.)
  local cur_bridge net_json bridge_exists
  cur_bridge="$(node_ssh "pct config ${VMID}" 2>/dev/null | sed -n 's/^net0:.*bridge=\([^,]*\).*/\1/p' | head -n1 || true)"
  if [[ -n "$cur_bridge" ]]; then
    net_json="$(prox_ssh "pvesh get /nodes/${NODE}/network --type any_bridge --output-format json" 2>/dev/null || true)"
    bridge_exists="$(printf '%s' "$net_json" | jq -r --arg b "$cur_bridge" 'map(.iface)|index($b) // empty' 2>/dev/null || true)"
    if [[ -z "$bridge_exists" ]]; then
      warn "  Restored bridge '${cur_bridge}' does not exist on ${NODE}."
      mapfile -t BRIDGES < <(printf '%s' "$net_json" | jq -r '.[].iface')
      (( ${#BRIDGES[@]} > 0 )) || die "No bridges available on ${NODE} to attach the deployer to."
      info "  Choose a bridge to attach the deployer to (offline-setup will set the final IP):"
      local i=1
      for b in "${BRIDGES[@]}"; do printf '   %s) %s\n' "$i" "$b"; ((i++)); done
      local bsel
      bsel="$(read_choice "Select bridge [1-${#BRIDGES[@]}]: " "${#BRIDGES[@]}")"
      local chosen_bridge="${BRIDGES[$((bsel-1))]}"
      node_ssh "pct set ${VMID} --net0 name=eth0,bridge=${chosen_bridge},ip=dhcp"
      ok "  Attached deployer to bridge '${chosen_bridge}' (DHCP for now)."
    fi
  fi

  info "  Starting the deployer..."
  node_ssh "pct start ${VMID}"
  ok "  Deployer is starting."

  print_final_instructions
}

print_final_instructions() {
  printf '\n'
  hr
  printf '%s\n' "${GREEN}${BOLD}  DEPLOYER DEPLOYED - finish setup from the Proxmox console.${RESET}"
  hr
  cat <<EOF

The deployer LXC is now running on your offline Proxmox:

  Node .............. ${NODE}  (${NODE_IP})
  VMID .............. ${VMID}
  Hostname .......... ${DEPLOYER_HOSTNAME}

HOW TO FINISH (run the offline setup TUI on the deployer):

  Option A - Proxmox web console (recommended in the field):
    1) Open the Proxmox web UI:  https://${PROX_IP}:8006
    2) In the left tree, select node '${NODE}' -> CT ${VMID} (${DEPLOYER_HOSTNAME}).
    3) Click '>_ Console', log in as root, then run the offline setup TUI:

         ${OFFLINE_TUI_PATH}

  Option B - directly from this Proxmox host over SSH:

         ssh ${PROX_USER}@${NODE_IP} "pct exec ${VMID} -- ${OFFLINE_TUI_PATH}"

The offline setup TUI is located on the deployer at:

  ${OFFLINE_TUI_PATH}

It will configure the deployer's offline network (IP/DHCP/DNS) and, if you
choose, the domain-join settings. After it finishes, the deployer serves
PXE/WinPE + deploy.wim on your offline network and is ready to image
workstations - no rebuild needed (it addresses itself by hostname).

NOTE: The uploaded tarball is still on the node at:
  ${NODE_IP}:/var/lib/vz/dump/$(basename "$TARBALL")
You can delete it once you have confirmed the deployer works.

EOF
  hr
}

# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
main() {
  hr
  printf '%s\n' "${BOLD}  Offline Deployer Field Deployment${RESET}"
  printf '%s\n' "${DIM}  Pushes the exported deployer LXC onto an offline Proxmox host and starts it.${RESET}"
  require_tools
  discover_tarball
  info "Using tarball: ${TARBALL}"
  prompt_connection
  confirm_connectivity
  select_node
  select_storage
  deploy_deployer
}

main "$@"
