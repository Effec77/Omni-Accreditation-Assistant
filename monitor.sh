#!/bin/bash

###############################################################################
# Monitoring Script for Accreditation Copilot
# Displays real-time system and application metrics
###############################################################################

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

clear

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Accreditation Copilot - System Monitor                ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# System Information
echo -e "${GREEN}[SYSTEM INFORMATION]${NC}"
echo "Hostname: $(hostname)"
echo "Uptime: $(uptime -p)"
echo "Date: $(date)"
echo ""

# CPU and Memory
echo -e "${GREEN}[RESOURCES]${NC}"
echo "CPU Usage:"
top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print "  Used: " 100 - $1 "%"}'

echo "Memory Usage:"
free -h | awk 'NR==2{printf "  Used: %s / %s (%.2f%%)\n", $3, $2, $3*100/$2}'

echo "Disk Usage:"
df -h / | awk 'NR==2{printf "  Used: %s / %s (%s)\n", $3, $2, $5}'
echo ""

# Docker Status
echo -e "${GREEN}[DOCKER CONTAINERS]${NC}"
if command -v docker &> /dev/null; then
    docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | head -n 10
else
    echo "Docker not installed"
fi
echo ""

# Service Health Checks
echo -e "${GREEN}[SERVICE HEALTH]${NC}"

# Backend
if curl -f http://localhost:8000/health &> /dev/null; then
    echo -e "Backend API:  ${GREEN}✓ Healthy${NC}"
else
    echo -e "Backend API:  ${RED}✗ Unhealthy${NC}"
fi

# Frontend
if curl -f http://localhost:3000 &> /dev/null; then
    echo -e "Frontend:     ${GREEN}✓ Healthy${NC}"
else
    echo -e "Frontend:     ${RED}✗ Unhealthy${NC}"
fi

# Nginx
if systemctl is-active --quiet nginx; then
    echo -e "Nginx:        ${GREEN}✓ Running${NC}"
else
    echo -e "Nginx:        ${YELLOW}○ Not Running${NC}"
fi
echo ""

# Docker Resource Usage
echo -e "${GREEN}[CONTAINER RESOURCES]${NC}"
if command -v docker &> /dev/null; then
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
fi
echo ""

# Recent Logs
echo -e "${GREEN}[RECENT LOGS - Last 5 lines]${NC}"
if [ -f "logs/backend.log" ]; then
    echo -e "${YELLOW}Backend:${NC}"
    tail -n 5 logs/backend.log 2>/dev/null || echo "No logs available"
fi
echo ""

# Network Connections
echo -e "${GREEN}[NETWORK]${NC}"
echo "Active Connections:"
netstat -an | grep -E ':(3000|8000|80|443)' | grep ESTABLISHED | wc -l | awk '{print "  Established: " $1}'
echo ""

# Disk I/O
echo -e "${GREEN}[DISK I/O]${NC}"
iostat -x 1 2 | tail -n +4 | head -n 1 | awk '{printf "  Read: %.2f MB/s, Write: %.2f MB/s\n", $6/1024, $7/1024}' 2>/dev/null || echo "  iostat not available"
echo ""

# Last Backup
echo -e "${GREEN}[BACKUPS]${NC}"
if [ -d "$HOME/backups" ]; then
    LAST_BACKUP=$(ls -t $HOME/backups/*.tar.gz 2>/dev/null | head -n 1)
    if [ -n "$LAST_BACKUP" ]; then
        echo "Last Backup: $(basename $LAST_BACKUP)"
        echo "Size: $(du -h $LAST_BACKUP | cut -f1)"
        echo "Date: $(stat -c %y $LAST_BACKUP | cut -d' ' -f1)"
    else
        echo "No backups found"
    fi
else
    echo "Backup directory not found"
fi
echo ""

# Alerts
echo -e "${GREEN}[ALERTS]${NC}"

# Check CPU
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
if (( $(echo "$CPU_USAGE > 80" | bc -l) )); then
    echo -e "${RED}⚠ High CPU usage: ${CPU_USAGE}%${NC}"
fi

# Check Memory
MEM_USAGE=$(free | grep Mem | awk '{print ($3/$2) * 100.0}')
if (( $(echo "$MEM_USAGE > 80" | bc -l) )); then
    echo -e "${RED}⚠ High memory usage: ${MEM_USAGE}%${NC}"
fi

# Check Disk
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | sed 's/%//')
if [ "$DISK_USAGE" -gt 80 ]; then
    echo -e "${RED}⚠ High disk usage: ${DISK_USAGE}%${NC}"
fi

# Check if no alerts
if (( $(echo "$CPU_USAGE < 80" | bc -l) )) && \
   (( $(echo "$MEM_USAGE < 80" | bc -l) )) && \
   [ "$DISK_USAGE" -lt 80 ]; then
    echo -e "${GREEN}✓ All systems normal${NC}"
fi

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════════${NC}"
echo "Press Ctrl+C to exit"
echo ""

# Optional: Auto-refresh every 5 seconds
# Uncomment the following lines for auto-refresh
# sleep 5
# exec $0
