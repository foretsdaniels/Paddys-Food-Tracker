# Restaurant Ingredient Tracker - Flask Edition Deployment Guide

> **Production deployment guide for the Flask implementation**

This guide covers deploying the Flask-based Restaurant Ingredient Tracker on various platforms and environments.

## 📖 Related Documentation

- **[Main README](../README.md)** - Project overview and implementation comparison
- **[Flask Implementation Guide](README.md)** - Complete Flask implementation overview
- **[Master Deployment Guide](../DEPLOYMENT.md)** - Cross-platform deployment options
- **[System Service Setup](SYSTEMD_SERVICE.md)** - Linux systemd service configuration
- **[Docker Deployment](../Docker%20Deployment/README.md)** - Container deployment options
- **[Docker Troubleshooting](../Docker%20Deployment/TROUBLESHOOTING.md)** - Container-specific issues
- **[Project Architecture](../replit.md)** - Technical specifications and changes

## Quick Start

### Local Development
```bash
cd "Flask Migration"
chmod +x setup.sh start.sh
./setup.sh
./start.sh
```

### Production Deployment
```bash
# Install as system service
sudo ./deploy.sh
sudo systemctl start restaurant-tracker
sudo systemctl enable restaurant-tracker
```

## Platform-Specific Deployment

### 1. Ubuntu/Debian VPS Deployment

#### Prerequisites
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx supervisor -y

# Install Node.js (optional, for future enhancements)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs
```

#### Automated Deployment
```bash
# Clone/copy the Flask Migration folder to your server
cd Flask\ Migration

# Run automated deployment
sudo chmod +x deploy.sh
sudo ./deploy.sh

# The application will be available at http://your-server-ip
```

#### Manual Deployment
```bash
# Create application user
sudo useradd --system --shell /bin/bash --home /opt/restaurant-tracker restaurant-tracker

# Copy application files
sudo cp -r . /opt/restaurant-tracker/
sudo chown -R restaurant-tracker:restaurant-tracker /opt/restaurant-tracker/

# Setup virtual environment
sudo -u restaurant-tracker python3 -m venv /opt/restaurant-tracker/venv
sudo -u restaurant-tracker /opt/restaurant-tracker/venv/bin/pip install -r /opt/restaurant-tracker/requirements.txt

# Setup systemd service
sudo cp restaurant-tracker.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl start restaurant-tracker
sudo systemctl enable restaurant-tracker

# Setup Nginx (optional)
sudo cp nginx.conf /etc/nginx/sites-available/restaurant-tracker
sudo ln -s /etc/nginx/sites-available/restaurant-tracker /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx
```

### 2. CentOS/RHEL Deployment

```bash
# Install dependencies
sudo yum update -y
sudo yum install python3 python3-pip nginx supervisor -y

# Follow similar steps as Ubuntu, but use:
# - yum instead of apt
# - Different service paths if needed
```

### 3. Docker Deployment

#### Simple Docker Run
```bash
cd Flask\ Migration
docker build -t restaurant-tracker .
docker run -d -p 5000:5000 --name restaurant-tracker restaurant-tracker
```

#### Docker Compose (Recommended)
```bash
# Production deployment with persistence
docker-compose -f docker-compose.prod.yml up -d

# Development deployment
docker-compose up -d
```

#### Docker Swarm (Multi-node)
```bash
# Initialize swarm (on manager node)
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.prod.yml restaurant-tracker
```

### 4. Cloud Platform Deployment

#### Heroku
```bash
# Install Heroku CLI
# Create Procfile (already included)
heroku create your-app-name
git init
git add .
git commit -m "Initial deployment"
git push heroku main
```

#### DigitalOcean App Platform
1. Connect Git repository
2. Select "Web Service"
3. Set build command: `pip install -r requirements.txt`
4. Set run command: `gunicorn --bind 0.0.0.0:$PORT app:app`
5. Set environment variables

#### AWS Elastic Beanstalk
```bash
# Install EB CLI
pip install awsebcli

# Initialize and deploy
eb init
eb create restaurant-tracker-prod
eb deploy
```

#### Google Cloud Run
```bash
# Build and deploy
gcloud run deploy restaurant-tracker \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### 5. Shared Hosting Deployment

Many shared hosting providers support Python/Flask applications:

#### cPanel/WHM Hosting
1. Upload files to public_html or subdirectory
2. Create virtual environment in hosting control panel
3. Install dependencies via pip
4. Configure WSGI application
5. Set startup file to `app.py`

#### Hostinger/Namecheap
1. Use File Manager to upload application
2. Setup Python environment in hosting panel
3. Configure application startup

## System Service Configuration

### Systemd Service (Linux)

The application includes a systemd service file (`restaurant-tracker.service`):

```ini
[Unit]
Description=Restaurant Ingredient Tracker Flask Application
After=network.target

[Service]
User=restaurant-tracker
Group=restaurant-tracker
WorkingDirectory=/opt/restaurant-tracker
Environment=PATH=/opt/restaurant-tracker/venv/bin
ExecStart=/opt/restaurant-tracker/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 2 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

#### Service Management Commands
```bash
# Start service
sudo systemctl start restaurant-tracker

# Stop service
sudo systemctl stop restaurant-tracker

# Restart service
sudo systemctl restart restaurant-tracker

# Enable auto-start on boot
sudo systemctl enable restaurant-tracker

# Disable auto-start
sudo systemctl disable restaurant-tracker

# Check status
sudo systemctl status restaurant-tracker

# View logs
sudo journalctl -u restaurant-tracker -f
```

### Supervisor Configuration (Alternative)

For systems without systemd, use Supervisor:

```ini
[program:restaurant-tracker]
command=/opt/restaurant-tracker/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 2 app:app
directory=/opt/restaurant-tracker
user=restaurant-tracker
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/restaurant-tracker.log
```

## Nginx Configuration (Reverse Proxy)

For production deployments, use Nginx as a reverse proxy:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static {
        alias /opt/restaurant-tracker/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}
```

### SSL/HTTPS Setup with Let's Encrypt
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Get SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

## Environment Configuration

### Production Environment Variables
```bash
# /opt/restaurant-tracker/.env
FLASK_ENV=production
SECRET_KEY=your-very-secure-secret-key-here
PORT=5000
DEBUG=False

# Database (if using external DB)
DATABASE_URL=postgresql://user:password@host:port/database

# File storage
UPLOAD_FOLDER=/opt/restaurant-tracker/uploads
EXPORT_FOLDER=/opt/restaurant-tracker/exports

# Security
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_HTTPONLY=True
```

### Development Environment
```bash
# Local .env
FLASK_ENV=development
SECRET_KEY=dev-secret-key
PORT=5000
DEBUG=True
```

## Performance Tuning

### Gunicorn Configuration
```python
# gunicorn.conf.py
bind = "0.0.0.0:5000"
workers = 2
worker_connections = 1000
timeout = 120
keepalive = 5
max_requests = 1000
max_requests_jitter = 100
preload_app = True
```

### Application Performance
```python
# app.py optimizations
from flask_caching import Cache

# Add caching
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Cache expensive operations
@cache.memoize(timeout=300)
def process_large_datasets():
    pass
```

## Monitoring and Logging

### Log Configuration
```python
# Add to app.py
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler(
        'logs/restaurant-tracker.log', 
        maxBytes=10240000, 
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
```

### Health Check Endpoint
```python
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'timestamp': datetime.now().isoformat()}
```

## Security Considerations

### Production Security Checklist
- [ ] Use strong SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Set secure session cookies
- [ ] Implement rate limiting
- [ ] Regular security updates
- [ ] Firewall configuration
- [ ] File upload validation
- [ ] SQL injection prevention
- [ ] XSS protection headers

### Firewall Configuration (UFW)
```bash
# Basic firewall setup
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

## Backup and Recovery

### Database Backup (if using external DB)
```bash
# PostgreSQL backup
pg_dump -h host -U user -d restaurant_tracker > backup.sql

# Restore
psql -h host -U user -d restaurant_tracker < backup.sql
```

### File Backup
```bash
# Backup uploads and exports
tar -czf backup-$(date +%Y%m%d).tar.gz uploads/ exports/ logs/

# Automated backup script
#!/bin/bash
DATE=$(date +%Y%m%d)
tar -czf /backups/restaurant-tracker-$DATE.tar.gz /opt/restaurant-tracker/uploads /opt/restaurant-tracker/exports
find /backups -name "restaurant-tracker-*.tar.gz" -mtime +30 -delete
```

## Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Find process using port 5000
sudo lsof -i :5000
sudo kill -9 <PID>
```

#### Permission Issues
```bash
# Fix file permissions
sudo chown -R restaurant-tracker:restaurant-tracker /opt/restaurant-tracker
sudo chmod +x /opt/restaurant-tracker/start.sh
```

#### Memory Issues
```bash
# Check memory usage
free -h
sudo systemctl status restaurant-tracker

# Adjust worker count in gunicorn
# Reduce workers if memory is limited
```

#### Service Won't Start
```bash
# Check service logs
sudo journalctl -u restaurant-tracker -n 50
sudo systemctl status restaurant-tracker

# Check application logs
tail -f /opt/restaurant-tracker/logs/restaurant-tracker.log
```

## Scaling Considerations

### Horizontal Scaling
- Use load balancer (Nginx, HAProxy)
- Deploy multiple application instances
- Shared file storage (NFS, cloud storage)
- External database for session storage

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Adjust worker processes
- Optimize database queries
- Implement caching

## Support and Maintenance

### Regular Maintenance Tasks
1. **Weekly**: Check logs for errors
2. **Monthly**: Update dependencies
3. **Quarterly**: Security audit
4. **Annually**: Full system backup test

### Update Procedure
```bash
# Stop service
sudo systemctl stop restaurant-tracker

# Backup current version
sudo cp -r /opt/restaurant-tracker /opt/restaurant-tracker-backup

# Deploy new version
# (copy new files)

# Update dependencies
sudo -u restaurant-tracker /opt/restaurant-tracker/venv/bin/pip install -r requirements.txt

# Start service
sudo systemctl start restaurant-tracker

# Verify deployment
curl http://localhost:5000/health
```

This deployment guide ensures your Flask-based Restaurant Ingredient Tracker can be deployed reliably across various environments with proper monitoring, security, and maintenance procedures.