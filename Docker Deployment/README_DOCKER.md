# 🐳 Docker Quick Start Guide

This guide provides the essential commands to quickly deploy the Restaurant Ingredient Tracker using Docker.

## ⚠️ Fixed "Illegal instruction (core dumped)" Issue

If you experienced the "Illegal instruction (core dumped)" error, it has been resolved with these fixes:

### Quick Fix - Use Simplified Configuration:
```bash
# Navigate to Docker Deployment directory
cd "Docker Deployment"

# Use the simplified Docker Compose file (no Redis/Nginx dependencies)
docker-compose -f docker-compose.simple.yml up --build

# Access the application at http://localhost:8501
```

### What Was Fixed:
1. **Platform compatibility**: Added `platform: linux/amd64` specification
2. **System libraries**: Added missing runtime libraries (libc6, libgcc-s1, libstdc++6)
3. **Python packages**: Fixed to stable versions (streamlit==1.28.2, pandas==2.1.4)
4. **Simplified deps**: Removed Redis dependency in simple config
5. **Enhanced startup**: Longer health check startup period

## ⚡ Quick Commands

```bash
# 1. Initial setup
./scripts/deploy.sh setup

# 2. Start development environment
./scripts/deploy.sh dev

# 3. Start production environment
./scripts/deploy.sh prod

# 4. Check status
./scripts/deploy.sh status

# 5. View logs
./scripts/deploy.sh logs -f

# 6. Stop services
./scripts/deploy.sh stop
```

## 📦 What's Included

### Docker Files
- **`Dockerfile`** - Multi-stage production-ready container
- **`docker-compose.yml`** - Complete orchestration with Redis & Nginx
- **`docker-compose.override.yml`** - Development overrides
- **`.dockerignore`** - Optimized build context

### Configuration
- **`.env.example`** - Environment template with all parameters
- **`scripts/deploy.sh`** - Automated deployment script

### Services
- **Streamlit App** - Main application (Port 8501)
- **Redis** - Session management (Port 6379)
- **Nginx** - Reverse proxy (Ports 80/443) [Production profile]

## 🚀 Deployment Options

### Development
```bash
./scripts/deploy.sh dev
```
- Hot reload enabled
- Debug mode
- Simplified setup
- Direct access to Streamlit

### Production (Basic)
```bash
./scripts/deploy.sh prod
```
- Optimized containers
- Redis session management
- Health checks
- Resource limits

### Production (with Nginx)
```bash
docker-compose --profile production up -d
```
- Nginx reverse proxy
- SSL termination ready
- Production security headers

## ⚙️ Configuration

1. **Copy environment template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit key settings:**
   ```bash
   nano .env
   ```

3. **Required changes:**
   - `SESSION_SECRET_KEY` - Change to unique value
   - `REDIS_PASSWORD` - Set secure password
   - `HOST_PORT` - Customize if needed

## 🔧 Management Commands

```bash
# Setup and configuration
./scripts/deploy.sh setup          # Initial setup
./scripts/deploy.sh status         # Check service health

# Start/stop services
./scripts/deploy.sh dev            # Development mode
./scripts/deploy.sh prod           # Production mode
./scripts/deploy.sh stop           # Stop all services

# Monitoring and debugging
./scripts/deploy.sh logs           # View recent logs
./scripts/deploy.sh logs -f        # Follow logs live

# Maintenance
./scripts/deploy.sh backup         # Create backup
./scripts/deploy.sh clean          # Clean containers/volumes
```

## 📊 Health Checks

The deployment includes comprehensive health monitoring:

- **Application**: `http://localhost:8501/_stcore/health`
- **Redis**: Built-in Redis ping check
- **Container**: Docker health checks every 30 seconds

Check all health status:
```bash
./scripts/deploy.sh status
```

## 🔐 Security Features

- Non-root container user
- Security headers enabled
- Resource limits enforced
- Network isolation
- Secrets management via environment variables

## 📁 Data Persistence

Data is persisted in Docker volumes and host directories:

```
project/
├── data/          # Application data
├── logs/          # Application logs  
├── exports/       # Generated reports
├── backups/       # Automated backups
└── ssl/           # SSL certificates
```

## 🛠️ Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Change port in .env
echo "HOST_PORT=8502" >> .env
./scripts/deploy.sh prod
```

**Permission errors:**
```bash
# Fix permissions
sudo chown -R $(id -u):$(id -g) data logs exports
```

**Container won't start:**
```bash
# Check logs
./scripts/deploy.sh logs

# Check Docker daemon
docker info
```

### Debug Commands

```bash
# Access container shell
docker-compose exec restaurant-tracker bash

# Check container resources
docker stats

# View all containers
docker ps -a
```

## 📋 System Requirements

- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Memory**: 1GB+ available
- **Storage**: 2GB+ free space

## 📞 Support

For detailed documentation, see [`DOCKER_DEPLOYMENT.md`](DOCKER_DEPLOYMENT.md)

For application usage, see [`README.md`](README.md)

## 🎯 Quick Examples

### Basic Development Workflow
```bash
# Setup
./scripts/deploy.sh setup
nano .env

# Start development
./scripts/deploy.sh dev

# Make changes to app.py
# Changes auto-reload in browser

# View logs
./scripts/deploy.sh logs -f

# Stop when done
./scripts/deploy.sh stop
```

### Production Deployment
```bash
# Setup
./scripts/deploy.sh setup

# Configure production settings
nano .env
# Set APP_ENV=production
# Set strong passwords

# Start production
./scripts/deploy.sh prod

# Monitor
./scripts/deploy.sh status

# Backup data
./scripts/deploy.sh backup
```

---

🍽️ **Restaurant Ingredient Tracker** - Dockerized for easy deployment!