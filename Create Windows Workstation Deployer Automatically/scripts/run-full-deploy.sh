#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

print_banner() {
  local message="$1"
  printf '\n'
  printf '####################################################################################################\n'
  printf '#                                                                                                  #\n'
  printf '#  %s\n' "$message"
  printf '#                                                                                                  #\n'
  printf '####################################################################################################\n'
  printf '\n'
}

print_banner "Starting full deploy pipeline in non-interactive mode."

cd "$PROJECT_ROOT"

echo
echo "==> Step 1/3: Bootstrapping controller"
"${PROJECT_ROOT}/scripts/bootstrap-controller.sh"

echo
echo "==> Step 2/3: Running preflight"
ansible-playbook -i inventories/windows-deployer/hosts.yml playbooks/00-preflight.yml

echo
echo "==> Step 3/3: Running full deployment pipeline"
ansible-playbook -i inventories/windows-deployer/hosts.yml playbooks/site.yml

echo
echo "Pipeline completed successfully."
