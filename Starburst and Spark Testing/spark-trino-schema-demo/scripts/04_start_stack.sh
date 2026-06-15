#!/usr/bin/env bash
set -euo pipefail

echo "Starting Spark + Trino schema demo stack..."

docker compose up -d \
  postgres-crm \
  mysql-webapp \
  postgres-governed \
  trino \
  spark-master \
  spark-worker-1

echo "Stack start requested."
echo "Run ./scripts/05_wait_for_stack.sh next."
