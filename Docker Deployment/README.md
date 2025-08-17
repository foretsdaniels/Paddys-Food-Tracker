# Restaurant Ingredient Tracker - Docker Deployment Guide

> **Containerized Deployment with CPU Compatibility Solutions**

Complete Docker deployment guide with specialized configurations for older systems and CPU compatibility issues.

## 📖 Documentation Links

- **[Main Project README](../README.md)** - Project overview and implementation comparison
- **[Flask Implementation](../Flask%20Migration/README.md)** - Production Flask version
- **[Master Deployment Guide](../DEPLOYMENT.md)** - Cross-platform deployment options
- **[Troubleshooting Guide](TROUBLESHOOTING.md)** - Docker-specific issues and solutions
- **[Flask Deployment Guide](../Flask%20Migration/DEPLOYMENT.md)** - Flask production deployment
- **[System Service Setup](../Flask%20Migration/SYSTEMD_SERVICE.md)** - Linux systemd services
- **[Project Architecture](../replit.md)** - Technical specifications and changes

## 🐳 Docker Deployment Options

This directory provides **three Docker configurations** to handle different deployment scenarios and CPU compatibility requirements:

### 1. Standard Configuration
- **File**: `docker-compose.yml`
- **Purpose**: Modern systems with full CPU instruction sets
- **Best For**: Development, modern cloud platforms, recent hardware

### 2. CPU-Compatible Configuration  
- **File**: `docker-compose.cpu-compatible.yml`
- **Purpose**: Older systems lacking AVX/SSE4.1 instructions
- **Best For**: Legacy servers, budget VPS, older hardware

### 3. Legacy-Compatible Configuration
- **File**: `docker-compose.cpu-compatible-legacy.yml`
- **Purpose**: Docker Compose 1.25.0 compatibility with CPU fixes
- **Best For**: Older Docker installations, compatibility requirements

## 🚀 Quick Start

### Standard Deployment (Modern Systems)
```bash
cd "Docker Deployment"
docker-compose up --build -d
```

### CPU-Compatible Deployment (Older Systems)
```bash
cd "Docker Deployment"
chmod +x run-cpu-compatible-legacy.sh
./run-cpu-compatible-legacy.sh
```

### Test Deployment
```bash
cd "Docker Deployment"
chmod +x test-compose.sh
./test-compose.sh
```

## 📁 Directory Structure

```
Docker Deployment/
├── README.md                           # This documentation
├── TROUBLESHOOTING.md                  # Docker-specific troubleshooting
├── docker-compose.yml                 # Standard configuration
├── docker-compose.cpu-compatible.yml  # CPU compatibility fixes
├── docker-compose.cpu-compatible-legacy.yml # Legacy Docker compatibility
├── docker-compose.simple.yml          # Minimal configuration
├── docker-compose.override.yml        # Development overrides
├── Dockerfile                         # Standard container image
├── Dockerfile.cpu-compatible          # CPU-compatible image
├── run-cpu-compatible.sh             # CPU-compatible deployment script
├── run-cpu-compatible-legacy.sh      # Legacy-compatible deployment script
├── run-fixed.sh                      # Fixed deployment script
├── test-compose.sh                   # Deployment testing script
└── scripts/                          # Additional deployment scripts
```

## 🔧 Configuration Details

### Standard Docker Compose (`docker-compose.yml`)
```yaml
version: '3.8'
services:
  streamlit-app:
    build: ../
    ports:
      - "5000:5000"
    environment:
      - STREAMLIT_SERVER_PORT=5000
    volumes:
      - ../uploads:/app/uploads
      - ../sample_data:/app/sample_data
```

### CPU-Compatible Configuration
- **Source Compilation**: Builds NumPy/Pandas from source
- **No AVX Dependencies**: Avoids AVX and SSE4.1 instruction requirements
- **Alpine Base**: Lightweight Linux distribution
- **Compatibility Focus**: Works on older processors

### Legacy Docker Compose Format
- **Version 2.0**: Compatible with Docker Compose 1.25.0+
- **No Network Specifications**: Avoids networking KeyError bugs
- **Simplified Syntax**: Reduced configuration complexity

## 🛠️ Deployment Scripts

### `run-cpu-compatible-legacy.sh` (Recommended)
```bash
#!/bin/bash
# Primary deployment script with maximum compatibility
# - Uses legacy Docker Compose format
# - Includes CPU compatibility fixes
# - Handles Docker Compose 1.25.0 networking bug
# - Provides comprehensive error handling
```

### `run-cpu-compatible.sh`
```bash
#!/bin/bash
# Modern CPU-compatible deployment
# - Uses version 3.8 format
# - CPU compatibility without legacy Docker issues
# - Best for newer Docker installations
```

### `test-compose.sh`
```bash
#!/bin/bash
# Deployment testing and validation
# - Tests multiple configurations
# - Validates deployment success
# - Provides debugging information
```

## 🐛 Common Issues and Solutions

### "Illegal instruction (core dumped)" Error
**Problem**: Application crashes on older CPUs without AVX/SSE4.1 support

**Solution**: Use CPU-compatible configuration
```bash
./run-cpu-compatible-legacy.sh
```

### Docker Compose Networking KeyError
**Problem**: Docker Compose 1.25.0 networking configuration bug

**Solution**: Use legacy format configuration
```bash
docker-compose -f docker-compose.cpu-compatible-legacy.yml up --build
```

### Port Already in Use
**Problem**: Port 5000 is occupied by another process

**Solution**: Stop conflicting service or use different port
```bash
# Find process using port 5000
sudo lsof -i :5000

# Kill process or stop service
sudo systemctl stop <service-name>

# Or modify port in docker-compose.yml
ports:
  - "5001:5000"  # Use port 5001 instead
```

### Container Build Failures
**Problem**: Build process fails due to dependency issues

**Solution**: Use pre-built configurations
```bash
# Clear Docker cache
docker system prune -a

# Rebuild with no cache
docker-compose build --no-cache

# Use CPU-compatible version
./run-cpu-compatible-legacy.sh
```

## 📊 Performance Comparison

| Configuration | Startup Time | Memory Usage | CPU Compatibility | Docker Version |
|---------------|--------------|--------------|-------------------|----------------|
| **Standard** | ~30 seconds | ~200MB | Modern CPUs only | 3.8+ |
| **CPU-Compatible** | ~45 seconds | ~150MB | All CPUs | 3.8+ |
| **Legacy-Compatible** | ~45 seconds | ~150MB | All CPUs | 1.25.0+ |

## 🔍 Debugging and Monitoring

### Container Logs
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f streamlit-app

# View last 100 lines
docker-compose logs --tail=100
```

### Container Status
```bash
# Check running containers
docker-compose ps

# View resource usage
docker stats

# Access container shell
docker-compose exec streamlit-app /bin/bash
```

### Health Checks
```bash
# Test application response
curl http://localhost:5000

# Check container health
docker-compose exec streamlit-app ps aux

# Verify file mounts
docker-compose exec streamlit-app ls -la /app/uploads
```

## 🔒 Security Considerations

### Network Security
- Containers run on isolated Docker networks
- Only necessary ports exposed to host
- No privileged containers required

### Data Security
- Uploads mounted as volumes for persistence
- Sample data read-only mounted
- Container filesystem is ephemeral

### Access Control
- Application-level authentication maintained
- No additional container privileges needed
- Standard Docker security practices

## 📈 Scaling and Production

### Horizontal Scaling
```bash
# Scale application instances
docker-compose up --scale streamlit-app=3

# Load balancer configuration
# Add Nginx container for load balancing
```

### Production Deployment
```bash
# Use production configuration
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Enable restart policies
# restart: unless-stopped (included in configurations)
```

### Monitoring
```bash
# Container monitoring
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"

# Log monitoring
docker-compose logs -f | grep ERROR

# Health monitoring
curl -f http://localhost:5000 || docker-compose restart
```

## 🔄 Updates and Maintenance

### Update Procedure
```bash
# Pull latest images
docker-compose pull

# Rebuild and restart
docker-compose up --build -d

# Clean old images
docker image prune -f
```

### Backup and Restore
```bash
# Backup uploaded data
docker cp $(docker-compose ps -q streamlit-app):/app/uploads ./backup-uploads

# Restore data
docker cp ./backup-uploads/. $(docker-compose ps -q streamlit-app):/app/uploads/
```

## 🆘 Troubleshooting Resources

### Quick Diagnostics
```bash
# Run comprehensive test
./test-compose.sh

# Check CPU compatibility
cat /proc/cpuinfo | grep -E "(avx|sse4_1)"

# Test Docker installation
docker --version && docker-compose --version
```

### Common Solutions
1. **CPU Issues**: Use `run-cpu-compatible-legacy.sh`
2. **Docker Version Issues**: Use legacy format configurations
3. **Port Conflicts**: Modify port mappings in compose files
4. **Build Failures**: Clear cache and use CPU-compatible images

### Additional Help
- **[Detailed Troubleshooting](TROUBLESHOOTING.md)** - Comprehensive issue resolution guide
- **[Flask Alternative](../Flask%20Migration/README.md)** - Non-Docker production option
- **[Project Architecture](../replit.md)** - Technical specifications and recent changes

---

> **🎯 Recommendation**: For production deployments, consider the [Flask implementation](../Flask%20Migration/README.md) which offers better performance and hosting compatibility. Use Docker for development, testing, and containerized production environments.