# Visual Deployment Guide

Step-by-step visual guide for deploying Accreditation Copilot on AWS.

## 🎯 Deployment Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT PROCESS                        │
└─────────────────────────────────────────────────────────────┘

Step 1: AWS Setup
┌──────────────┐
│   Launch     │
│   EC2        │──→ Ubuntu 22.04 LTS
│   Instance   │    t3.xlarge (4 vCPU, 16GB RAM)
└──────────────┘    50GB + 100GB storage

Step 2: Security Configuration
┌──────────────┐
│   Configure  │
│   Security   │──→ Ports: 22, 80, 443, 3000, 8000
│   Group      │    SSH key authentication
└──────────────┘    Elastic IP

Step 3: Server Setup
┌──────────────┐
│   Install    │
│   Docker &   │──→ Docker Engine
│   Tools      │    Docker Compose
└──────────────┘    Nginx (optional)

Step 4: Application Deployment
┌──────────────┐
│   Clone &    │
│   Configure  │──→ Git clone repository
│   Project    │    Setup .env file
└──────────────┘    Run ./deploy.sh

Step 5: Verification
┌──────────────┐
│   Test &     │
│   Monitor    │──→ Health checks
│   Services   │    Monitor resources
└──────────────┘    View logs

Step 6: Production Ready
┌──────────────┐
│   SSL/TLS    │
│   Backups    │──→ Let's Encrypt SSL
│   Monitoring │    Automated backups
└──────────────┘    CloudWatch (optional)
```

## 📋 Pre-Deployment Checklist

```
┌─────────────────────────────────────────────────────────────┐
│                   BEFORE YOU START                           │
└─────────────────────────────────────────────────────────────┘

Required Items:
  ☐ AWS Account
  ☐ SSH Key Pair
  ☐ Groq API Keys (3 keys)
  ☐ LangSmith API Key
  ☐ HuggingFace Token
  ☐ Domain Name (optional)

Local Setup:
  ☐ Git installed
  ☐ SSH client installed
  ☐ Text editor ready
  ☐ Terminal/Command prompt

Knowledge Required:
  ☐ Basic Linux commands
  ☐ SSH connection
  ☐ Text file editing
  ☐ Basic networking
```

## 🖥️ EC2 Instance Setup

```
┌─────────────────────────────────────────────────────────────┐
│                   EC2 CONFIGURATION                          │
└─────────────────────────────────────────────────────────────┘

Instance Details:
┌──────────────────────────────────────────────────────────────┐
│ Name:          accreditation-copilot-prod                    │
│ AMI:           Ubuntu Server 22.04 LTS                       │
│ Instance Type: t3.xlarge                                     │
│ vCPU:          4                                             │
│ Memory:        16 GB                                         │
│ Storage:       50 GB (root) + 100 GB (data)                 │
└──────────────────────────────────────────────────────────────┘

Security Group Rules:
┌──────────────────────────────────────────────────────────────┐
│ Port  │ Protocol │ Source      │ Purpose                    │
├───────┼──────────┼─────────────┼────────────────────────────┤
│ 22    │ TCP      │ Your IP     │ SSH Access                 │
│ 80    │ TCP      │ 0.0.0.0/0   │ HTTP                       │
│ 443   │ TCP      │ 0.0.0.0/0   │ HTTPS                      │
│ 3000  │ TCP      │ 0.0.0.0/0   │ Frontend (temporary)       │
│ 8000  │ TCP      │ 0.0.0.0/0   │ Backend API (temporary)    │
└──────────────────────────────────────────────────────────────┘

Note: Ports 3000 and 8000 can be closed after Nginx setup
```

## 🔧 Installation Commands

```
┌─────────────────────────────────────────────────────────────┐
│                   INSTALLATION STEPS                         │
└─────────────────────────────────────────────────────────────┘

1. Connect to EC2:
   ┌────────────────────────────────────────────────────────┐
   │ chmod 400 your-key.pem                                 │
   │ ssh -i your-key.pem ubuntu@<ELASTIC_IP>                │
   └────────────────────────────────────────────────────────┘

2. Update System:
   ┌────────────────────────────────────────────────────────┐
   │ sudo apt update && sudo apt upgrade -y                 │
   └────────────────────────────────────────────────────────┘

3. Install Docker:
   ┌────────────────────────────────────────────────────────┐
   │ curl -fsSL https://get.docker.com -o get-docker.sh    │
   │ sudo sh get-docker.sh                                  │
   │ sudo usermod -aG docker ubuntu                         │
   └────────────────────────────────────────────────────────┘

4. Install Docker Compose:
   ┌────────────────────────────────────────────────────────┐
   │ sudo curl -L "https://github.com/docker/compose/      │
   │   releases/latest/download/docker-compose-             │
   │   $(uname -s)-$(uname -m)"                             │
   │   -o /usr/local/bin/docker-compose                     │
   │ sudo chmod +x /usr/local/bin/docker-compose            │
   └────────────────────────────────────────────────────────┘

5. Logout and Login:
   ┌────────────────────────────────────────────────────────┐
   │ exit                                                   │
   │ ssh -i your-key.pem ubuntu@<ELASTIC_IP>                │
   └────────────────────────────────────────────────────────┘
```

## 📦 Application Deployment

```
┌─────────────────────────────────────────────────────────────┐
│                   DEPLOYMENT STEPS                           │
└─────────────────────────────────────────────────────────────┘

1. Clone Repository:
   ┌────────────────────────────────────────────────────────┐
   │ git clone <YOUR_REPO_URL> accreditation-copilot       │
   │ cd accreditation-copilot                               │
   └────────────────────────────────────────────────────────┘

2. Setup Environment:
   ┌────────────────────────────────────────────────────────┐
   │ cp accreditation_copilot/.env.example \                │
   │    accreditation_copilot/.env                          │
   │ nano accreditation_copilot/.env                        │
   └────────────────────────────────────────────────────────┘

   Add your API keys:
   ┌────────────────────────────────────────────────────────┐
   │ GROQ_API_KEY_1=your_actual_key_1                       │
   │ GROQ_API_KEY_2=your_actual_key_2                       │
   │ GROQ_API_KEY_3=your_actual_key_3                       │
   │ LANGCHAIN_API_KEY=your_langsmith_key                   │
   │ HUGGINGFACE_TOKEN=your_hf_token                        │
   └────────────────────────────────────────────────────────┘

3. Run Setup:
   ┌────────────────────────────────────────────────────────┐
   │ ./setup-deployment.sh                                  │
   └────────────────────────────────────────────────────────┘

4. Deploy Application:
   ┌────────────────────────────────────────────────────────┐
   │ ./deploy.sh                                            │
   └────────────────────────────────────────────────────────┘

   This will:
   ✓ Check prerequisites
   ✓ Create backup
   ✓ Build Docker images
   ✓ Start services
   ✓ Verify health
```

## 🔍 Verification Steps

```
┌─────────────────────────────────────────────────────────────┐
│                   VERIFICATION                               │
└─────────────────────────────────────────────────────────────┘

1. Check Services:
   ┌────────────────────────────────────────────────────────┐
   │ docker-compose ps                                      │
   └────────────────────────────────────────────────────────┘

   Expected Output:
   ┌────────────────────────────────────────────────────────┐
   │ NAME                    STATUS      PORTS              │
   │ accreditation-backend   Up          0.0.0.0:8000->8000 │
   │ accreditation-frontend  Up          0.0.0.0:3000->3000 │
   │ accreditation-nginx     Up          0.0.0.0:80->80     │
   └────────────────────────────────────────────────────────┘

2. Test Endpoints:
   ┌────────────────────────────────────────────────────────┐
   │ curl http://localhost:8000/health                      │
   │ curl http://localhost:3000                             │
   └────────────────────────────────────────────────────────┘

3. Run Health Check:
   ┌────────────────────────────────────────────────────────┐
   │ ./healthcheck.sh                                       │
   └────────────────────────────────────────────────────────┘

4. View Logs:
   ┌────────────────────────────────────────────────────────┐
   │ docker-compose logs -f                                 │
   └────────────────────────────────────────────────────────┘
```

## 🌐 Access Your Application

```
┌─────────────────────────────────────────────────────────────┐
│                   APPLICATION URLS                           │
└─────────────────────────────────────────────────────────────┘

Frontend:
┌────────────────────────────────────────────────────────────┐
│ http://<ELASTIC_IP>:3000                                   │
│ or                                                         │
│ http://yourdomain.com (after Nginx + SSL setup)           │
└────────────────────────────────────────────────────────────┘

Backend API:
┌────────────────────────────────────────────────────────────┐
│ http://<ELASTIC_IP>:8000                                   │
│ or                                                         │
│ http://yourdomain.com/api (after Nginx setup)             │
└────────────────────────────────────────────────────────────┘

API Documentation:
┌────────────────────────────────────────────────────────────┐
│ http://<ELASTIC_IP>:8000/docs                              │
└────────────────────────────────────────────────────────────┘

Health Check:
┌────────────────────────────────────────────────────────────┐
│ http://<ELASTIC_IP>:8000/health                            │
└────────────────────────────────────────────────────────────┘
```

## 🔐 SSL/TLS Setup (Optional)

```
┌─────────────────────────────────────────────────────────────┐
│                   SSL CERTIFICATE SETUP                      │
└─────────────────────────────────────────────────────────────┘

1. Install Certbot:
   ┌────────────────────────────────────────────────────────┐
   │ sudo apt install -y certbot python3-certbot-nginx     │
   └────────────────────────────────────────────────────────┘

2. Get Certificate:
   ┌────────────────────────────────────────────────────────┐
   │ sudo certbot --nginx -d yourdomain.com                 │
   └────────────────────────────────────────────────────────┘

3. Test Auto-Renewal:
   ┌────────────────────────────────────────────────────────┐
   │ sudo certbot renew --dry-run                           │
   └────────────────────────────────────────────────────────┘

After SSL Setup:
┌────────────────────────────────────────────────────────────┐
│ ✓ HTTPS enabled                                            │
│ ✓ HTTP redirects to HTTPS                                 │
│ ✓ Auto-renewal configured                                 │
│ ✓ Access via: https://yourdomain.com                      │
└────────────────────────────────────────────────────────────┘
```

## 📊 Monitoring Dashboard

```
┌─────────────────────────────────────────────────────────────┐
│                   MONITORING TOOLS                           │
└─────────────────────────────────────────────────────────────┘

Real-time Monitor:
┌────────────────────────────────────────────────────────────┐
│ ./monitor.sh                                               │
└────────────────────────────────────────────────────────────┘

Shows:
  • System resources (CPU, Memory, Disk)
  • Docker container status
  • Service health
  • Network connections
  • Recent logs
  • Alerts

Health Check:
┌────────────────────────────────────────────────────────────┐
│ ./healthcheck.sh                                           │
└────────────────────────────────────────────────────────────┘

Checks:
  • System resources
  • Docker containers
  • Network ports
  • Service endpoints
  • API functionality

View Logs:
┌────────────────────────────────────────────────────────────┐
│ docker-compose logs -f                    # All services   │
│ docker-compose logs -f backend            # Backend only   │
│ docker-compose logs -f frontend           # Frontend only  │
└────────────────────────────────────────────────────────────┘
```

## 🔄 Maintenance Commands

```
┌─────────────────────────────────────────────────────────────┐
│                   COMMON OPERATIONS                          │
└─────────────────────────────────────────────────────────────┘

Update Application:
┌────────────────────────────────────────────────────────────┐
│ ./update.sh                                                │
└────────────────────────────────────────────────────────────┘

Create Backup:
┌────────────────────────────────────────────────────────────┐
│ ./backup.sh                                                │
└────────────────────────────────────────────────────────────┘

Restore from Backup:
┌────────────────────────────────────────────────────────────┐
│ ./rollback.sh                                              │
└────────────────────────────────────────────────────────────┘

Restart Services:
┌────────────────────────────────────────────────────────────┐
│ docker-compose restart                                     │
└────────────────────────────────────────────────────────────┘

Stop Services:
┌────────────────────────────────────────────────────────────┐
│ docker-compose down                                        │
└────────────────────────────────────────────────────────────┘

Start Services:
┌────────────────────────────────────────────────────────────┐
│ docker-compose up -d                                       │
└────────────────────────────────────────────────────────────┘

View Resource Usage:
┌────────────────────────────────────────────────────────────┐
│ docker stats                                               │
└────────────────────────────────────────────────────────────┘
```

## 🆘 Troubleshooting Quick Reference

```
┌─────────────────────────────────────────────────────────────┐
│                   COMMON ISSUES                              │
└─────────────────────────────────────────────────────────────┘

Service Won't Start:
┌────────────────────────────────────────────────────────────┐
│ docker-compose logs <service_name>                         │
│ docker-compose down                                        │
│ docker-compose up -d                                       │
└────────────────────────────────────────────────────────────┘

Out of Memory:
┌────────────────────────────────────────────────────────────┐
│ sudo fallocate -l 4G /swapfile                             │
│ sudo chmod 600 /swapfile                                   │
│ sudo mkswap /swapfile                                      │
│ sudo swapon /swapfile                                      │
└────────────────────────────────────────────────────────────┘

Port Already in Use:
┌────────────────────────────────────────────────────────────┐
│ sudo lsof -i :8000                                         │
│ sudo kill -9 <PID>                                         │
└────────────────────────────────────────────────────────────┘

Docker Permission Denied:
┌────────────────────────────────────────────────────────────┐
│ sudo usermod -aG docker $USER                              │
│ newgrp docker                                              │
└────────────────────────────────────────────────────────────┘
```

## ✅ Success Indicators

```
┌─────────────────────────────────────────────────────────────┐
│                   DEPLOYMENT SUCCESS                         │
└─────────────────────────────────────────────────────────────┘

You know deployment is successful when:

✓ All Docker containers are running
✓ Health check passes
✓ Frontend loads in browser
✓ Backend API responds
✓ No errors in logs
✓ Resource usage is normal
✓ Backups are working
✓ Monitoring is active

Access your application at:
  Frontend: http://<ELASTIC_IP>:3000
  Backend:  http://<ELASTIC_IP>:8000
  API Docs: http://<ELASTIC_IP>:8000/docs
```

---

**For detailed instructions, see:** `AWS_DEPLOYMENT_GUIDE.md`
**For quick reference, see:** `QUICK_DEPLOY.md`
**For package info, see:** `DEPLOYMENT_README.md`
