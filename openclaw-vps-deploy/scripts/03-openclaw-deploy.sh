#!/bin/bash
# OpenClaw VPS Setup - Step 3: OpenClaw Deployment
# Clones repo, builds Docker image, runs onboarding

set -e

# Arguments (passed by agent or set manually)
OLLAMA_API_KEY="${OLLAMA_API_KEY:-}"

echo "=== Step 3: OpenClaw Deployment ==="

# Switch to openclaw user context
cd /home/openclaw

# Create directories
echo "Creating directories..."
mkdir -p /home/openclaw/.openclaw/workspace
chown -R openclaw:openclaw /home/openclaw/.openclaw
chmod -R 755 /home/openclaw/.openclaw

# Clone repository
echo "Cloning OpenClaw repository..."
if [ -d "/home/openclaw/openclaw-repo" ]; then
    echo "Repository already exists, pulling latest..."
    cd /home/openclaw/openclaw-repo
    su - openclaw -c "cd /home/openclaw/openclaw-repo && git pull"
else
    su - openclaw -c "git clone https://github.com/openclaw/openclaw.git /home/openclaw/openclaw-repo"
    cd /home/openclaw/openclaw-repo
fi

# Fix ownership
chown -R openclaw:openclaw /home/openclaw/openclaw-repo

# Store Ollama API key
if [ -n "$OLLAMA_API_KEY" ]; then
    echo "Storing Ollama API key..."
    su - openclaw -c "mkdir -p /home/openclaw/.openclaw"
    su - openclaw -c "echo 'OLLAMA_API_KEY=$OLLAMA_API_KEY' >> /home/openclaw/.openclaw/.env"
    chmod 600 /home/openclaw/.openclaw/.env
fi

# Run docker-setup.sh
echo "Running docker-setup.sh..."
echo "This will start the onboarding wizard..."
cd /home/openclaw/openclaw-repo

# Note: docker-setup.sh is interactive, agent should handle this differently
# For automated setup, we'll create config manually and start gateway

echo ""
echo "=== Step 3 Complete ==="
echo "Repository cloned to: /home/openclaw/openclaw-repo"
echo ""
echo "Next: Run docker-setup.sh or configure manually with 04-post-setup.sh"
echo ""
