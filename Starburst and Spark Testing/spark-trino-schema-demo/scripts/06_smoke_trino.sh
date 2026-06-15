#!/usr/bin/env bash
set -euo pipefail

source .env

TRINO="./bin/trino"
SERVER="http://localhost:${TRINO_HOST_PORT}"
USER="demo"

if [ ! -x "$TRINO" ]; then
  echo "ERROR: Trino CLI not found. Run ./scripts/03_download_trino_cli.sh first."
  exit 1
fi

run_sql() {
  local sql="$1"
  echo
  echo "SQL> $sql"
  "$TRINO" --server "$SERVER" --user "$USER" --execute "$sql"
}

run_sql "SHOW CATALOGS"
run_sql "SHOW SCHEMAS FROM crm"
run_sql "SHOW SCHEMAS FROM webapp"
run_sql "SHOW SCHEMAS FROM governed"

run_sql "SELECT count(*) AS crm_rows FROM crm.public.customers"
run_sql "SELECT count(*) AS webapp_rows FROM webapp.appdb.user_profiles"

run_sql "
SELECT source_system, row_count
FROM (
  SELECT 'CRM' AS source_system, count(*) AS row_count FROM crm.public.customers
  UNION ALL
  SELECT 'WEBAPP' AS source_system, count(*) AS row_count FROM webapp.appdb.user_profiles
)
ORDER BY source_system
"

echo
echo "Trino smoke test completed."
