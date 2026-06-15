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

echo "Publishing governed Postgres outputs to Iceberg tables..."

run_sql "CREATE SCHEMA IF NOT EXISTS iceberg.governed"

run_sql "DROP TABLE IF EXISTS iceberg.governed.customer_standard"
run_sql "
CREATE TABLE iceberg.governed.customer_standard AS
SELECT
  customer_id,
  email,
  created_at,
  country,
  status,
  source_system,
  ingested_at
FROM governed.public.customer_standard
"

run_sql "DROP TABLE IF EXISTS iceberg.governed.customer_rejects"
run_sql "
CREATE TABLE iceberg.governed.customer_rejects AS
SELECT
  reject_id,
  customer_id,
  email,
  created_at,
  country,
  status,
  source_system,
  ingested_at,
  rejection_reasons,
  original_payload,
  rejected_at
FROM governed.public.customer_rejects
"

echo "Iceberg governed tables synced."
