# Restaurant Ingredient Tracker - Docker Deployment

Complete Docker deployment solution with CPU compatibility support for the Restaurant Ingredient Tracker application.

## Quick Start

### Standard Systems
```bash
cd "Docker Deployment"
./run-fixed.sh
```

### SSE4a-Only CPUs (Older AMD Processors)
```bash
cd "Docker Deployment"
./run-cpu-compatible.sh
```

## Available Configurations

### 1. Standard Configuration
- **File**: `docker-compose.yml`
- **Features**: Redis caching, Nginx proxy, full production setup
- **Use case**: Production deployments with full features

### 2. Simplified Configuration  
- **File**: `docker-compose.simple.yml`
- **Features**: Streamlit only, no external dependencies
- **Use case**: Quick testing, development, minimal setup

### 3. CPU-Compatible Configuration
- **File**: `docker-compose.cpu-compatible.yml`
- **Features**: Compiled from source for SSE4a-only processors
- **Use case**: Older AMD CPUs that crash with "Illegal instruction"

## CPU Compatibility Issue

### Problem
The "Illegal instruction (core dumped)" error occurs on processors that only support SSE4a instruction set (common on older AMD chips). Modern Python packages like NumPy and Pandas are pre-compiled with SSE4.1/AVX instructions.

### Solution
The CPU-compatible build:
- Compiles NumPy and Pandas from source
- Avoids pre-compiled binaries with newer instructions
- Uses CPU-safe package versions
- Takes longer to build (10-15 minutes) but guarantees compatibility

### Technical Details
```bash
# Packages compiled from source
numpy==1.24.4
pandas==2.0.3

# Environment variables set
OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1
NUMBA_DISABLE_JIT=1
```

## Files Overview

| File | Purpose |
|------|---------|
| `Dockerfile` | Standard multi-stage build |
| `Dockerfile.cpu-compatible` | CPU-compatible build with source compilation |
| `docker-compose.yml` | Full production setup |
| `docker-compose.simple.yml` | Minimal Streamlit-only setup |
| `docker-compose.cpu-compatible.yml` | SSE4a-compatible setup |
| `run-fixed.sh` | Automated deployment script (standard) |
| `run-cpu-compatible.sh` | Automated deployment script (CPU-compatible) |
| `.env.example` | Environment variables template |

## Manual Deployment

### For Standard Systems
```bash
# Copy environment file
cp .env.example .env

# Start application
docker-compose -f docker-compose.simple.yml up --build

# Access at http://localhost:8501
```

### For SSE4a-Only CPUs
```bash
# Copy environment file
cp .env.example .env

# Build and start (takes 10-15 minutes)
docker-compose -f docker-compose.cpu-compatible.yml up --build

# Access at http://localhost:8501
```

## Demo Accounts

When not using Replit Auth, these demo accounts are available:
- **admin** / **admin123**
- **manager** / **manager456**
- **staff** / **staff789**

## Useful Commands

```bash
# View logs
docker-compose -f [compose-file] logs -f

# Stop services
docker-compose -f [compose-file] down

# Restart services
docker-compose -f [compose-file] restart

# Check status
docker-compose -f [compose-file] ps

# Clean rebuild
docker-compose -f [compose-file] down --rmi all
docker-compose -f [compose-file] build --no-cache
```

## Troubleshooting

For detailed troubleshooting, see `TROUBLESHOOTING.md`.

### Common Issues
- **Port conflicts**: Change port mapping in compose file
- **Build failures**: Check disk space and internet connection
- **Permission errors**: Fix file ownership with `chown`
- **Health check failures**: Increase timeout values

### Getting Help
1. Check logs: `docker-compose logs`
2. Verify CPU compatibility: `lscpu | grep flags`
3. Check resources: `df -h && free -h`
4. Review troubleshooting guide

## Production Considerations

- Use `docker-compose.yml` for full production setup
- Configure SSL certificates for HTTPS
- Set up log rotation and monitoring
- Implement backup strategy for data volumes
- Consider using Docker Swarm or Kubernetes for scaling