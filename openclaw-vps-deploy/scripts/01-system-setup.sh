#!/bin/bash
# OpenClaw VPS Setup - Step 1: System Hardening
# Creates openclaw user, configures SSH, sets up UFW firewall

set -e

echo "=== Step 1: System Hardening ==="

# 1. Create openclaw user
echo "Creating openclaw user..."
if id "openclaw" &>/dev/null; then
    echo "User openclaw already exists, skipping..."
else
    adduser --disabled-password --gecos "" openclaw
    echo "openclaw:openclaw123" | chpasswd
    echo "Password for openclaw: openclaw123 (CHANGE THIS IMMEDIATELY!)"
fi

# Add to groups
usermod -aG sudo openclaw
usermod -aG docker openclaw 2>/dev/null || true  # docker group may not exist yet

echo "✅ User openclaw created"

# 2. SSH Hardening
echo "Hardening SSH configuration..."

# Backup original config
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup

# Disable password authentication (uncomment or add)
sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sed -i 's/PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config

# Disable root login
sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sed -i 's/PermitRootLogin prohibit-password/PermitRootLogin no/' /etc/ssh/sshd_config

# Restart SSH
systemctl restart sshd

echo "✅ SSH hardened (password auth disabled, root login disabled)"

# 3. UFW Firewall
echo "Setting up UFW firewall..."

ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp

# Enable without prompt
echo "y" | ufw enable

echo "✅ UFW firewall enabled (ports: 22, 80, 443)"

# Summary
echo ""
echo "=== Step 1 Complete ==="
echo "User: openclaw (change password with: passwd openclaw)"
echo "SSH: key-only auth, root login disabled"
echo "Firewall: UFW enabled (22, 80, 443)"
echo ""
echo "⚠️  IMPORTANT: Add your SSH key before logging out!"
echo "Run on your LOCAL machine: ssh-copy-id openclaw@$(curl -s ifconfig.me)"
echo ""
