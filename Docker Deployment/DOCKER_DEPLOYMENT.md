# Restaurant Ingredient Tracker - Docker Deployment Guide

This guide provides comprehensive instructions for deploying the Restaurant Ingredient Tracker application using Docker and Docker Compose, including specialized CPU compatibility solutions.

## 🚨 CPU Compatibility Notice

If you experience "Illegal instruction (core dumped)" errors, your CPU likely only supports SSE4a (older AMD processors). Use the CPU-compatible configuration:

```bash
cd "Docker Deployment"
./run-cpu-compatible.sh
```

**Why this happens**: Pre-compiled Python packages (NumPy, Pandas) often use SSE4.1/AVX instructions that crash on SSE4a-only processors. The CPU-compatible build compiles from source without these dependencies.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Prerequisites](#prerequisites)
- [Configuration](#configuration)
- [Deployment Options](#deployment-options)
- [Development Setup](#development-setup)
- [Production Deployment](#production-deployment)
- [Troubleshooting](#troubleshooting)
- [Maintenance](#maintenance)

## 🚀 Quick Start

### 1. Clone and Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd restaurant-ingredient-tracker

# Copy environment template
cp .env.example .env

# Edit environment variables
nano .env  # or use your preferred editor
```

### 2. Basic Deployment
```bash
# Start the application
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f restaurant-tracker
```

### 3. Access Application
- Open your browser to `http://localhost:8501`
- Use demo credentials (see .env.example for details)

## 📦 Prerequisites

### System Requirements
- **Docker**: Version 20.10 or later
- **Docker Compose**: Version 2.0 or later
- **Memory**: Minimum 1GB RAM available for containers
- **Storage**: At least 2GB free disk space

### Installation Commands

#### Ubuntu/Debian
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER
```

#### CentOS/RHEL
```bash
# Install Docker
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker
```

#### macOS
```bash
# Using Homebrew
brew install docker docker-compose

# Or download Docker Desktop from docker.com
```

#### Windows
Download and install Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop)

## ⚙️ Configuration

### Environment Setup

1. **Copy the environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit key configuration values:**
   ```bash
   # Required: Change security keys
   SESSION_SECRET_KEY=your-unique-secret-key-here
   REDIS_PASSWORD=your-secure-redis-password

   # Optional: Customize ports
   HOST_PORT=8501
   NGINX_HTTP_PORT=80
   NGINX_HTTPS_PORT=443

   # Optional: Set timezone
   TIMEZONE=America/New_York
   ```

3. **Generate secure keys:**
   ```bash
   # Generate session secret
   python3 -c "import secrets; print('SESSION_SECRET_KEY=' + secrets.token_hex(32))"

   # Generate Redis password
   python3 -c "import secrets; print('REDIS_PASSWORD=' + secrets.token_urlsafe(16))"
   ```

### Directory Structure

Create necessary directories:
```bash
mkdir -p data logs exports config ssl
chmod 755 data logs exports
```

## 🎯 Deployment Options

### Option 1: Development Mode
For local development with hot reload:

```bash
# Start development environment
docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d

# View development logs
docker-compose logs -f restaurant-tracker
```

**Features:**
- Hot reload on code changes
- Debug mode enabled
- Simplified configuration
- No Redis or Nginx dependencies

### Option 2: Production Mode (Basic)
For simple production deployment:

```bash
# Start production environment
docker-compose up -d

# Check health
docker-compose ps
```

**Features:**
- Optimized production image
- Redis for session management
- Health checks enabled
- Resource limits applied

### Option 3: Production Mode (with Nginx)
For production with reverse proxy:

```bash
# Start with Nginx proxy
docker-compose --profile production up -d

# Configure SSL (optional)
./scripts/setup-ssl.sh
```

**Features:**
- Nginx reverse proxy
- SSL/TLS termination
- Load balancing ready
- Production security headers

## 🛠️ Development Setup

### Setting Up Development Environment

1. **Start development containers:**
   ```bash
   docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d
   ```

2. **Enable code hot-reload:**
   ```bash
   # Code changes will automatically reload the application
   # Edit app.py and see changes instantly
   ```

3. **Access development tools:**
   ```bash
   # View application logs
   docker-compose logs -f restaurant-tracker

   # Access container shell
   docker-compose exec restaurant-tracker bash

   # Run tests
   docker-compose exec restaurant-tracker python -m pytest
   ```

### Development Commands

```bash
# Rebuild development image
docker-compose build restaurant-tracker

# Reset development data
docker-compose down -v
docker-compose up -d

# Debug container issues
docker-compose exec restaurant-tracker bash
```

## 🏭 Production Deployment

### Production Checklist

- [ ] **Security Configuration**
  - [ ] Change default passwords in `.env`
  - [ ] Set strong `SESSION_SECRET_KEY`
  - [ ] Configure `REDIS_PASSWORD`
  - [ ] Set `APP_ENV=production`
  - [ ] Disable `APP_DEBUG=false`

- [ ] **SSL/TLS Setup**
  - [ ] Obtain SSL certificates
  - [ ] Configure Nginx SSL settings
  - [ ] Set up automatic certificate renewal

- [ ] **Monitoring**
  - [ ] Configure log aggregation
  - [ ] Set up health check monitoring
  - [ ] Configure backup procedures

### SSL Certificate Setup

#### Using Let's Encrypt
```bash
# Install Certbot
sudo apt-get install certbot

# Obtain certificate
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ./ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ./ssl/key.pem

# Set permissions
sudo chown $(id -u):$(id -g) ./ssl/*.pem
chmod 600 ./ssl/*.pem
```

#### Using Self-Signed Certificates (Development)
```bash
# Generate self-signed certificate
openssl req -x509 -newkey rsa:4096 -keyout ssl/key.pem -out ssl/cert.pem -days 365 -nodes
```

### Production Startup

```bash
# Start production services
docker-compose --profile production up -d

# Verify all services are running
docker-compose ps

# Check application health
curl -f http://localhost/_stcore/health
```

## 🔧 Troubleshooting

### Common Issues

#### Container Won't Start
```bash
# Check container logs
docker-compose logs restaurant-tracker

# Check container status
docker-compose ps

# Restart specific service
docker-compose restart restaurant-tracker
```

#### Permission Issues
```bash
# Fix directory permissions
sudo chown -R $(id -u):$(id -g) data logs exports

# Check container user
docker-compose exec restaurant-tracker id
```

#### Port Conflicts
```bash
# Check what's using the port
sudo netstat -tlpn | grep :8501

# Change port in .env file
echo "HOST_PORT=8502" >> .env
docker-compose up -d
```

#### Memory Issues
```bash
# Check container memory usage
docker stats

# Increase memory limits in docker-compose.yml
# Or check available system memory
free -h
```

### Health Checks

```bash
# Check application health
curl -f http://localhost:8501/_stcore/health

# Check Redis health
docker-compose exec redis redis-cli ping

# Check Nginx health (if using)
curl -f http://localhost/health
```

### Log Analysis

```bash
# View real-time logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f restaurant-tracker

# Export logs for analysis
docker-compose logs --no-color > app.log 2>&1
```

## 🔄 Maintenance

### Regular Tasks

#### Daily
```bash
# Check container health
docker-compose ps

# Review application logs
docker-compose logs --tail=100 restaurant-tracker
```

#### Weekly
```bash
# Update container images
docker-compose pull
docker-compose up -d

# Clean up unused images
docker image prune -f
```

#### Monthly
```bash
# Full system cleanup
docker system prune -f

# Backup data volumes
./scripts/backup-data.sh

# Update SSL certificates (if using Let's Encrypt)
sudo certbot renew
```

### Backup Procedures

#### Data Backup
```bash
# Create backup directory
mkdir -p backups/$(date +%Y%m%d)

# Backup application data
tar -czf backups/$(date +%Y%m%d)/data.tar.gz data/

# Backup Redis data (if needed)
docker-compose exec redis redis-cli BGSAVE
docker cp restaurant-tracker-redis:/data/dump.rdb backups/$(date +%Y%m%d)/
```

#### Configuration Backup
```bash
# Backup configuration files
tar -czf backups/$(date +%Y%m%d)/config.tar.gz .env docker-compose.yml config/
```

### Updates and Upgrades

#### Application Updates
```bash
# Pull latest code
git pull origin main

# Rebuild containers
docker-compose build

# Update with minimal downtime
docker-compose up -d --no-deps restaurant-tracker
```

#### Security Updates
```bash
# Update base images
docker-compose pull

# Rebuild with latest security patches
docker-compose build --no-cache

# Rolling restart
docker-compose up -d
```

## 📊 Monitoring

### Container Monitoring
```bash
# View resource usage
docker stats

# Monitor specific container
docker stats restaurant-tracker-app

# Check container health
docker-compose ps
```

### Application Monitoring
```bash
# Health endpoint
curl http://localhost:8501/_stcore/health

# Application metrics
curl http://localhost:8501/_stcore/metrics

# Log monitoring
tail -f logs/app.log
```

### Alerts Setup

Configure monitoring alerts for:
- Container restart events
- High memory usage (>80%)
- High CPU usage (>80%)
- Disk space usage (>85%)
- Application errors
- Failed health checks

## 🔐 Security Best Practices

1. **Network Security**
   - Use internal networks for inter-service communication
   - Expose only necessary ports
   - Configure firewall rules

2. **Container Security**
   - Run containers as non-root user
   - Use minimal base images
   - Keep images updated

3. **Data Security**
   - Encrypt sensitive data at rest
   - Use secure passwords
   - Regular security audits

4. **Access Control**
   - Implement proper authentication
   - Use HTTPS in production
   - Monitor access logs

## 📞 Support

For issues and questions:

1. Check the troubleshooting section above
2. Review container logs: `docker-compose logs`
3. Check the application README.md
4. Create an issue in the project repository

## 📄 License

This deployment configuration is part of the Restaurant Ingredient Tracker project.
Please refer to the main project license for terms and conditions.