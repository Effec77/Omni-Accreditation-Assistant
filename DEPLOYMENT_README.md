# Accreditation Copilot - AWS Deployment Package

Complete deployment package for deploying Accreditation Copilot on AWS using Docker.

## 📦 Package Contents

### Documentation
- `AWS_DEPLOYMENT_GUIDE.md` - Complete step-by-step deployment guide
- `QUICK_DEPLOY.md` - Quick reference guide
- `DEPLOYMENT_README.md` - This file

### Docker Configuration
- `Dockerfile.backend` - Backend API container configuration
- `Dockerfile.frontend` - Frontend Next.js container configuration
- `docker-compose.yml` - Multi-container orchestration
- `.dockerignore` - Files to exclude from Docker builds
- `nginx.conf` - Nginx reverse proxy configuration

### Deployment Scripts
- `deploy.sh` - Main deployment script
- `update.sh` - Zero-downtime update script
- `backup.sh` - Automated backup script
- `rollback.sh` - Restore from backup script
- `monitor.sh` - Real-time monitoring dashboard
- `healthcheck.sh` - Comprehensive health check script

## 🚀 Quick Start

### 1. Prerequisites

Ensure you have:
- AWS account with EC2 access
- SSH key pair for EC2
- Git installed
- Basic knowledge of Linux/Ubuntu

### 2. Launch EC2 Instance

```bash
# Recommended configuration
Instance Type: t3.xlarge (4 vCPU, 16 GB RAM)
AMI: Ubuntu 22.04 LTS
Storage: 50 GB root + 100 GB data
Security Group: Ports 22, 80, 443, 3000, 8000
```

### 3. Connect and Setup

```bash
# Connect to EC2
ssh -i your-key.pem ubuntu@<ELASTIC_IP>

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again
exit
```

### 4. Clone and Configure

```bash
# Clone repository
git clone <YOUR_REPO_URL> accreditation-copilot
cd accreditation-copilot

# Setup environment
cp accreditation_copilot/.env.example accreditation_copilot/.env
nano accreditation_copilot/.env  # Add your API keys

# Make scripts executable
chmod +x *.sh
```

### 5. Deploy

```bash
# Run deployment
./deploy.sh

# Monitor deployment
./monitor.sh
```

### 6. Verify

```bash
# Run health checks
./healthcheck.sh

# Check services
docker-compose ps

# View logs
docker-compose logs -f
```

## 📋 Deployment Scripts

### deploy.sh
Main deployment script that:
- Checks prerequisites
- Creates necessary directories
- Backs up existing data
- Builds Docker images
- Starts all services
- Verifies health

```bash
./deploy.sh
```

### update.sh
Zero-downtime update script that:
- Creates backup before update
- Pulls latest code
- Rebuilds images
- Performs rolling update
- Verifies health

```bash
./update.sh
```

### backup.sh
Automated backup script that:
- Backs up data, indexes, and databases
- Creates compressed archives
- Maintains backup retention
- Optional S3 upload

```bash
./backup.sh
```

### rollback.sh
Restore from backup script that:
- Lists available backups
- Allows selection of backup
- Stops services
- Restores data
- Restarts services

```bash
./rollback.sh
```

### monitor.sh
Real-time monitoring dashboard showing:
- System resources (CPU, memory, disk)
- Docker container status
- Service health
- Network connections
- Recent logs
- Alerts

```bash
./monitor.sh
```

### healthcheck.sh
Comprehensive health check that verifies:
- System resources
- Docker containers
- Network ports
- Service endpoints
- API functionality

```bash
./healthcheck.sh
```

## 🔧 Configuration

### Environment Variables

Edit `accreditation_copilot/.env`:

```env
# Groq API Keys (Required)
GROQ_API_KEY_1=your_key_1
GROQ_API_KEY_2=your_key_2
GROQ_API_KEY_3=your_key_3

# LangSmith (Required)
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=accreditation-copilot-prod

# HuggingFace (Required)
HUGGINGFACE_TOKEN=your_hf_token

# Application
ENVIRONMENT=production
DEBUG=false
```

### Docker Compose

Modify `docker-compose.yml` to adjust:
- Resource limits (CPU, memory)
- Port mappings
- Volume mounts
- Network configuration

### Nginx

Edit `nginx.conf` to configure:
- Reverse proxy settings
- SSL/TLS certificates
- Rate limiting
- Caching policies

## 📊 Monitoring

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Last 100 lines
docker-compose logs --tail=100
```

### Resource Usage

```bash
# Real-time stats
docker stats

# System resources
htop

# Disk usage
df -h
```

### Service Status

```bash
# Docker containers
docker-compose ps

# System services
systemctl status nginx
systemctl status docker
```

## 🔒 Security

### Firewall Configuration

```bash
# Install UFW
sudo apt install -y ufw

# Configure rules
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable
```

### SSL/TLS Setup

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com

# Auto-renewal (already configured)
sudo certbot renew --dry-run
```

### Security Best Practices

- Use SSH key authentication only
- Keep system updated: `sudo apt update && sudo apt upgrade`
- Use strong passwords for services
- Enable firewall (UFW or Security Groups)
- Regular security audits
- Monitor logs for suspicious activity

## 🔄 Maintenance

### Regular Tasks

**Daily:**
- Check service health: `./healthcheck.sh`
- Monitor resources: `./monitor.sh`
- Review logs: `docker-compose logs --tail=100`

**Weekly:**
- Update system: `sudo apt update && sudo apt upgrade`
- Review backups: `ls -lh ~/backups/`
- Check disk space: `df -h`

**Monthly:**
- Security updates
- Performance optimization
- Backup verification
- Log rotation

### Automated Backups

Setup cron job for daily backups:

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /home/ubuntu/accreditation-copilot/backup.sh
```

### Log Rotation

Configure Docker log rotation:

```bash
# Edit Docker daemon config
sudo nano /etc/docker/daemon.json

# Add:
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}

# Restart Docker
sudo systemctl restart docker
```

## 🐛 Troubleshooting

### Services Won't Start

```bash
# Check logs
docker-compose logs <service_name>

# Restart services
docker-compose down
docker-compose up -d

# Rebuild images
docker-compose up -d --build
```

### Out of Memory

```bash
# Check memory
free -h

# Add swap space
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile

# Make permanent
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Port Already in Use

```bash
# Find process using port
sudo lsof -i :8000

# Kill process
sudo kill -9 <PID>

# Or stop conflicting service
sudo systemctl stop <service_name>
```

### Docker Permission Denied

```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Apply changes
newgrp docker

# Or logout and login again
```

### High CPU/Memory Usage

```bash
# Check resource usage
docker stats

# Restart specific service
docker-compose restart backend

# Adjust resource limits in docker-compose.yml
```

## 📞 Support

### Useful Commands

```bash
# Restart all services
docker-compose restart

# Stop all services
docker-compose down

# Start services
docker-compose up -d

# View service status
docker-compose ps

# Clean up unused resources
docker system prune -a

# Check Docker version
docker --version
docker-compose --version
```

### Log Locations

- Docker logs: `docker-compose logs`
- Nginx logs: `/var/log/nginx/`
- Application logs: `./logs/`
- System logs: `/var/log/syslog`

### Health Check Endpoints

- Backend: `http://localhost:8000/health`
- Frontend: `http://localhost:3000`
- API Docs: `http://localhost:8000/docs`

## 📚 Additional Resources

- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Ubuntu Server Guide](https://ubuntu.com/server/docs)

## 🎯 Next Steps

After successful deployment:

1. **Configure Domain**
   - Point DNS to Elastic IP
   - Setup SSL certificate
   - Update Nginx configuration

2. **Setup Monitoring**
   - CloudWatch metrics
   - Log aggregation
   - Alerting system

3. **Implement CI/CD**
   - GitHub Actions
   - Automated testing
   - Automated deployment

4. **Optimize Performance**
   - CDN setup (CloudFront)
   - Database optimization
   - Caching strategies

5. **Disaster Recovery**
   - Multi-region backup
   - Failover strategy
   - Recovery procedures

## 📝 Changelog

- **v1.0.0** - Initial deployment package
  - Docker configuration
  - Deployment scripts
  - Monitoring tools
  - Documentation

---

**Last Updated:** 2025-01-XX
**Version:** 1.0.0
**Maintainer:** Your Team
