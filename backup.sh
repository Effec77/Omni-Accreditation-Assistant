#!/bin/bash

###############################################################################
# Backup Script for Accreditation Copilot
# Creates timestamped backups of data, indexes, and databases
###############################################################################

set -e

# Configuration
PROJECT_NAME="accreditation-copilot"
BACKUP_BASE_DIR="$HOME/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="$BACKUP_BASE_DIR/${PROJECT_NAME}_${TIMESTAMP}"
RETENTION_DAYS=7

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

# Create backup directory
mkdir -p "$BACKUP_DIR"

log_info "Starting backup to $BACKUP_DIR"

# Backup data directory
if [ -d "data" ]; then
    log_info "Backing up data directory..."
    tar -czf "$BACKUP_DIR/data.tar.gz" data/
fi

# Backup indexes
if [ -d "accreditation_copilot/indexes" ]; then
    log_info "Backing up indexes..."
    tar -czf "$BACKUP_DIR/indexes.tar.gz" accreditation_copilot/indexes/
fi

# Backup API indexes
if [ -d "accreditation_copilot/api/indexes" ]; then
    log_info "Backing up API indexes..."
    tar -czf "$BACKUP_DIR/api_indexes.tar.gz" accreditation_copilot/api/indexes/
fi

# Backup databases
if [ -d "accreditation_copilot/data" ]; then
    log_info "Backing up databases..."
    tar -czf "$BACKUP_DIR/databases.tar.gz" accreditation_copilot/data/
fi

# Backup environment file (without sensitive data)
if [ -f "accreditation_copilot/.env" ]; then
    log_info "Backing up environment configuration..."
    # Remove sensitive values
    grep -v "API_KEY\|TOKEN\|SECRET\|PASSWORD" accreditation_copilot/.env > "$BACKUP_DIR/env.backup" || true
fi

# Backup Docker volumes (if using named volumes)
log_info "Backing up Docker volumes..."
docker run --rm \
    -v accreditation-copilot_data:/data \
    -v "$BACKUP_DIR":/backup \
    alpine tar -czf /backup/docker_volumes.tar.gz /data 2>/dev/null || log_warn "No Docker volumes to backup"

# Create backup manifest
cat > "$BACKUP_DIR/manifest.txt" << EOF
Backup Created: $(date)
Hostname: $(hostname)
Project: $PROJECT_NAME
Backup Location: $BACKUP_DIR

Contents:
$(ls -lh "$BACKUP_DIR")

Docker Containers:
$(docker ps --format "table {{.Names}}\t{{.Status}}")
EOF

log_info "Backup manifest created"

# Compress entire backup
log_info "Compressing backup..."
cd "$BACKUP_BASE_DIR"
tar -czf "${PROJECT_NAME}_${TIMESTAMP}.tar.gz" "${PROJECT_NAME}_${TIMESTAMP}/"
rm -rf "${PROJECT_NAME}_${TIMESTAMP}/"

BACKUP_FILE="${BACKUP_BASE_DIR}/${PROJECT_NAME}_${TIMESTAMP}.tar.gz"
BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)

log_info "Backup completed: $BACKUP_FILE ($BACKUP_SIZE)"

# Cleanup old backups
log_info "Cleaning up backups older than $RETENTION_DAYS days..."
find "$BACKUP_BASE_DIR" -name "${PROJECT_NAME}_*.tar.gz" -mtime +$RETENTION_DAYS -delete

log_info "Backup process completed successfully"

# Optional: Upload to S3 (uncomment if using AWS S3)
# if command -v aws &> /dev/null; then
#     log_info "Uploading to S3..."
#     aws s3 cp "$BACKUP_FILE" "s3://your-bucket-name/backups/"
#     log_info "Uploaded to S3"
# fi
