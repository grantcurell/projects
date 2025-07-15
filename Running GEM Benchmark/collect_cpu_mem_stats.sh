#!/bin/bash

HOSTS_FILE="$1"
MAX_PARALLEL=20

if [ -z "$HOSTS_FILE" ] || [ ! -f "$HOSTS_FILE" ]; then
    echo "Usage: $0 /path/to/hosts.txt"
    exit 1
fi

TMPDIR=$(mktemp -d)
JOBS=0

SEM(){
    while [ "$(jobs -r | wc -l)" -ge "$MAX_PARALLEL" ]; do
        sleep 0.2
    done
}

for HOST in $(cat "$HOSTS_FILE"); do
    SEM

    {
    ssh -o ConnectTimeout=10 -o BatchMode=yes "$HOST" 'bash -s' <<'EOF' > "$TMPDIR/$HOST.out" 2>/dev/null
TMPFILE=$(mktemp)
/usr/bin/mpstat -P ALL 1 30 > "$TMPFILE"
MEMLINE=$(free -m | awk '/Mem:/ {printf "%d %.2f %d %d", $2, ($3 / $2) * 100, $3, $2}')
awk -v memline="$MEMLINE" -v host="$(hostname)" '
/Average/ && $2 ~ /[0-9]+/ {
    core = $2
    idle = $(NF)
    usage = 100 - idle
    split(memline, mem, " ")
    printf "%-15s %-6s %-12.2f %-12.2f %-d/%d\n", host, core, usage, mem[2], mem[3], mem[4]
}' "$TMPFILE"
rm -f "$TMPFILE"
EOF

    if [ $? -ne 0 ]; then
        echo -e "$HOST\tERROR\tN/A\tN/A\tN/A" > "$TMPDIR/$HOST.out"
    fi
    } &

done

# Wait for all to finish
wait

# Print header
printf "%-15s %-6s %-12s %-12s %-20s\n" "HOST" "CORE" "CPU_Usage(%)" "Mem_Used(%)" "Mem_Used(MB)/Total(MB)"
echo "---------------------------------------------------------------------------------------------"

# Print all output in sorted host order
for HOST in $(cat "$HOSTS_FILE"); do
    if [ -f "$TMPDIR/$HOST.out" ]; then
        cat "$TMPDIR/$HOST.out"
    else
        printf "%-15s %-6s %-12s %-12s %-20s\n" "$HOST" "ERROR" "N/A" "N/A" "N/A"
    fi
done

# Cleanup
rm -rf "$TMPDIR"
