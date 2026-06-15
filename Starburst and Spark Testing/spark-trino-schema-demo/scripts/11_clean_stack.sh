#!/usr/bin/env bash
set -euo pipefail

docker compose down -v --remove-orphans
rm -rf data/iceberg

echo "Stack removed, including volumes and local Iceberg warehouse data."
