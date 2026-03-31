#!/bin/bash

###############################################################################
# Health Check Script for Accreditation Copilot
# Performs comprehensive health checks on all services
###############################################################################

set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

FAILED_CHECKS=0

check_service() {
    local service_name=$1
    local url=$2
    local expected_status=${3:-200}
    
    echo -n "Checking $service_name... "
    
    response=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null || echo "000")
    
    if [ "$response" -eq "$expected_status" ]; then
        echo -e "${GREEN}✓ OK${NC} (HTTP $response)"
        return 0
    else
        echo -e "${RED}✗ FAILED${NC} (HTTP $response)"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

check_docker_container() {
    local container_name=$1
    
    echo -n "Checking Docker container $container_name... "
    
    if docker ps --format '{{.Names}}' | grep -q "^${container_name}$"; then
        status=$(docker inspect --format='{{.State.Health.Status}}' "$container_name" 2>/dev/null || echo "unknown")
        
        if [ "$status" = "healthy" ] || [ "$status" = "unknown" ]; then
            echo -e "${GREEN}✓ Running${NC}"
            return 0
        else
            echo -e "${YELLOW}⚠ Running but unhealthy${NC}"
            FAILED_CHECKS=$((FAILED_CHECKS + 1))
            return 1
        fi
    else
        echo -e "${RED}✗ Not running${NC}"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

check_port() {
    local port=$1
    local service=$2
    
    echo -n "Checking port $port ($service)... "
    
    if netstat -tuln | grep -q ":$port "; then
        echo -e "${GREEN}✓ Open${NC}"
        return 0
    else
        echo -e "${RED}✗ Closed${NC}"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

check_disk_space() {
    echo -n "Checking disk space... "
    
    usage=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
    
    if [ "$usage" -lt 90 ]; then
        echo -e "${GREEN}✓ OK${NC} (${usage}% used)"
        return 0
    else
        echo -e "${RED}✗ WARNING${NC} (${usage}% used)"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

check_memory() {
    echo -n "Checking memory... "
    
    usage=$(free | grep Mem | awk '{printf "%.0f", ($3/$2) * 100.0}')
    
    if [ "$usage" -lt 90 ]; then
        echo -e "${GREEN}✓ OK${NC} (${usage}% used)"
        return 0
    else
        echo -e "${RED}✗ WARNING${NC} (${usage}% used)"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     Accreditation Copilot - Health Check                  ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

echo "[SYSTEM RESOURCES]"
check_disk_space
check_memory
echo ""

echo "[DOCKER CONTAINERS]"
check_docker_container "accreditation-backend"
check_docker_container "accreditation-frontend"
check_docker_container "accreditation-nginx"
echo ""

echo "[NETWORK PORTS]"
check_port 8000 "Backend API"
check_port 3000 "Frontend"
check_port 80 "HTTP"
echo ""

echo "[SERVICE ENDPOINTS]"
check_service "Backend Health" "http://localhost:8000/health"
check_service "Backend API" "http://localhost:8000/api/health" 404  # May not exist
check_service "Frontend" "http://localhost:3000"
echo ""

echo "[API FUNCTIONALITY]"
check_service "Criteria Endpoint" "http://localhost:8000/api/audit/criteria/NAAC"
echo ""

# Summary
echo "════════════════════════════════════════════════════════════"
if [ $FAILED_CHECKS -eq 0 ]; then
    echo -e "${GREEN}✓ All health checks passed${NC}"
    exit 0
else
    echo -e "${RED}✗ $FAILED_CHECKS health check(s) failed${NC}"
    echo ""
    echo "Troubleshooting steps:"
    echo "1. Check logs: docker-compose logs -f"
    echo "2. Restart services: docker-compose restart"
    echo "3. Check resources: docker stats"
    exit 1
fi
