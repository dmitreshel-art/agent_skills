#!/bin/bash
# OpenClaw VPS Setup - Step 2: Docker Installation
# Installs Docker Engine and Docker Compose

set -e

echo "=== Step 2: Docker Installation ==="

# Check if Docker is already installed
if command -v docker &> /dev/null; then
    echo "Docker already installed, skipping..."
    echo "Docker version: $(docker --version)"
    exit 0
fi

# Update packages
echo "Updating packages..."
apt update
apt install -y ca-certificates curl gnupg

# Add Docker GPG key
echo "Adding Docker GPG key..."
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

# Add Docker repository
echo "Adding Docker repository..."
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
echo "Installing Docker..."
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Start Docker
systemctl start docker
systemctl enable docker

# Add openclaw user to docker group
usermod -aG docker openclaw

# Verify installation
echo ""
echo "=== Docker Installation Complete ==="
docker --version
docker compose version

echo ""
echo "✅ Docker installed and running"
echo "User 'openclaw' added to docker group"
echo ""
echo "⚠️  Run 'su - openclaw' to apply group changes"
echo ""
