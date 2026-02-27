#!/bin/bash
# OpenClaw VPS Setup - Step 6: Backup Configuration (Optional)
# Sets up automated backups

set -e

# Arguments
BACKUP_TYPE="${BACKUP_TYPE:-local}"  # local, remote, none
REMOTE_SERVER="${REMOTE_SERVER:-}"
REMOTE_USER="${REMOTE_USER:-backup}"
BACKUP_DIR="/backup/openclaw"

if [ "$BACKUP_TYPE" = "none" ]; then
    echo "Backup setup skipped."
    exit 0
fi

echo "=== Step 6: Backup Setup ==="
echo "Type: $BACKUP_TYPE"

# Create backup directory
mkdir -p "$BACKUP_DIR"
chown openclaw:openclaw "$BACKUP_DIR"

# Create backup script
cat > /home/openclaw/backup-openclaw.sh << 'BACKUP_SCRIPT'
#!/bin/bash
# OpenClaw Backup Script

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backup/openclaw"
OPENCLAW_DIR="/home/openclaw/.openclaw"
LOG_FILE="/var/log/openclaw-backup.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log "Starting backup..."

# Create backup
mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/openclaw-$DATE.tar.gz" \
    -C /home/openclaw .openclaw \
    --exclude="*.log" \
    --exclude="sessions/*.jsonl" \
    2>/dev/null || log "Warning: Some files excluded"

# Keep only last 7 days
find "$BACKUP_DIR" -name "*.tar.gz" -mtime +7 -delete 2>/dev/null

# Count backups
COUNT=$(ls -1 "$BACKUP_DIR"/*.tar.gz 2>/dev/null | wc -l)
log "Backup complete. Total backups: $COUNT"

echo "Backup saved: $BACKUP_DIR/openclaw-$DATE.tar.gz"
BACKUP_SCRIPT

chmod +x /home/openclaw/backup-openclaw.sh
chown openclaw:openclaw /home/openclaw/backup-openclaw.sh

# Setup based on type
case "$BACKUP_TYPE" in
    local)
        echo "Setting up local backup..."
        
        # Add cron job (daily at 3 AM)
        (crontab -u openclaw -l 2>/dev/null | grep -v "backup-openclaw.sh"; echo "0 3 * * * /home/openclaw/backup-openclaw.sh >> /var/log/openclaw-backup.log 2>&1") | crontab -u openclaw -
        
        # Create log file
        touch /var/log/openclaw-backup.log
        chown openclaw:openclaw /var/log/openclaw-backup.log
        
        echo "✅ Local backup configured (daily at 3 AM)"
        echo "   Backups: $BACKUP_DIR"
        echo "   Log: /var/log/openclaw-backup.log"
        ;;
        
    remote)
        if [ -z "$REMOTE_SERVER" ]; then
            echo "Error: REMOTE_SERVER not specified for remote backup"
            exit 1
        fi
        
        echo "Setting up remote backup to $REMOTE_SERVER..."
        
        # Setup SSH key for backup (if not exists)
        if [ ! -f /home/openclaw/.ssh/backup_key ]; then
            su - openclaw -c "ssh-keygen -t ed25519 -f ~/.ssh/backup_key -N '' -C 'openclaw-backup'"
            echo ""
            echo "⚠️  Add this public key to $REMOTE_SERVER:"
            echo "---"
            cat /home/openclaw/.ssh/backup_key.pub
            echo "---"
        fi
        
        # Create remote backup script
        cat > /home/openclaw/backup-remote.sh << REMOTE_BACKUP
#!/bin/bash
DATE=\$(date +%Y%m%d_%H%M%S)
rsync -avz -e "ssh -i ~/.ssh/backup_key -o StrictHostKeyChecking=no" \\
    /home/openclaw/.openclaw/ \\
    $REMOTE_USER@$REMOTE_SERVER:/backup/openclaw/\\$DATE/
REMOTE_BACKUP
        
        chmod +x /home/openclaw/backup-remote.sh
        chown openclaw:openclaw /home/openclaw/backup-remote.sh
        
        # Add cron job
        (crontab -u openclaw -l 2>/dev/null | grep -v "backup-remote.sh"; echo "0 3 * * * /home/openclaw/backup-remote.sh") | crontab -u openclaw -
        
        echo "✅ Remote backup configured"
        echo "   Target: $REMOTE_USER@$REMOTE_SERVER:/backup/openclaw/"
        ;;
esac

echo ""
echo "=== Step 6 Complete ==="
echo ""
echo "Manual backup: /home/openclaw/backup-openclaw.sh"
echo "View cron: crontab -u openclaw -l"
echo ""
