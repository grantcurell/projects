#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[1/5] Installing controller dependencies..."
sudo apt-get update
sudo apt-get install -y python3-pip sshpass git rsync ansible-core smbclient

echo "[2/5] Installing Python packages..."
python3 -m pip install --user --break-system-packages ansible paramiko requests proxmoxer pyyaml textual pywinrm requests-ntlm

echo "[3/5] Installing Ansible collections..."
ansible-galaxy collection install -r requirements.yml

echo "[4/5] Checking required inventory placeholders are replaced..."
PLACEHOLDER_MATCHES="$(grep -R -nE "PUT_WINPE_BUILDER_IP_HERE|PUT_WINPE_BUILDER_PASSWORD_HERE|REPLACE_WITH_PROXMOX_API_TOKEN_SECRET" inventories/windows-deployer || true)"
if [[ -n "$PLACEHOLDER_MATCHES" ]]; then
  echo
  echo "ERROR: Replace all required placeholders before deployment:"
  echo "$PLACEHOLDER_MATCHES"
  exit 1
fi

echo "[5/5] Running Ansible syntax checks..."
ansible-playbook -i inventories/windows-deployer/hosts.yml playbooks/site.yml --syntax-check

echo
echo "Bootstrap complete."
echo "Next command:"
echo "  ansible-playbook -i inventories/windows-deployer/hosts.yml playbooks/site.yml"
