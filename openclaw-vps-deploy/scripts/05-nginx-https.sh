#!/bin/bash
# OpenClaw VPS Setup - Step 5: Nginx + HTTPS (Optional)
# Sets up Nginx reverse proxy with Let's Encrypt SSL

set -e

# Arguments
DOMAIN="${DOMAIN:-}"
EMAIL="${EMAIL:-}"

if [ -z "$DOMAIN" ]; then
    echo "No domain provided, skipping Nginx setup..."
    echo "Access will be via SSH tunnel only:"
    echo "  ssh -L 18789:127.0.0.1:18789 openclaw@<IP>"
    exit 0
fi

echo "=== Step 5: Nginx + HTTPS Setup ==="
echo "Domain: $DOMAIN"

# Install Nginx
echo "Installing Nginx..."
apt install -y nginx

# Create Nginx config
echo "Creating Nginx configuration..."
cat > /etc/nginx/sites-available/openclaw << NGINX_CONFIG
server {
    listen 80;
    server_name $DOMAIN;
    return 301 https://\$server_name\$request_uri;
}

server {
    listen 443 ssl http2;
    server_name $DOMAIN;

    ssl_certificate /etc/letsencrypt/live/$DOMAIN/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$DOMAIN/privkey.pem;

    # Security headers
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;

    location / {
        proxy_pass http://127.0.0.1:18789;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;

        # WebSocket support
        proxy_read_timeout 86400;
    }
}
NGINX_CONFIG

# Enable site
ln -sf /etc/nginx/sites-available/openclaw /etc/nginx/sites-enabled/

# Test config
nginx -t

# Install Certbot
echo "Installing Certbot..."
apt install -y certbot python3-certbot-nginx

# Obtain SSL certificate
echo "Obtaining SSL certificate..."
if [ -n "$EMAIL" ]; then
    certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --email "$EMAIL"
else
    certbot --nginx -d "$DOMAIN" --non-interactive --agree-tos --register-unsafely-without-email
fi

# Reload Nginx
systemctl reload nginx

# Test auto-renewal
certbot renew --dry-run

echo ""
echo "=== Step 5 Complete ==="
echo "Nginx configured with HTTPS"
echo "Control UI: https://$DOMAIN"
echo ""
echo "✅ SSL certificate installed"
echo "✅ Auto-renewal configured"
echo ""
