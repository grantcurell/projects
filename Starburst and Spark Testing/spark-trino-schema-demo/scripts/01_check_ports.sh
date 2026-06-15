#!/usr/bin/env bash
set -euo pipefail

source .env

PORTS=(
  "$TRINO_HOST_PORT"
  "$SPARK_MASTER_UI_PORT"
  "$SPARK_WORKER_UI_PORT"
  "7077"
  "$CRM_POSTGRES_HOST_PORT"
  "$GOVERNED_POSTGRES_HOST_PORT"
  "$MYSQL_HOST_PORT"
)

echo "Checking required ports..."

for port in "${PORTS[@]}"; do
  if ss -ltn | awk '{print $4}' | grep -Eq "(:|\\])${port}$"; then
    echo "ERROR: Port ${port} is already in use."
    echo "Find the process with: sudo lsof -i :${port}"
    exit 1
  fi
done

echo "All required ports are available."
