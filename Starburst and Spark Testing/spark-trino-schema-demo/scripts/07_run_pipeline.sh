#!/usr/bin/env bash
set -euo pipefail

source .env

mkdir -p tmp
exec 9>tmp/pipeline.lock
if ! flock -n 9; then
  echo "ERROR: Another pipeline run is already in progress."
  exit 1
fi

echo "Clearing governed output tables..."
docker exec postgres-governed psql \
  -U "$DEMO_DB_USER" \
  -d "$GOVERNED_POSTGRES_DB" \
  -c "TRUNCATE TABLE public.customer_rejects RESTART IDENTITY; TRUNCATE TABLE public.customer_standard;"

echo "Running Spark schema enforcement job..."
docker compose run --rm spark-submit \
  /opt/spark/bin/spark-submit \
  --master spark://spark-master:7077 \
  --conf spark.task.maxFailures=1 \
  --conf spark.speculation=false \
  --packages io.trino:trino-jdbc:${TRINO_CLIENT_VERSION},org.postgresql:postgresql:${POSTGRES_JDBC_VERSION} \
  /opt/spark-apps/jobs/enforce_customer_schema.py

echo "Syncing governed outputs to Iceberg..."
./scripts/07b_sync_iceberg_governed.sh

echo "Pipeline run completed."
