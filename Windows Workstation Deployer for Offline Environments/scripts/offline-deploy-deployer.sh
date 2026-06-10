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
  # Optional: pv gives a nicer upload progress bar; scp's own meter is the fallback.
  command -v pv >/dev/null 2>&1 || warn "Tip: install 'pv' for a richer upload progress bar (apt/dnf install pv). Falling back to scp's built-in meter."
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

# Upload a (potentially very large) local file to NODE_IP:dest with a live
# progress bar + transfer rate. Prefers `pv` for a rich bar (percent, rate, ETA);
# otherwise falls back to scp, whose own progress meter also shows size/rate/ETA.
node_upload() {
  local src="$1" dest="$2"
  if command -v pv >/dev/null 2>&1; then
    local size
    size="$(stat -c%s "$src" 2>/dev/null || echo 0)"
    # pv streams the file through ssh; `cat` writes it on the node. pipefail
    # (set -o pipefail) ensures a mid-transfer failure aborts the script.
    if (( size > 0 )); then
      pv -pterab -s "$size" "$src" | sshpass -e ssh "${SSH_OPTS[@]}" "${PROX_USER}@${NODE_IP}" "cat > '${dest}'"
    else
      pv -pterab "$src" | sshpass -e ssh "${SSH_OPTS[@]}" "${PROX_USER}@${NODE_IP}" "cat > '${dest}'"
    fi
  else
    sshpass -e scp "${SSH_OPTS[@]}" "$src" "${PROX_USER}@${NODE_IP}:${dest}"
  fi
}

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

# Let the user choose the temporary staging filesystem for the tarball. The
# selected *restore* storage (e.g. a ZFS/LVM pool) usually is not a plain
# directory we can scp into, so the tarball needs a staging path on a filesystem
# that actually has room. Sets UPLOAD_DIR and UPLOAD_AVAIL.
# Args: $1 = bytes needed.
select_staging() {
  local need="$1" df_out line avail mount
  hr
  info "${BOLD}Step 5: Choose where to stage the tarball on '${NODE}'${RESET}"
  printf "%s\n" "${DIM}  This is a temporary copy used only for the restore, then deleted.${RESET}"
  # All filesystem parsing is done locally; Proxmox nodes do not ship jq, but df
  # is always present. -P gives stable single-line columns; -B1 = bytes.
  df_out="$(node_ssh "df -PB1 -x tmpfs -x devtmpfs -x overlay -x squashfs 2>/dev/null | tail -n +2" 2>/dev/null || true)"

  local mounts=() avails=()
  while IFS= read -r line; do
    [[ -n "$line" ]] || continue
    avail="$(awk '{print $4}' <<<"$line")"
    # Mount point is column 6 onward (may legitimately contain spaces).
    mount="$(awk '{out=$6; for(i=7;i<=NF;i++) out=out" "$i; print out}' <<<"$line")"
    [[ "$avail" =~ ^[0-9]+$ && -n "$mount" ]] || continue
    mounts+=("$mount"); avails+=("$avail")
  done <<<"$df_out"
  (( ${#mounts[@]} > 0 )) || die "Could not enumerate filesystems on ${NODE}."

  local i fits
  for (( i=0; i<${#mounts[@]}; i++ )); do
    if (( need > 0 && avails[i] < need )); then fits="${RED}too small${RESET}"; else fits="${GREEN}fits${RESET}"; fi
    printf "   %s) %s ${DIM}(%s GiB free)${RESET} - %s\n" "$((i+1))" "${mounts[i]}" "$((avails[i]/1073741824))" "$fits"
  done

  while true; do
    local sel
    sel="$(read_choice "Select staging filesystem [1-${#mounts[@]}]: " "${#mounts[@]}")"
    local idx=$((sel-1))
    if (( need > 0 && avails[idx] < need )); then
      err "That filesystem only has $((avails[idx]/1073741824)) GiB free; the tarball needs $((need/1073741824)) GiB. Pick another."
      continue
    fi
    UPLOAD_DIR="${mounts[idx]}"
    UPLOAD_AVAIL="${avails[idx]}"
    break
  done
  ok "  Staging filesystem: ${UPLOAD_DIR} ($((UPLOAD_AVAIL/1073741824)) GiB free)"
}

# --------------------------------------------------------------------------
# 6. Push + restore + start, then print finishing instructions
# --------------------------------------------------------------------------
deploy_deployer() {
  local tarball_base remote_path tarball_size
  tarball_base="$(basename "$TARBALL")"
  tarball_size="$(stat -c%s "$TARBALL" 2>/dev/null || echo 0)"

  # Let the user choose where to stage the tarball (the chosen restore storage is
  # often a pool we can't scp a file into).
  select_staging "$tarball_size"
  local upload_dir="${UPLOAD_DIR%/}/deployer-staging"
  remote_path="${upload_dir}/${tarball_base}"

  hr
  info "${BOLD}Step 6: Pushing and starting the deployer${RESET}"

  VMID="$(prox_ssh 'pvesh get /cluster/nextid' 2>/dev/null | tr -dc '0-9')"
  [[ -n "$VMID" ]] || die "Could not obtain a free VMID from Proxmox."

  printf '\n'
  info "About to deploy:"
  printf '   Tarball ...... %s (%s)\n' "$TARBALL" "$(du -h "$TARBALL" | cut -f1)"
  printf '   Node ......... %s (%s)\n' "$NODE" "$NODE_IP"
  printf '   Restore to ... %s\n' "$STORAGE"
  printf "   Staging at ... %s ${DIM}(%s GiB free, temporary - deleted after restore)${RESET}\n" "$upload_dir" "$((UPLOAD_AVAIL/1073741824))"
  printf '   New VMID ..... %s\n' "$VMID"
  printf '   Hostname ..... %s\n' "$DEPLOYER_HOSTNAME"
  printf '\n'
  read -r -p "Proceed? [y/N]: " confirm
  [[ "$confirm" =~ ^[Yy]$ ]] || { warn "Aborted by user."; exit 0; }

  info "  Ensuring staging directory exists on ${NODE}..."
  node_ssh "mkdir -p '${upload_dir}'"

  info "  Copying tarball to ${NODE}:${remote_path} (this can take a while for large images)..."
  node_upload "$TARBALL" "$remote_path"
  ok "  Upload complete."

  info "  Restoring LXC ${VMID} from the tarball onto storage '${STORAGE}'..."
  node_ssh "pct restore ${VMID} ${remote_path} --storage ${STORAGE} --hostname ${DEPLOYER_HOSTNAME}"
  ok "  Restore complete."

  # The tarball was only needed for the restore; reclaim the staging space now.
  info "  Cleaning up the staged tarball on ${NODE}..."
  node_ssh "rm -f '${remote_path}'; rmdir '${upload_dir}' 2>/dev/null || true" || warn "  Could not remove staged tarball at ${remote_path}; delete it manually if needed."

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

  Option B - over SSH (the -t is REQUIRED so the TUI gets a real terminal;
            without it the screen fills with escape codes and the mouse/keys
            do not work):

         ssh -t ${PROX_USER}@${NODE_IP} "pct exec ${VMID} -- ${OFFLINE_TUI_PATH}"

The offline setup TUI is located on the deployer at:

  ${OFFLINE_TUI_PATH}

It will configure the deployer's offline network (IP/DHCP/DNS) and, if you
choose, the domain-join settings. After it finishes, the deployer serves
PXE/WinPE + deploy.wim on your offline network and is ready to image
workstations - no rebuild needed (it addresses itself by hostname).

NOTE: The staged tarball was removed from the node after the restore; the
deployer now lives on storage '${STORAGE}'. Your local copy of the tarball is
untouched.

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
