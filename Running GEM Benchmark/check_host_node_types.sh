#!/usr/bin/env bash
###############################################################################
# group_node_hardware.sh  –  Group node001‑node023 by identical CPU & memory
# Works on Bash 5 (RHEL 9.5).  Requires password‑less SSH keys.
###############################################################################

HOST_PREFIX="node"
START=1
END=23
MAX_PARALLEL=10
SSH_OPTS="-o BatchMode=yes -o ConnectTimeout=5"

TMPDIR=$(mktemp -d)
LINEFILE="$TMPDIR/hw_lines.txt"

limiter() {                           # simple semaphore
  while [ "$(jobs -pr | wc -l)" -ge "$MAX_PARALLEL" ]; do
    sleep 0.1
  done
}

collect_one() {                       # $1 = host
  local host="$1" outfile="$TMPDIR/${host}.line"

  ssh $SSH_OPTS "$host" 'bash -s' <<'REMOTE' 2>/dev/null >"$outfile"
cpu=$(lscpu | awk -F':' '/Model name/ {gsub(/^[[:space:]]+/,"",$2); print $2; exit}')
cores=$(lscpu | awk '/^CPU\(s\):/ {print $2; exit}')
mem=$(free -m | awk '/^Mem:/ {print $2; exit}')
printf "%s\t%s\t%s\t%s\n" "$HOSTNAME" "$cpu" "$cores" "$mem"
REMOTE

  [[ $? -ne 0 ]] && echo -e "${host}\tUNREACHABLE\t-\t-" >"$outfile"
}

# ── launch jobs with correct 3‑digit padding ────────────────────────────────
for n in $(seq $START $END); do
  host="${HOST_PREFIX}$(printf "%03d" "$n")"
  limiter
  collect_one "$host" &
done
wait

cat "$TMPDIR"/*.line >"$LINEFILE"

# ── group & report ───────────────────────────────────────────────────────────
echo -e "\n========== NODE GROUPS (CPU | CORES | MEM_MB) =========="

awk -F'\t' '
$2!="UNREACHABLE" {
    key = $2 " | " $3 " cores | " $4 "MB"
    nodes[key] = nodes[key] " " $1
}
END {
    for (k in nodes) {
        print "-----------------------------"
        print "Hardware Signature: " k
        print "Nodes:" nodes[k]
    }
}
' "$LINEFILE"

echo -e "\n========== UNREACHABLE NODES =========="
awk -F'\t' '$2=="UNREACHABLE" {print $1}' "$LINEFILE"

rm -rf "$TMPDIR"
