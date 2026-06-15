#!/usr/bin/env bash
set -euo pipefail

echo "Installing Ubuntu prerequisites..."

sudo apt-get update
sudo apt-get install -y \
  ca-certificates \
  curl \
  gnupg \
  jq \
  make \
  git \
  openjdk-17-jre \
  lsb-release

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is not installed. Installing Docker Engine from Docker apt repository..."

  sudo install -m 0755 -d /etc/apt/keyrings

  if [ ! -f /etc/apt/keyrings/docker.gpg ]; then
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
      | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
  fi

  sudo chmod a+r /etc/apt/keyrings/docker.gpg

  echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
    | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

  sudo apt-get update
  sudo apt-get install -y \
    docker-ce \
    docker-ce-cli \
    containerd.io \
    docker-buildx-plugin \
    docker-compose-plugin
else
  echo "Docker is already installed."
fi

sudo systemctl enable docker
sudo systemctl start docker

if ! groups "$USER" | grep -q docker; then
  echo "Adding current user to docker group..."
  sudo usermod -aG docker "$USER" || true
  echo "You may need to log out and log back in, or run: newgrp docker"
fi

echo "Versions:"
docker --version || true
docker compose version || true
java --version || true

echo "Prerequisite installation complete."
