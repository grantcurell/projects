#!/usr/bin/env bash
set -euo pipefail

source .env

TRINO="./bin/trino"
SERVER="http://localhost:${TRINO_HOST_PORT}"
USER="demo"

get_count() {
  local sql="$1"
  "$TRINO" \
    --server "$SERVER" \
    --user "$USER" \
    --output-format CSV \
    --execute "$sql" \
    | tr -d '"\r\n '
}

crm_count="$(get_count "SELECT count(*) FROM crm.public.customers")"
webapp_count="$(get_count "SELECT count(*) FROM webapp.appdb.user_profiles")"
accepted_count="$(get_count "SELECT count(*) FROM governed.public.customer_standard")"
rejected_count="$(get_count "SELECT count(*) FROM governed.public.customer_rejects")"
iceberg_accepted_count="$(get_count "SELECT count(*) FROM iceberg.governed.customer_standard")"
iceberg_rejected_count="$(get_count "SELECT count(*) FROM iceberg.governed.customer_rejects")"

echo "CRM source rows:              $crm_count"
echo "WebApp source rows:           $webapp_count"
echo "Accepted governed rows:       $accepted_count"
echo "Rejected governed rows:       $rejected_count"
echo "Accepted Iceberg rows:        $iceberg_accepted_count"
echo "Rejected Iceberg rows:        $iceberg_rejected_count"

if [ "$crm_count" != "6" ]; then
  echo "ERROR: expected 6 CRM rows, got $crm_count"
  exit 1
fi

if [ "$webapp_count" != "7" ]; then
  echo "ERROR: expected 7 WebApp rows, got $webapp_count"
  exit 1
fi

if [ "$accepted_count" != "4" ]; then
  echo "ERROR: expected 4 accepted rows, got $accepted_count"
  exit 1
fi

if [ "$rejected_count" != "9" ]; then
  echo "ERROR: expected 9 rejected rows, got $rejected_count"
  exit 1
fi

if [ "$iceberg_accepted_count" != "4" ]; then
  echo "ERROR: expected 4 accepted Iceberg rows, got $iceberg_accepted_count"
  exit 1
fi

if [ "$iceberg_rejected_count" != "9" ]; then
  echo "ERROR: expected 9 rejected Iceberg rows, got $iceberg_rejected_count"
  exit 1
fi

echo "All expected counts passed."
