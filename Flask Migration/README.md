# Restaurant Ingredient Tracker - Flask Edition

> **Production-Ready Flask Implementation with Universal Hosting Compatibility**

This is the Flask-based implementation of the Restaurant Ingredient Tracker, designed for production deployment across all hosting platforms.

## 📖 Documentation Links

- **[Main Project README](../README.md)** - Project overview and implementation comparison
- **[Master Deployment Guide](../DEPLOYMENT.md)** - Cross-platform deployment options
- **[Flask Production Deployment](DEPLOYMENT.md)** - Detailed Flask deployment guide
- **[System Service Setup](SYSTEMD_SERVICE.md)** - Linux systemd service configuration
- **[Docker Deployment](../Docker%20Deployment/README.md)** - Container deployment options
- **[Troubleshooting Guide](../Docker%20Deployment/TROUBLESHOOTING.md)** - Common issues and solutions
- **[Project Architecture](../replit.md)** - Technical specifications and recent changes

## 🏗️ Flask Edition Advantages

### Universal Hosting Compatibility
- **Shared Hosting**: Works on cPanel, WHM, and standard web hosting
- **Cloud Platforms**: Native support for Heroku, DigitalOcean, AWS, GCP
- **VPS/Dedicated**: Full control with systemd services and monitoring
- **Container Platforms**: Docker and Kubernetes ready

### Performance Benefits
- **Faster Startup**: < 5 seconds vs 30+ seconds (Streamlit)
- **Lower Memory**: < 100MB vs 200+ MB (Streamlit)
- **Better Concurrency**: Handles multiple users efficiently
- **Standard Protocols**: Uses only HTTP/HTTPS (no WebSocket dependencies)

### Production Features
- **Professional UI**: Bootstrap-based responsive design
- **Service Management**: Systemd integration with health monitoring
- **Security Hardening**: Non-privileged execution, file access controls
- **Monitoring Tools**: Comprehensive logging and health checks

## 🚀 Quick Start

### Local Development
```bash
# Setup environment
chmod +x setup.sh start.sh
./setup.sh

# Start development server
./start.sh
```

### Production Deployment
```bash
# Automated production setup (Linux)
sudo ./deploy.sh

# Manual service management
sudo systemctl start restaurant-tracker
sudo systemctl enable restaurant-tracker
```

### Docker Deployment
```bash
# Development
docker-compose up --build

# Production
docker-compose -f docker-compose.prod.yml up -d
```

## 📁 Project Structure

```
Flask Migration/
├── app.py                    # Main Flask application
├── run.py                    # Development server runner
├── requirements.txt          # Python dependencies
├── .env.example             # Environment configuration template
├── utils/
│   ├── data_processor.py    # Data processing logic (identical to Streamlit)
│   └── auth.py              # Authentication handling
├── reports/
│   ├── pdf_generator.py     # PDF report generation
│   └── excel_generator.py   # Excel report generation
├── templates/
│   ├── base.html            # Base template with Bootstrap
│   ├── login.html           # Authentication page
│   ├── dashboard.html       # Main dashboard
│   ├── upload.html          # File upload interface
│   ├── analytics.html       # Data analysis page
│   ├── reports.html         # Report generation page
│   ├── settings.html        # User settings
│   └── error.html           # Error pages
├── setup.sh                 # Development environment setup
├── start.sh                 # Development server startup
├── deploy.sh                # Production deployment script
├── service-manager.sh       # Service management utility
├── restaurant-tracker.service # Systemd service file
├── nginx.conf               # Nginx reverse proxy configuration
├── docker-compose.yml       # Development Docker setup
├── docker-compose.prod.yml  # Production Docker setup
├── Dockerfile               # Container image definition
├── DEPLOYMENT.md            # Production deployment guide
├── SYSTEMD_SERVICE.md       # System service documentation
└── sample_*.csv            # Sample data files
```

## 🎯 Feature Comparison with Streamlit

| Feature | Streamlit | Flask | Notes |
|---------|-----------|-------|-------|
| **CSV Upload** | ✅ File widgets | ✅ HTML forms | Identical functionality |
| **Data Processing** | ✅ Pandas | ✅ Pandas | Same logic, same results |
| **Analytics** | ✅ Tables | ✅ Bootstrap tables | Same filtering/sorting |
| **PDF Reports** | ✅ FPDF | ✅ FPDF | Identical reports |
| **Excel Reports** | ✅ XlsxWriter | ✅ XlsxWriter | Same workbooks |
| **Authentication** | ✅ Replit Auth | ✅ Dual auth | Plus demo accounts |
| **Sample Data** | ✅ Built-in | ✅ Built-in | Same sample files |
| **Visual Alerts** | ✅ Colored rows | ✅ Bootstrap alerts | Enhanced styling |
| **Multi-page Nav** | ✅ Sidebar | ✅ Top nav | Professional layout |

## 🛠️ Management Scripts

### Setup Script (`setup.sh`)
- Creates virtual environment
- Installs dependencies
- Generates secure configuration
- Sets up directories and permissions
- Validates installation

### Start Script (`start.sh`)
- Activates environment
- Loads configuration
- Provides startup information
- Handles port conflicts
- Supports both development and production modes

### Deploy Script (`deploy.sh`)
- Automated production deployment
- Creates system user and directories
- Installs systemd service
- Configures Nginx reverse proxy
- Sets up firewall and security
- Implements log rotation

### Service Manager (`service-manager.sh`)
- Service control (start/stop/restart)
- Health monitoring and checks
- Log viewing and following
- Performance monitoring
- Update management with backups

## 🔧 Configuration

### Environment Variables (.env)
```bash
FLASK_ENV=production
SECRET_KEY=your-secure-secret-key
PORT=5000
DEBUG=False
UPLOAD_FOLDER=/path/to/uploads
EXPORT_FOLDER=/path/to/exports
```

### Systemd Service
- **Service User**: `restaurant-tracker`
- **Installation Path**: `/opt/restaurant-tracker`
- **Service Name**: `restaurant-tracker.service`
- **Auto-start**: Enabled on boot
- **Security**: Hardened with restricted permissions

### Nginx Configuration
- **Reverse Proxy**: Routes traffic to Flask application
- **Static Files**: Optimized serving with caching
- **Security Headers**: XSS protection, CSRF prevention
- **SSL/HTTPS**: Ready for Let's Encrypt integration

## 🔒 Security Features

### Application Security
- **Input Validation**: CSV structure and data validation
- **File Upload Security**: Type checking and size limits
- **Session Management**: Secure cookies with expiration
- **CSRF Protection**: Built-in Flask security features

### System Security
- **Non-privileged User**: Service runs as dedicated user
- **File Permissions**: Restricted access to sensitive files
- **Network Security**: Firewall configuration included
- **Process Isolation**: Systemd security sandboxing

## 📊 Performance Monitoring

### Built-in Health Checks
- **HTTP Endpoint**: `/health` for load balancer checks
- **Service Status**: Real-time service monitoring
- **Resource Usage**: Memory and CPU monitoring
- **Port Verification**: Network connectivity checks

### Logging
- **Application Logs**: Structured logging with rotation
- **Access Logs**: HTTP request tracking
- **Error Logs**: Detailed error information
- **System Logs**: Systemd journal integration

## 🚀 Deployment Platforms

### Linux VPS/Dedicated Servers
```bash
# Ubuntu/Debian
sudo ./deploy.sh

# Service management
sudo systemctl status restaurant-tracker
./service-manager.sh health
```

### Cloud Platforms

#### Heroku
```bash
# Create Procfile (included)
heroku create your-app-name
git push heroku main
```

#### DigitalOcean App Platform
1. Connect Git repository
2. Set build command: `pip install -r requirements.txt`
3. Set run command: `gunicorn app:app`

#### AWS Elastic Beanstalk
```bash
eb init
eb create restaurant-tracker-prod
eb deploy
```

### Shared Hosting
1. Upload files via FTP/cPanel File Manager
2. Create virtual environment in hosting control panel
3. Install dependencies via pip
4. Configure WSGI application pointing to `app.py`

### Docker Platforms
```bash
# Docker Swarm
docker stack deploy -c docker-compose.prod.yml restaurant-tracker

# Kubernetes
kubectl apply -f k8s-deployment.yaml
```

## 🔍 Troubleshooting

### Common Issues

#### Service Won't Start
```bash
# Check service status
sudo systemctl status restaurant-tracker

# View logs
sudo journalctl -u restaurant-tracker -f

# Validate service file
sudo systemd-analyze verify restaurant-tracker.service
```

#### Port Conflicts
```bash
# Find process using port
sudo lsof -i :5000

# Kill conflicting process
sudo kill -9 <PID>
```

#### Permission Errors
```bash
# Fix ownership
sudo chown -R restaurant-tracker:restaurant-tracker /opt/restaurant-tracker

# Set correct permissions
sudo chmod +x /opt/restaurant-tracker/start.sh
```

### Performance Issues
```bash
# Monitor resource usage
./service-manager.sh health

# Adjust worker count
sudo nano /etc/systemd/system/restaurant-tracker.service
# Modify --workers parameter

# Restart service
sudo systemctl daemon-reload
sudo systemctl restart restaurant-tracker
```

## 📈 Scaling and Optimization

### Horizontal Scaling
- **Load Balancer**: Nginx or HAProxy configuration
- **Multiple Instances**: Deploy across multiple servers
- **Session Storage**: External Redis for session sharing
- **File Storage**: Shared NFS or cloud storage

### Vertical Scaling
- **Resource Limits**: Adjust CPU and memory allocation
- **Worker Processes**: Scale based on CPU cores
- **Database**: External PostgreSQL for data persistence
- **Caching**: Redis for improved performance

## 🔄 Updates and Maintenance

### Regular Maintenance
- **Weekly**: Review logs for errors and performance issues
- **Monthly**: Update dependencies and security patches
- **Quarterly**: Full system backup and disaster recovery testing

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
./service-manager.sh health
```

## 🆘 Support and Resources

### Documentation
- **[Production Deployment](DEPLOYMENT.md)** - Comprehensive deployment guide
- **[System Service](SYSTEMD_SERVICE.md)** - Service management documentation
- **[Main Project](../README.md)** - Project overview and alternatives

### Scripts and Tools
- All management scripts include `--help` options
- Service manager provides comprehensive health checking
- Deployment scripts include error handling and rollback

### Community and Issues
- Check recent changes in [project architecture](../replit.md)
- Review troubleshooting guides for common solutions
- Use included logging for debugging issues

---

> **🎯 Production Ready**: This Flask implementation is designed for production use with enterprise-grade security, monitoring, and management tools. Choose this implementation for any serious deployment.