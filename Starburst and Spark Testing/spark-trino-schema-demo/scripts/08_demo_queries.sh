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
  local title="$1"
  local sql="$2"

  echo
  echo "================================================================================"
  echo "$title"
  echo "================================================================================"
  echo "$sql"
  echo
  "$TRINO" \
    --server "$SERVER" \
    --user "$USER" \
    --output-format ALIGNED \
    --execute "$sql"
}

run_sql "1. Trino can see all configured catalogs" "
SHOW CATALOGS
"

run_sql "2. Trino reads the PostgreSQL CRM source" "
SELECT *
FROM crm.public.customers
ORDER BY customer_id
"

run_sql "3. Trino reads the MySQL WebApp source" "
SELECT *
FROM webapp.appdb.user_profiles
ORDER BY id
"

run_sql "4. Trino federates both source systems into one logical result" "
SELECT
  source_system,
  customer_id,
  email,
  CAST(created_at AS varchar) AS created_at,
  country,
  status
FROM (
  SELECT
    'CRM' AS source_system,
    CAST(customer_id AS varchar) AS customer_id,
    CAST(email AS varchar) AS email,
    created_at,
    CAST(country AS varchar) AS country,
    CAST(status AS varchar) AS status
  FROM crm.public.customers

  UNION ALL

  SELECT
    'WEBAPP' AS source_system,
    CONCAT('app-', CAST(id AS varchar)) AS customer_id,
    CAST(email_address AS varchar) AS email,
    from_unixtime(signup_epoch) AS created_at,
    CAST(country_code AS varchar) AS country,
    CASE
      WHEN is_active = 1 THEN 'ACTIVE'
      WHEN is_active = 0 THEN 'INACTIVE'
      ELSE NULL
    END AS status
  FROM webapp.appdb.user_profiles
)
ORDER BY source_system, customer_id
"

run_sql "5. Trino queries accepted canonical rows written by Spark" "
SELECT
  customer_id,
  email,
  CAST(created_at AS varchar) AS created_at,
  country,
  status,
  source_system
FROM governed.public.customer_standard
ORDER BY customer_id
"

run_sql "6. Trino queries rejected rows and rejection reasons written by Spark" "
SELECT
  customer_id,
  email,
  CAST(created_at AS varchar) AS created_at,
  country,
  status,
  source_system,
  rejection_reasons
FROM governed.public.customer_rejects
ORDER BY customer_id NULLS LAST, reject_id
"

run_sql "7. Final accepted vs rejected counts" "
SELECT 'accepted' AS result_type, count(*) AS row_count
FROM governed.public.customer_standard
UNION ALL
SELECT 'rejected' AS result_type, count(*) AS row_count
FROM governed.public.customer_rejects
ORDER BY result_type
"

echo
echo "Demo queries completed."
