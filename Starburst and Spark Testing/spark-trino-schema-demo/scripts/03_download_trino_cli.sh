#!/usr/bin/env bash
set -euo pipefail

source .env

mkdir -p bin

CLI_PATH="bin/trino"
CLI_URL="https://github.com/trinodb/trino/releases/download/${TRINO_CLIENT_VERSION}/trino-cli-${TRINO_CLIENT_VERSION}"

echo "Downloading Trino CLI ${TRINO_CLIENT_VERSION} from:"
echo "$CLI_URL"

curl -fsSL -o "$CLI_PATH" "$CLI_URL"
chmod +x "$CLI_PATH"

echo "Trino CLI installed:"
"$CLI_PATH" --version
