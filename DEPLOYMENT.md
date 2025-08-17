# Restaurant Ingredient Tracker - Master Deployment Guide

> **Complete deployment documentation for all platforms and environments**

This is the master deployment guide covering all hosting options for the Restaurant Ingredient Tracker application. Choose the deployment method that best fits your infrastructure and requirements.

## 📖 Documentation Navigation

### Core Documentation
- **[Main README](README.md)** - Project overview and implementation comparison
- **[Project Architecture](replit.md)** - Technical specifications and recent changes

### Implementation-Specific Guides
- **[Flask Implementation](Flask%20Migration/README.md)** - Complete Flask production implementation
- **[Flask Deployment Guide](Flask%20Migration/DEPLOYMENT.md)** - Flask-specific production deployment
- **[System Service Setup](Flask%20Migration/SYSTEMD_SERVICE.md)** - Linux systemd service configuration

### Containerized Deployment
- **[Docker Deployment Guide](Docker%20Deployment/README.md)** - Containerized deployment options
- **[Docker Troubleshooting](Docker%20Deployment/TROUBLESHOOTING.md)** - Docker-specific issues and solutions

## 🏗️ Architecture & Implementation Choice

The Restaurant Ingredient Tracker provides **two complete implementations**:

### Streamlit Edition (Development/Testing)
- **Best For**: Development, testing, Replit hosting
- **Location**: Root directory files (`app.py`, etc.)
- **Strengths**: Rapid development, built-in UI components
- **Limitations**: Limited hosting options, WebSocket dependencies

### Flask Edition (Production/Universal) ⭐ **RECOMMENDED**
- **Best For**: Production, any hosting platform
- **Location**: [`Flask Migration/`](Flask%20Migration/) directory  
- **Strengths**: Universal compatibility, better performance, standard protocols
- **Documentation**: [Flask Implementation Guide](Flask%20Migration/README.md)

> **💡 Production Choice**: For production deployments, we strongly recommend the Flask edition due to its universal hosting compatibility and enterprise-grade features.

## 🚀 Quick Start by Platform

### 🖥️ Local Development

#### Streamlit (Quick Testing)
```bash
# Install and run Streamlit version
pip install streamlit pandas fpdf2 xlsxwriter
streamlit run app.py
# Access: http://localhost:8501
```

#### Flask (Production Testing)
```bash
# Setup and run Flask version
cd "Flask Migration"
chmod +x setup.sh start.sh
./setup.sh && ./start.sh
# Access: http://localhost:5000
```

### 🐧 Linux VPS/Dedicated Server (Recommended)

#### Automated Flask Production Deployment
```bash
cd "Flask Migration"
sudo ./deploy.sh  # Complete automated setup
```

**What this includes:**
- System user and directory creation
- Python virtual environment setup
- Systemd service installation
- Nginx reverse proxy configuration
- Firewall setup and security hardening
- SSL/HTTPS preparation

**Management:**
```bash
# Service control
sudo systemctl start restaurant-tracker
sudo systemctl status restaurant-tracker

# Health monitoring
./service-manager.sh health
./service-manager.sh logs
```

📖 **See**: [Flask Deployment Guide](Flask%20Migration/DEPLOYMENT.md) | [System Service Guide](Flask%20Migration/SYSTEMD_SERVICE.md)

### 🐳 Docker Deployment

#### Standard Docker (Modern Systems)
```bash
cd "Docker Deployment"
docker-compose up --build -d
```

#### CPU-Compatible Docker (Older Systems)
```bash
cd "Docker Deployment"
./run-cpu-compatible-legacy.sh
```

📖 **See**: [Docker Deployment Guide](Docker%20Deployment/README.md) | [Docker Troubleshooting](Docker%20Deployment/TROUBLESHOOTING.md)

### ☁️ Cloud Platform Deployment

#### Heroku (Flask)
```bash
cd "Flask Migration"
# Procfile included
heroku create your-app-name
git add . && git commit -m "Deploy"
git push heroku main
```

#### DigitalOcean App Platform (Flask)
1. Connect Git repository
2. **Root Directory**: `Flask Migration`
3. **Build Command**: `pip install -r requirements.txt`
4. **Run Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`
5. **Environment Variables**: Set `SECRET_KEY`

#### AWS Elastic Beanstalk (Flask)
```bash
cd "Flask Migration"
eb init
eb create restaurant-tracker-prod
eb deploy
```

### 🌐 Shared Hosting (cPanel/WHM)

#### Flask on Shared Hosting
1. **Upload Files**: Use File Manager to upload `Flask Migration` contents
2. **Python Environment**: Create virtual environment in hosting control panel
3. **Dependencies**: Install from `requirements.txt` via pip interface
4. **WSGI Setup**: Point to `app.py` as application entry point
5. **Environment**: Set `SECRET_KEY` in hosting environment variables

📖 **See**: [Flask Implementation Guide](Flask%20Migration/README.md)

## 📊 Platform Compatibility Matrix

| Platform | Streamlit | Flask | Docker | Recommendation |
|----------|-----------|-------|--------|----------------|
| **Replit** | ✅ Native | ✅ Compatible | ⚠️ Limited | Use Streamlit |
| **Heroku** | ⚠️ Limited | ✅ Excellent | ✅ Good | Use Flask |
| **DigitalOcean** | ⚠️ Complex | ✅ Simple | ✅ Excellent | Use Flask |
| **AWS/GCP** | ⚠️ Complex | ✅ Native | ✅ Excellent | Use Flask |
| **Shared Hosting** | ❌ No support | ✅ Full support | ❌ No support | Use Flask |
| **VPS/Dedicated** | ⚠️ Limited | ✅ Full control | ✅ Excellent | Use Flask |
| **Docker Platforms** | ⚠️ Complex | ✅ Compatible | ✅ Native | Use Docker + Flask |

## 🔧 Deployment Features Comparison

| Feature | Streamlit | Flask | Docker |
|---------|-----------|-------|--------|
| **Startup Time** | 30+ seconds | < 5 seconds | 10-45 seconds |
| **Memory Usage** | 200+ MB | < 100 MB | 150-200 MB |
| **Concurrent Users** | Limited | Excellent | Good |
| **Hosting Options** | Limited | Universal | Container platforms |
| **Management Tools** | Basic | Enterprise | Container tools |
| **Monitoring** | Limited | Full monitoring | Container monitoring |
| **SSL/HTTPS** | Complex | Built-in support | Nginx integration |
| **Custom Domains** | Limited | Full support | Full support |
| **Auto-scaling** | No | Manual/automatic | Container orchestration |

## 🛠️ Management and Monitoring

### Flask Service Management
```bash
cd "Flask Migration"

# Service status and health
./service-manager.sh status
./service-manager.sh health

# Log monitoring
./service-manager.sh logs
./service-manager.sh follow

# Service control (requires sudo)
sudo ./service-manager.sh start
sudo ./service-manager.sh restart
sudo ./service-manager.sh stop
```

### Docker Management
```bash
cd "Docker Deployment"

# Container status
docker-compose ps
docker-compose logs -f

# Resource monitoring
docker stats

# Container control
docker-compose restart
docker-compose stop
```

### System Monitoring
```bash
# Resource usage
htop
free -h
df -h

# Network monitoring
sudo netstat -tlnp | grep :5000
sudo lsof -i :5000

# Application health
curl http://localhost:5000/health
```

## 🔒 Security Best Practices

### Production Security Checklist

#### Application Security
- [ ] Strong `SECRET_KEY` in environment variables
- [ ] Input validation for CSV uploads
- [ ] File upload size limits
- [ ] Secure session management
- [ ] CSRF protection enabled

#### System Security
- [ ] Non-privileged service user
- [ ] Firewall configured (ports 22, 80, 443 only)
- [ ] SSL/HTTPS certificates installed
- [ ] Regular security updates
- [ ] Log monitoring and rotation

#### Network Security
- [ ] Reverse proxy (Nginx) configured
- [ ] Security headers enabled
- [ ] Rate limiting implemented
- [ ] DDoS protection considered

### Security Implementation

#### Flask Security (Automated)
```bash
# Automated security setup
cd "Flask Migration"
sudo ./deploy.sh  # Includes firewall, user creation, file permissions
```

#### Manual Security Hardening
```bash
# Firewall setup
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable

# SSL certificate (Let's Encrypt)
sudo certbot --nginx -d your-domain.com
```

## 📈 Performance Optimization

### Application Performance

#### Flask Performance Tuning
```bash
# Adjust worker processes (CPU cores × 2 + 1)
sudo nano /etc/systemd/system/restaurant-tracker.service
# Modify: --workers 4

# Enable caching
# Add Redis for session storage and caching
```

#### Resource Monitoring
```bash
# Monitor Flask application
./service-manager.sh health

# System resource monitoring
htop
iotop
sudo systemctl status restaurant-tracker
```

### Infrastructure Scaling

#### Vertical Scaling
- **CPU**: Increase server CPU cores
- **Memory**: Add RAM for larger datasets
- **Storage**: Use SSD for better I/O performance

#### Horizontal Scaling
- **Load Balancer**: Nginx or HAProxy for multiple instances
- **Database**: External PostgreSQL for data persistence
- **File Storage**: Shared storage (NFS, cloud storage)
- **Session Storage**: Redis for session sharing

## 🔍 Troubleshooting by Platform

### General Issues

#### Port Conflicts
```bash
# Find process using port 5000
sudo lsof -i :5000
sudo kill -9 <PID>

# Or use different port
export PORT=5001
```

#### Permission Issues
```bash
# Flask permissions
sudo chown -R restaurant-tracker:restaurant-tracker /opt/restaurant-tracker
sudo chmod +x /opt/restaurant-tracker/start.sh

# File upload permissions
chmod 755 uploads/ exports/
```

### Platform-Specific Troubleshooting

#### Flask Service Issues
```bash
# Service logs
sudo journalctl -u restaurant-tracker -f

# Application logs
tail -f /opt/restaurant-tracker/logs/error.log

# Restart service
sudo systemctl restart restaurant-tracker
```

#### Docker Issues
```bash
# Container logs
docker-compose logs -f

# CPU compatibility issues
./run-cpu-compatible-legacy.sh

# Rebuild containers
docker-compose build --no-cache
```

📖 **See**: [Docker Troubleshooting Guide](Docker%20Deployment/TROUBLESHOOTING.md)

#### Cloud Platform Issues
- **Heroku**: Check build logs and runtime logs
- **DigitalOcean**: Verify build/run commands and environment variables
- **AWS**: Check Elastic Beanstalk logs and health status

## 🔄 Updates and Maintenance

### Regular Maintenance Schedule

#### Weekly Tasks
- Review application logs for errors
- Monitor system resource usage
- Check SSL certificate expiration
- Verify backup functionality

#### Monthly Tasks
- Update system packages
- Update Python dependencies
- Review security logs
- Performance monitoring review

#### Quarterly Tasks
- Full system backup test
- Security audit
- Disaster recovery test
- Performance optimization review

### Update Procedures

#### Flask Application Updates
```bash
# Backup current version
sudo cp -r /opt/restaurant-tracker /opt/restaurant-tracker-backup-$(date +%Y%m%d)

# Update application
cd "Flask Migration"
sudo ./service-manager.sh update

# Verify update
./service-manager.sh health
```

#### Docker Updates
```bash
cd "Docker Deployment"
docker-compose pull
docker-compose up --build -d
docker image prune -f
```

## 🆘 Support and Resources

### Documentation Quick Links
- **[Flask Production Guide](Flask%20Migration/DEPLOYMENT.md)** - Detailed Flask deployment
- **[System Service Management](Flask%20Migration/SYSTEMD_SERVICE.md)** - Linux service configuration
- **[Docker Deployment](Docker%20Deployment/README.md)** - Container deployment
- **[Troubleshooting](Docker%20Deployment/TROUBLESHOOTING.md)** - Common issues and solutions
- **[Project Architecture](replit.md)** - Technical specifications

### Management Scripts
All deployment methods include management tools:
- **Flask**: `service-manager.sh` for comprehensive service management
- **Docker**: Standard `docker-compose` commands with custom scripts
- **Development**: `setup.sh` and `start.sh` for quick environment setup

### Community and Issues
- Check [recent changes](replit.md) for latest updates and known issues
- Review platform-specific documentation for detailed troubleshooting
- Use included health check tools for debugging

---

> **🎯 Production Recommendation**: For production deployments, use the [Flask implementation](Flask%20Migration/README.md) with the [automated deployment script](Flask%20Migration/DEPLOYMENT.md) for enterprise-grade reliability and universal hosting compatibility.