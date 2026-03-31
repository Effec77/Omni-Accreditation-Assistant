#!/bin/bash

###############################################################################
# Update Script for Accreditation Copilot
# Pulls latest code and redeploys with zero downtime
###############################################################################

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
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

# Check if git repo
if [ ! -d ".git" ]; then
    log_error "Not a git repository"
    exit 1
fi

log_info "Starting update process..."

# Create backup before update
log_info "Creating backup..."
./backup.sh

# Stash any local changes
log_info "Stashing local changes..."
git stash

# Pull latest code
log_info "Pulling latest code..."
BRANCH=$(git rev-parse --abbrev-ref HEAD)
log_info "Current branch: $BRANCH"

git pull origin $BRANCH

# Pop stashed changes if any
git stash pop 2>/dev/null || log_info "No stashed changes to restore"

# Rebuild images
log_info "Rebuilding Docker images..."
docker-compose build --no-cache

# Rolling update (zero downtime)
log_info "Performing rolling update..."

# Update backend
log_info "Updating backend..."
docker-compose up -d --no-deps --build backend

# Wait for backend to be healthy
log_info "Waiting for backend to be healthy..."
for i in {1..30}; do
    if curl -f http://localhost:8000/health &> /dev/null; then
        log_info "Backend is healthy"
        break
    fi
    if [ $i -eq 30 ]; then
        log_error "Backend failed to start"
        log_error "Rolling back..."
        docker-compose down
        docker-compose up -d
        exit 1
    fi
    sleep 2
done

# Update frontend
log_info "Updating frontend..."
docker-compose up -d --no-deps --build frontend

# Wait for frontend to be healthy
log_info "Waiting for frontend to be healthy..."
for i in {1..30}; do
    if curl -f http://localhost:3000 &> /dev/null; then
        log_info "Frontend is healthy"
        break
    fi
    if [ $i -eq 30 ]; then
        log_error "Frontend failed to start"
        log_error "Rolling back..."
        docker-compose down
        docker-compose up -d
        exit 1
    fi
    sleep 2
done

# Update nginx if needed
log_info "Updating nginx..."
docker-compose up -d --no-deps nginx

# Cleanup
log_info "Cleaning up old images..."
docker image prune -f

# Show status
log_info "Update completed successfully!"
log_info "Current status:"
docker-compose ps

# Show recent logs
log_info "Recent logs:"
docker-compose logs --tail=20
