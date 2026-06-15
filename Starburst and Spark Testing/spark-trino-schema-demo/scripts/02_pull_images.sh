#!/usr/bin/env bash
set -euo pipefail

source .env

IMAGES=(
  "$TRINO_IMAGE"
  "$SPARK_IMAGE"
  "$POSTGRES_IMAGE"
  "$MYSQL_IMAGE"
)

echo "Pulling Docker images..."

for image in "${IMAGES[@]}"; do
  echo "Pulling ${image}..."
  if ! docker pull "$image"; then
    echo "ERROR: Failed to pull image: ${image}"
    exit 1
  fi
done

echo "All images pulled successfully."
