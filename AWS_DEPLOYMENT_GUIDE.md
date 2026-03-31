# AWS Deployment Guide - Accreditation Copilot

Complete step-by-step guide to deploy the Accreditation Copilot project on AWS using Docker.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         AWS Cloud                            │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              EC2 Instance (Ubuntu)                  │    │
│  │                                                      │    │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────┐ │    │
│  │  │   Frontend   │  │   Backend    │  │  Nginx   │ │    │
│  │  │  (Next.js)   │  │  (FastAPI)   │  │  Reverse │ │    │
│  │  │  Port 3000   │  │  Port 8000   │  │  Proxy   │ │    │
│  │  └──────────────┘  └──────────────┘  └──────────┘ │    │
│  │                                                      │    │
│  │  ┌──────────────────────────────────────────────┐  │    │
│  │  │         Docker Compose Network               │  │    │
│  │  └──────────────────────────────────────────────┘  │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────┐  ┌────────────────┐                    │
│  │  Security      │  │  Elastic IP    │                    │
│  │  Group         │  │  (Static IP)   │                    │
│  └────────────────┘  └────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

1. AWS Account with appropriate permissions
2. AWS CLI installed and configured
3. SSH key pair for EC2 access
4. Domain name (optional, for custom domain)
5. Git installed locally

---

## Phase 1: AWS Infrastructure Setup

### Step 1.1: Create EC2 Instance

1. **Login to AWS Console**
   - Navigate to EC2 Dashboard
   - Click "Launch Instance"

2. **Configure Instance**
   ```
   Name: accreditation-copilot-prod
   AMI: Ubuntu Server 22.04 LTS (HVM), SSD Volume Type
   Instance Type: t3.xlarge (4 vCPU, 16 GB RAM)
   ```

3. **Create/Select Key Pair**
   - Key pair name: `accreditation-copilot-key`
   - Key pair type: RSA
   - Private key format: .pem
   - Download and save securely

4. **Network Settings**
   - Create new security group: `accreditation-copilot-sg`
   - Allow SSH (port 22) from your IP
   - Allow HTTP (port 80) from anywhere
   - Allow HTTPS (port 443) from anywhere
   - Allow Custom TCP (port 8000) from anywhere (for API)
   - Allow Custom TCP (port 3000) from anywhere (for frontend)

5. **Storage Configuration**
   - Root volume: 50 GB gp3
   - Add additional volume: 100 GB gp3 (for data/indexes)

6. **Launch Instance**

### Step 1.2: Setup Security Group Rules

```bash
# SSH from your IP
Type: SSH
Protocol: TCP
Port: 22
Source: Your IP/32

# HTTP
Type: HTTP
Protocol: TCP
Port: 80
Source: 0.0.0.0/0

# HTTPS
Type: HTTPS
Protocol: TCP
Port: 443
Source: 0.0.0.0/0

# Backend API
Type: Custom TCP
Protocol: TCP
Port: 8000
Source: 0.0.0.0/0

# Frontend
Type: Custom TCP
Protocol: TCP
Port: 3000
Source: 0.0.0.0/0
```

### Step 1.3: Allocate Elastic IP

1. Navigate to EC2 → Elastic IPs
2. Click "Allocate Elastic IP address"
3. Click "Allocate"
4. Select the new Elastic IP
5. Actions → Associate Elastic IP address
6. Select your EC2 instance
7. Click "Associate"

### Step 1.4: Create IAM Role (Optional)

If you need S3 access for file storage:

1. Navigate to IAM → Roles
2. Create role for EC2
3. Attach policies:
   - AmazonS3FullAccess (or custom policy)
4. Attach role to EC2 instance

---

## Phase 2: Server Configuration

### Step 2.1: Connect to EC2 Instance

```bash
# Set correct permissions for key
chmod 400 accreditation-copilot-key.pem

# Connect via SSH
ssh -i accreditation-copilot-key.pem ubuntu@<ELASTIC_IP>
```

### Step 2.2: Update System

```bash
# Update package list
sudo apt update && sudo apt upgrade -y

# Install essential tools
sudo apt install -y git curl wget vim htop
```

### Step 2.3: Install Docker

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker ubuntu

# Start Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Verify installation
docker --version
```

### Step 2.4: Install Docker Compose

```bash
# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make executable
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version
```

### Step 2.5: Install Nginx (Reverse Proxy)

```bash
# Install Nginx
sudo apt install -y nginx

# Start and enable Nginx
sudo systemctl start nginx
sudo systemctl enable nginx

# Verify
sudo systemctl status nginx
```

---

## Phase 3: Project Setup

### Step 3.1: Clone Repository

```bash
# Navigate to home directory
cd ~

# Clone your repository
git clone <YOUR_REPO_URL> accreditation-copilot
cd accreditation-copilot
```

### Step 3.2: Setup Environment Variables

```bash
# Copy environment template
cp accreditation_copilot/.env.example accreditation_copilot/.env

# Edit environment file
nano accreditation_copilot/.env
```

Add your API keys and configuration:
```env
# Groq API Keys
GROQ_API_KEY_1=your_key_1
GROQ_API_KEY_2=your_key_2
GROQ_API_KEY_3=your_key_3

# LangSmith
LANGCHAIN_API_KEY=your_langsmith_key
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=accreditation-copilot-prod

# HuggingFace
HUGGINGFACE_TOKEN=your_hf_token

# Application
ENVIRONMENT=production
DEBUG=false
```

### Step 3.3: Install Dependencies

```bash
# Create data directories
sudo mkdir -p /data/accreditation-copilot/{indexes,data,uploads}
sudo chown -R ubuntu:ubuntu /data/accreditation-copilot

# Copy existing data (if any)
cp -r accreditation_copilot/data/* /data/accreditation-copilot/data/
cp -r accreditation_copilot/indexes/* /data/accreditation-copilot/indexes/
```

---

## Phase 4: Docker Configuration

### Step 4.1: Create Dockerfiles

These files are already created in the deployment package. Review them:

- `Dockerfile.backend` - Backend API container
- `Dockerfile.frontend` - Frontend Next.js container
- `docker-compose.yml` - Orchestration file
- `nginx.conf` - Nginx reverse proxy configuration

### Step 4.2: Build Docker Images

```bash
# Build backend image
docker build -f Dockerfile.backend -t accreditation-backend:latest .

# Build frontend image
docker build -f Dockerfile.frontend -t accreditation-frontend:latest .

# Verify images
docker images
```

### Step 4.3: Configure Nginx Reverse Proxy

```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/accreditation-copilot
```

Copy the configuration from `nginx.conf` file provided.

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/accreditation-copilot /etc/nginx/sites-enabled/

# Remove default site
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx
```

---

## Phase 5: Launch Application

### Step 5.1: Start Docker Containers

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Step 5.2: Verify Services

```bash
# Check backend health
curl http://localhost:8000/health

# Check frontend
curl http://localhost:3000

# Check through Nginx
curl http://<ELASTIC_IP>
```

### Step 5.3: Monitor Logs

```bash
# Backend logs
docker-compose logs -f backend

# Frontend logs
docker-compose logs -f frontend

# All logs
docker-compose logs -f
```

---

## Phase 6: SSL/HTTPS Setup (Optional but Recommended)

### Step 6.1: Install Certbot

```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx
```

### Step 6.2: Obtain SSL Certificate

```bash
# Get certificate (replace with your domain)
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Follow prompts
# - Enter email
# - Agree to terms
# - Choose redirect option (2)
```

### Step 6.3: Auto-renewal

```bash
# Test renewal
sudo certbot renew --dry-run

# Certbot auto-renewal is enabled by default
```

---

## Phase 7: Monitoring & Maintenance

### Step 7.1: Setup Monitoring

```bash
# Install monitoring tools
sudo apt install -y htop iotop nethogs

# Monitor resources
htop

# Monitor Docker
docker stats
```

### Step 7.2: Setup Log Rotation

```bash
# Configure Docker log rotation
sudo nano /etc/docker/daemon.json
```

Add:
```json
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
```

```bash
# Restart Docker
sudo systemctl restart docker
```

### Step 7.3: Backup Strategy

```bash
# Create backup script
nano ~/backup.sh
```

Add backup script content (provided separately).

```bash
# Make executable
chmod +x ~/backup.sh

# Setup cron job for daily backups
crontab -e
```

Add:
```
0 2 * * * /home/ubuntu/backup.sh
```

---

## Phase 8: Testing & Validation

### Step 8.1: Health Checks

```bash
# Backend health
curl http://<ELASTIC_IP>/api/health

# Frontend
curl http://<ELASTIC_IP>

# Full audit test
curl -X POST http://<ELASTIC_IP>/api/audit/run-full-audit
```

### Step 8.2: Load Testing

```bash
# Install Apache Bench
sudo apt install -y apache2-utils

# Test backend
ab -n 100 -c 10 http://<ELASTIC_IP>/api/health

# Test frontend
ab -n 100 -c 10 http://<ELASTIC_IP>/
```

---

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   sudo lsof -i :8000
   sudo kill -9 <PID>
   ```

2. **Docker permission denied**
   ```bash
   sudo usermod -aG docker $USER
   newgrp docker
   ```

3. **Out of memory**
   ```bash
   # Check memory
   free -h
   
   # Add swap
   sudo fallocate -l 4G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

4. **Container won't start**
   ```bash
   docker-compose logs <service_name>
   docker-compose down
   docker-compose up -d
   ```

---

## Useful Commands

```bash
# Restart all services
docker-compose restart

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build

# View resource usage
docker stats

# Clean up unused resources
docker system prune -a

# Update application
cd ~/accreditation-copilot
git pull
docker-compose up -d --build

# View Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

---

## Security Checklist

- [ ] SSH key-based authentication only
- [ ] Firewall configured (UFW or Security Groups)
- [ ] SSL/TLS certificate installed
- [ ] Environment variables secured
- [ ] Regular security updates
- [ ] Backup strategy implemented
- [ ] Monitoring enabled
- [ ] Log rotation configured
- [ ] Non-root user for application
- [ ] Docker security best practices

---

## Next Steps

1. Configure domain name (if applicable)
2. Setup CI/CD pipeline
3. Configure monitoring (CloudWatch, Prometheus)
4. Setup alerting
5. Implement auto-scaling (if needed)
6. Configure CDN (CloudFront)
7. Setup database backups
8. Implement disaster recovery plan

---

## Support & Resources

- AWS Documentation: https://docs.aws.amazon.com/
- Docker Documentation: https://docs.docker.com/
- Nginx Documentation: https://nginx.org/en/docs/
- Let's Encrypt: https://letsencrypt.org/

---

**Deployment Date:** [Add date]
**Last Updated:** [Add date]
**Deployed By:** [Add name]
