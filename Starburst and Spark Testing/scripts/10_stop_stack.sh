#!/usr/bin/env bash
set -euo pipefail

docker compose stop

echo "Stack stopped. Data volumes are preserved."
