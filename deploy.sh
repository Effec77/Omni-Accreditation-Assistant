#!/bin/bash

###############################################################################
# Deployment Script for Accreditation Copilot on AWS
# This script automates the deployment process
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="accreditation-copilot"
DOCKER_COMPOSE_FILE="docker-compose.yml"
BACKUP_DIR="$HOME/backups"

# Functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check Docker
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed"
        exit 1
    fi
    
    # Check Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed"
        exit 1
    fi
    
    # Check if .env file exists
    if [ ! -f "accreditation_copilot/.env" ]; then
        log_error ".env file not found in accreditation_copilot/"
        log_info "Please copy .env.example to .env and configure it"
        exit 1
    fi
    
    log_info "Prerequisites check passed"
}

create_directories() {
    log_info "Creating necessary directories..."
    
    mkdir -p logs
    mkdir -p logs/nginx
    mkdir -p ssl
    mkdir -p $BACKUP_DIR
    
    log_info "Directories created"
}

backup_data() {
    log_info "Creating backup..."
    
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_FILE="$BACKUP_DIR/${PROJECT_NAME}_${TIMESTAMP}.tar.gz"
    
    if [ -d "data" ] || [ -d "accreditation_copilot/data" ]; then
        tar -czf "$BACKUP_FILE" \
            data/ \
            accreditation_copilot/data/ \
            accreditation_copilot/indexes/ \
            2>/dev/null || true
        
        log_info "Backup created: $BACKUP_FILE"
    else
        log_warn "No data to backup"
    fi
}

stop_services() {
    log_info "Stopping existing services..."
    
    if [ -f "$DOCKER_COMPOSE_FILE" ]; then
        docker-compose down || true
    fi
    
    log_info "Services stopped"
}

build_images() {
    log_info "Building Docker images..."
    
    # Build backend
    log_info "Building backend image..."
    docker build -f Dockerfile.backend -t ${PROJECT_NAME}-backend:latest .
    
    # Build frontend
    log_info "Building frontend image..."
    docker build -f Dockerfile.frontend -t ${PROJECT_NAME}-frontend:latest .
    
    log_info "Images built successfully"
}

start_services() {
    log_info "Starting services..."
    
    docker-compose up -d
    
    log_info "Services started"
}

wait_for_services() {
    log_info "Waiting for services to be healthy..."
    
    # Wait for backend
    log_info "Waiting for backend..."
    for i in {1..30}; do
        if curl -f http://localhost:8000/health &> /dev/null; then
            log_info "Backend is healthy"
            break
        fi
        if [ $i -eq 30 ]; then
            log_error "Backend failed to start"
            docker-compose logs backend
            exit 1
        fi
        sleep 2
    done
    
    # Wait for frontend
    log_info "Waiting for frontend..."
    for i in {1..30}; do
        if curl -f http://localhost:3000 &> /dev/null; then
            log_info "Frontend is healthy"
            break
        fi
        if [ $i -eq 30 ]; then
            log_error "Frontend failed to start"
            docker-compose logs frontend
            exit 1
        fi
        sleep 2
    done
    
    log_info "All services are healthy"
}

show_status() {
    log_info "Service Status:"
    docker-compose ps
    
    echo ""
    log_info "Resource Usage:"
    docker stats --no-stream
    
    echo ""
    log_info "Application URLs:"
    echo "  Frontend: http://localhost:3000"
    echo "  Backend API: http://localhost:8000"
    echo "  API Docs: http://localhost:8000/docs"
    echo "  Health Check: http://localhost:8000/health"
}

cleanup_old_images() {
    log_info "Cleaning up old Docker images..."
    docker image prune -f
    log_info "Cleanup complete"
}

# Main deployment flow
main() {
    log_info "Starting deployment of $PROJECT_NAME..."
    
    check_prerequisites
    create_directories
    backup_data
    stop_services
    build_images
    start_services
    wait_for_services
    show_status
    cleanup_old_images
    
    log_info "Deployment completed successfully!"
    log_info "Access your application at http://localhost:3000"
}

# Run main function
main "$@"
