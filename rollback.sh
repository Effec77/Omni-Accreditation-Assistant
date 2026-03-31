#!/bin/bash

###############################################################################
# Rollback Script for Accreditation Copilot
# Restores from the most recent backup
###############################################################################

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

BACKUP_DIR="$HOME/backups"

# Check if backup directory exists
if [ ! -d "$BACKUP_DIR" ]; then
    log_error "Backup directory not found: $BACKUP_DIR"
    exit 1
fi

# List available backups
log_info "Available backups:"
backups=($(ls -t $BACKUP_DIR/accreditation-copilot_*.tar.gz 2>/dev/null))

if [ ${#backups[@]} -eq 0 ]; then
    log_error "No backups found"
    exit 1
fi

# Display backups with numbers
for i in "${!backups[@]}"; do
    backup_file=$(basename "${backups[$i]}")
    backup_date=$(echo "$backup_file" | sed 's/accreditation-copilot_\(.*\)\.tar\.gz/\1/')
    backup_size=$(du -h "${backups[$i]}" | cut -f1)
    echo "  [$i] $backup_date ($backup_size)"
done

# Ask user to select backup
echo ""
read -p "Select backup number to restore (0 for most recent, or 'q' to quit): " selection

if [ "$selection" = "q" ]; then
    log_info "Rollback cancelled"
    exit 0
fi

# Validate selection
if ! [[ "$selection" =~ ^[0-9]+$ ]] || [ "$selection" -ge ${#backups[@]} ]; then
    log_error "Invalid selection"
    exit 1
fi

BACKUP_FILE="${backups[$selection]}"
log_info "Selected backup: $(basename $BACKUP_FILE)"

# Confirm rollback
echo ""
log_warn "This will:"
log_warn "  1. Stop all running services"
log_warn "  2. Restore data from backup"
log_warn "  3. Restart services"
echo ""
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    log_info "Rollback cancelled"
    exit 0
fi

# Create a backup of current state before rollback
log_info "Creating backup of current state..."
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
CURRENT_BACKUP="$BACKUP_DIR/pre_rollback_${TIMESTAMP}.tar.gz"

tar -czf "$CURRENT_BACKUP" \
    data/ \
    accreditation_copilot/data/ \
    accreditation_copilot/indexes/ \
    2>/dev/null || log_warn "Some directories not found"

log_info "Current state backed up to: $CURRENT_BACKUP"

# Stop services
log_info "Stopping services..."
docker-compose down

# Extract backup
log_info "Extracting backup..."
TEMP_DIR=$(mktemp -d)
tar -xzf "$BACKUP_FILE" -C "$TEMP_DIR"

# Find the extracted directory
EXTRACTED_DIR=$(find "$TEMP_DIR" -maxdepth 1 -type d -name "accreditation-copilot_*" | head -n 1)

if [ -z "$EXTRACTED_DIR" ]; then
    log_error "Failed to find extracted backup directory"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# Restore data
log_info "Restoring data..."

# Restore main data directory
if [ -f "$EXTRACTED_DIR/data.tar.gz" ]; then
    log_info "Restoring data directory..."
    rm -rf data/
    tar -xzf "$EXTRACTED_DIR/data.tar.gz"
fi

# Restore indexes
if [ -f "$EXTRACTED_DIR/indexes.tar.gz" ]; then
    log_info "Restoring indexes..."
    rm -rf accreditation_copilot/indexes/
    tar -xzf "$EXTRACTED_DIR/indexes.tar.gz"
fi

# Restore API indexes
if [ -f "$EXTRACTED_DIR/api_indexes.tar.gz" ]; then
    log_info "Restoring API indexes..."
    rm -rf accreditation_copilot/api/indexes/
    tar -xzf "$EXTRACTED_DIR/api_indexes.tar.gz"
fi

# Restore databases
if [ -f "$EXTRACTED_DIR/databases.tar.gz" ]; then
    log_info "Restoring databases..."
    rm -rf accreditation_copilot/data/
    tar -xzf "$EXTRACTED_DIR/databases.tar.gz"
fi

# Cleanup temp directory
rm -rf "$TEMP_DIR"

# Restart services
log_info "Restarting services..."
docker-compose up -d

# Wait for services to be healthy
log_info "Waiting for services to be healthy..."
sleep 10

# Run health check
log_info "Running health check..."
if ./healthcheck.sh; then
    log_info "Rollback completed successfully!"
else
    log_error "Health check failed after rollback"
    log_error "You may need to investigate further"
    exit 1
fi

log_info "Services restored from backup: $(basename $BACKUP_FILE)"
log_info "Pre-rollback backup saved to: $CURRENT_BACKUP"
