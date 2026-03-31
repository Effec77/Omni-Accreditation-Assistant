# AWS Deployment Checklist

Use this checklist to ensure a smooth deployment of the Accreditation Copilot project.

## Pre-Deployment

### AWS Setup
- [ ] AWS account created and configured
- [ ] IAM user with appropriate permissions
- [ ] SSH key pair generated and downloaded
- [ ] Security group created with required ports
- [ ] Elastic IP allocated (optional but recommended)

### Local Preparation
- [ ] Repository cloned locally
- [ ] All deployment files present
- [ ] Environment variables configured
- [ ] API keys obtained:
  - [ ] Groq API keys (3 keys)
  - [ ] LangSmith API key
  - [ ] HuggingFace token
- [ ] Domain name configured (optional)

## EC2 Instance Setup

### Instance Launch
- [ ] EC2 instance launched (t3.xlarge recommended)
- [ ] Ubuntu 22.04 LTS selected
- [ ] Storage configured (50 GB root + 100 GB data)
- [ ] Security group attached
- [ ] Elastic IP associated (if using)
- [ ] SSH access verified

### System Configuration
- [ ] Connected to instance via SSH
- [ ] System updated: `sudo apt update && sudo apt upgrade -y`
- [ ] Docker installed
- [ ] Docker Compose installed
- [ ] User added to docker group
- [ ] Nginx installed (if using external Nginx)

## Application Deployment

### Repository Setup
- [ ] Repository cloned on EC2
- [ ] Navigated to project directory
- [ ] Environment file created and configured
- [ ] Deployment scripts made executable: `chmod +x *.sh`

### Deployment Execution
- [ ] Setup script run: `./setup-deployment.sh`
- [ ] Environment variables verified
- [ ] Deployment script run: `./deploy.sh`
- [ ] No errors during deployment

### Verification
- [ ] Backend health check passed: `curl http://localhost:8000/health`
- [ ] Frontend accessible: `curl http://localhost:3000`
- [ ] Docker containers running: `docker-compose ps`
- [ ] Health check script passed: `./healthcheck.sh`
- [ ] Logs reviewed: `docker-compose logs`

## Post-Deployment

### Nginx Configuration (if using)
- [ ] Nginx configuration copied
- [ ] Configuration tested: `sudo nginx -t`
- [ ] Nginx reloaded: `sudo systemctl reload nginx`
- [ ] Application accessible via Nginx

### SSL/TLS Setup (optional but recommended)
- [ ] Certbot installed
- [ ] SSL certificate obtained
- [ ] HTTPS working
- [ ] HTTP to HTTPS redirect configured
- [ ] Auto-renewal tested: `sudo certbot renew --dry-run`

### Monitoring & Maintenance
- [ ] Monitoring script tested: `./monitor.sh`
- [ ] Backup script tested: `./backup.sh`
- [ ] Cron job for backups configured
- [ ] Log rotation configured
- [ ] CloudWatch monitoring setup (optional)

### Security
- [ ] Firewall configured (UFW or Security Groups)
- [ ] SSH key-based authentication only
- [ ] Unnecessary ports closed
- [ ] Environment variables secured
- [ ] Regular security updates scheduled

## Testing

### Functional Testing
- [ ] Frontend loads correctly
- [ ] Backend API responds
- [ ] API documentation accessible: `http://<IP>:8000/docs`
- [ ] Full audit endpoint tested
- [ ] File upload working (if applicable)
- [ ] All major features tested

### Performance Testing
- [ ] Load testing performed
- [ ] Response times acceptable
- [ ] Resource usage monitored
- [ ] No memory leaks detected

### Disaster Recovery
- [ ] Backup created successfully
- [ ] Backup restoration tested
- [ ] Rollback script tested: `./rollback.sh`
- [ ] Recovery procedures documented

## Documentation

### Internal Documentation
- [ ] Deployment date recorded
- [ ] Server details documented
- [ ] Access credentials secured
- [ ] Troubleshooting guide reviewed
- [ ] Team members trained

### External Documentation
- [ ] User guide updated
- [ ] API documentation published
- [ ] Change log updated
- [ ] Support contacts provided

## Final Checks

### Operational Readiness
- [ ] All services running smoothly
- [ ] No critical errors in logs
- [ ] Monitoring alerts configured
- [ ] Backup strategy in place
- [ ] Support team notified
- [ ] Rollback plan ready

### Performance Metrics
- [ ] CPU usage < 70%
- [ ] Memory usage < 80%
- [ ] Disk usage < 80%
- [ ] Response time < 2s
- [ ] Uptime > 99%

### Security Audit
- [ ] Security scan completed
- [ ] Vulnerabilities addressed
- [ ] Access logs reviewed
- [ ] Compliance requirements met

## Sign-Off

**Deployment Date:** _______________

**Deployed By:** _______________

**Verified By:** _______________

**Production Ready:** [ ] Yes [ ] No

**Notes:**
_________________________________________________________________
_________________________________________________________________
_________________________________________________________________

---

## Quick Reference

### Essential Commands

```bash
# Deploy application
./deploy.sh

# Update application
./update.sh

# Create backup
./backup.sh

# Restore from backup
./rollback.sh

# Monitor system
./monitor.sh

# Health check
./healthcheck.sh

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Stop services
docker-compose down

# Start services
docker-compose up -d
```

### Important URLs

- Frontend: `http://<ELASTIC_IP>:3000`
- Backend API: `http://<ELASTIC_IP>:8000`
- API Docs: `http://<ELASTIC_IP>:8000/docs`
- Health Check: `http://<ELASTIC_IP>:8000/health`

### Support Contacts

- Technical Lead: _______________
- DevOps Team: _______________
- AWS Support: _______________
- Emergency Contact: _______________

---

**Document Version:** 1.0
**Last Updated:** 2025-01-XX
