#!/bin/bash

###############################################################################
# Setup Deployment Package
# Makes all scripts executable and verifies the deployment package
###############################################################################

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
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

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Accreditation Copilot - Deployment Package Setup        ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

log_info "Setting up deployment package..."
echo ""

# Make scripts executable
log_info "Making scripts executable..."
chmod +x deploy.sh
chmod +x update.sh
chmod +x backup.sh
chmod +x rollback.sh
chmod +x monitor.sh
chmod +x healthcheck.sh
log_info "Scripts are now executable"
echo ""

# Verify required files
log_info "Verifying required files..."

REQUIRED_FILES=(
    "Dockerfile.backend"
    "Dockerfile.frontend"
    "docker-compose.yml"
    "nginx.conf"
    ".dockerignore"
    "deploy.sh"
    "update.sh"
    "backup.sh"
    "rollback.sh"
    "monitor.sh"
    "healthcheck.sh"
    "AWS_DEPLOYMENT_GUIDE.md"
    "QUICK_DEPLOY.md"
    "DEPLOYMENT_README.md"
)

MISSING_FILES=0

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "  ${GREEN}✓${NC} $file"
    else
        echo -e "  ${RED}✗${NC} $file (missing)"
        MISSING_FILES=$((MISSING_FILES + 1))
    fi
done

echo ""

if [ $MISSING_FILES -gt 0 ]; then
    log_error "$MISSING_FILES required file(s) missing"
    exit 1
fi

log_info "All required files present"
echo ""

# Check environment file
log_info "Checking environment configuration..."

if [ -f "accreditation_copilot/.env" ]; then
    log_info "Environment file exists"
    
    # Check for placeholder values
    if grep -q "your_key" accreditation_copilot/.env; then
        log_warn "Environment file contains placeholder values"
        log_warn "Please update accreditation_copilot/.env with your actual API keys"
    else
        log_info "Environment file appears configured"
    fi
else
    log_warn "Environment file not found"
    
    if [ -f "accreditation_copilot/.env.example" ]; then
        log_info "Creating .env from .env.example..."
        cp accreditation_copilot/.env.example accreditation_copilot/.env
        log_warn "Please edit accreditation_copilot/.env and add your API keys"
    else
        log_error ".env.example not found"
        exit 1
    fi
fi

echo ""

# Check Docker installation (if on server)
log_info "Checking Docker installation..."

if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version)
    log_info "Docker installed: $DOCKER_VERSION"
else
    log_warn "Docker not installed"
    log_info "Run this on your EC2 instance to install Docker:"
    echo "  curl -fsSL https://get.docker.com -o get-docker.sh"
    echo "  sudo sh get-docker.sh"
    echo "  sudo usermod -aG docker \$USER"
fi

echo ""

if command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version)
    log_info "Docker Compose installed: $COMPOSE_VERSION"
else
    log_warn "Docker Compose not installed"
    log_info "Run this on your EC2 instance to install Docker Compose:"
    echo "  sudo curl -L \"https://github.com/docker/compose/releases/latest/download/docker-compose-\$(uname -s)-\$(uname -m)\" -o /usr/local/bin/docker-compose"
    echo "  sudo chmod +x /usr/local/bin/docker-compose"
fi

echo ""

# Create necessary directories
log_info "Creating necessary directories..."

mkdir -p logs
mkdir -p logs/nginx
mkdir -p ssl
mkdir -p ~/backups

log_info "Directories created"
echo ""

# Display next steps
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Setup completed successfully!${NC}"
echo ""
echo "Next steps:"
echo ""
echo "1. Configure environment variables:"
echo "   nano accreditation_copilot/.env"
echo ""
echo "2. Review deployment guide:"
echo "   cat AWS_DEPLOYMENT_GUIDE.md"
echo ""
echo "3. Deploy application:"
echo "   ./deploy.sh"
echo ""
echo "4. Monitor deployment:"
echo "   ./monitor.sh"
echo ""
echo "5. Run health checks:"
echo "   ./healthcheck.sh"
echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo ""
echo "For quick reference, see: QUICK_DEPLOY.md"
echo "For detailed guide, see: AWS_DEPLOYMENT_GUIDE.md"
echo "For package info, see: DEPLOYMENT_README.md"
echo ""
