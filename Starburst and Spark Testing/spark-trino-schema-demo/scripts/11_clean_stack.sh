#!/usr/bin/env bash
set -euo pipefail

docker compose down -v --remove-orphans

echo "Stack removed, including volumes."
