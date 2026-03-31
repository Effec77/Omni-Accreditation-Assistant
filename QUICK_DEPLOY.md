# Quick Deployment Guide

This is a condensed version of the full deployment guide for quick reference.

## Prerequisites

- AWS Account
- SSH key pair
- Domain name (optional)

## Step-by-Step Deployment

### 1. Launch EC2 Instance

```bash
# Instance Configuration
AMI: Ubuntu 22.04 LTS
Type: t3.xlarge (4 vCPU, 16 GB RAM)
Storage: 50 GB root + 100 GB data
Security Group: Allow ports 22, 80, 443, 3000, 8000
```

### 2. Connect to Instance

```bash
chmod 400 your-key.pem
ssh -i your-key.pem ubuntu@<ELASTIC_IP>
```

### 3. Install Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again for group changes
exit
```

### 4. Clone and Setup Project

```bash
# Clone repository
git clone <YOUR_REPO_URL> accreditation-copilot
cd accreditation-copilot

# Setup environment
cp accreditation_copilot/.env.example accreditation_copilot/.env
nano accreditation_copilot/.env  # Add your API keys

# Make scripts executable
chmod +x deploy.sh backup.sh update.sh
```

### 5. Deploy Application

```bash
# Run deployment script
./deploy.sh
```

### 6. Verify Deployment

```bash
# Check services
docker-compose ps

# Test endpoints
curl http://localhost:8000/health
curl http://localhost:3000

# View logs
docker-compose logs -f
```

### 7. Setup Nginx (Optional)

```bash
# Install Nginx
sudo apt install -y nginx

# Copy configuration
sudo cp nginx.conf /etc/nginx/sites-available/accreditation-copilot
sudo ln -s /etc/nginx/sites-available/accreditation-copilot /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Test and reload
sudo nginx -t
sudo systemctl reload nginx
```

### 8. Setup SSL (Optional)

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com
```

## Common Commands

```bash
# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Update application
./update.sh

# Create backup
./backup.sh

# Check resource usage
docker stats
```

## Troubleshooting

### Services won't start
```bash
docker-compose logs <service_name>
docker-compose down
docker-compose up -d
```

### Out of memory
```bash
# Add swap
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Port already in use
```bash
sudo lsof -i :8000
sudo kill -9 <PID>
```

## Access URLs

- Frontend: `http://<ELASTIC_IP>:3000`
- Backend API: `http://<ELASTIC_IP>:8000`
- API Docs: `http://<ELASTIC_IP>:8000/docs`
- Health Check: `http://<ELASTIC_IP>:8000/health`

## Security Checklist

- [ ] SSH key-based authentication
- [ ] Firewall configured
- [ ] SSL certificate installed
- [ ] Environment variables secured
- [ ] Regular backups enabled
- [ ] Monitoring configured

## Support

For detailed instructions, see `AWS_DEPLOYMENT_GUIDE.md`
