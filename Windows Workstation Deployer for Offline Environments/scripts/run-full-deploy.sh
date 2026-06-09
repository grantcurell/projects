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
echo "==> Step 1/2: Bootstrapping controller"
"${PROJECT_ROOT}/scripts/bootstrap-controller.sh"

echo
echo "==> Step 2/2: Running the end-to-end automated offline domain-join test"
# offline-test.yml runs preflight, cleans prior-run leftovers, health-checks the
# offline DC/admin fixtures, (optionally) rebuilds artifacts online, restores +
# configures the offline deployer, PXE-installs a workstation, proves the domain
# join from the deployer, and prompts for cleanup on success.
ansible-playbook -i inventories/windows-deployer/hosts.yml playbooks/offline-test.yml

echo
echo "Pipeline completed successfully."
