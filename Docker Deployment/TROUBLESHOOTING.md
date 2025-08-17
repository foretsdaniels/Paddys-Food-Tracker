# Docker Deployment Troubleshooting Guide

## Common Issues and Solutions

### "Illegal instruction (core dumped)" Error

**Symptom**: Streamlit container crashes immediately with "Illegal instruction (core dumped)"

**Cause**: Your CPU only supports SSE4a instruction set (common on older AMD processors). Pre-compiled Python packages use newer SSE4.1/AVX instructions.

**Solution**: 
```bash
# Use CPU-compatible configuration
cd "Docker Deployment"
./run-cpu-compatible.sh
```

**Technical Details**:
- Compiles NumPy and Pandas from source without AVX/SSE4.1 dependencies
- Uses older package versions known to work on SSE4a-only CPUs
- Build time: 10-15 minutes vs 2-3 minutes for regular build

### Port Already in Use

**Symptom**: Error binding to port 8501

**Solution**:
```bash
# Find process using port 8501
sudo lsof -i :8501

# Kill the process
sudo kill <PID>

# Or change port in docker-compose.yml
ports:
  - "8502:8501"  # Use port 8502 instead
```

### Container Fails to Start

**Symptom**: Container exits immediately

**Diagnosis**:
```bash
# Check logs
docker-compose -f docker-compose.simple.yml logs

# Check container status
docker-compose -f docker-compose.simple.yml ps
```

**Common causes**:
1. **File not found**: Ensure `app.py` exists in parent directory
2. **Permission issues**: Check file permissions
3. **Memory limit**: Increase memory limits in compose file

### Build Failures

**Symptom**: Docker build fails with compilation errors

**For CPU-compatible builds**:
- Ensure sufficient disk space (2GB+ free)
- Increase Docker memory allocation (4GB recommended)
- Check internet connection for source downloads

**Solution**:
```bash
# Clean build
docker-compose -f docker-compose.cpu-compatible.yml down --rmi all
docker-compose -f docker-compose.cpu-compatible.yml build --no-cache
```

### Health Check Failures

**Symptom**: Container shows as "unhealthy"

**Diagnosis**:
```bash
# Check health check logs
docker inspect restaurant-tracker-app | grep -A 10 Health
```

**Solution**:
```bash
# Disable health check temporarily
# Comment out healthcheck section in docker-compose.yml

# Or increase timeout
healthcheck:
  start_period: 120s  # Increase from 60s
```

### Network Issues

**Symptom**: Cannot access application on localhost:8501

**Solutions**:
1. **Check container networking**:
   ```bash
   docker-compose -f docker-compose.simple.yml ps
   # Ensure container shows "Up" status
   ```

2. **Test internal connectivity**:
   ```bash
   docker exec restaurant-tracker-app curl http://localhost:8501
   ```

3. **Check firewall settings**:
   ```bash
   sudo ufw status
   sudo ufw allow 8501/tcp
   ```

### Volume Mount Issues

**Symptom**: Data not persisting or permission errors

**Solution**:
```bash
# Fix ownership
sudo chown -R 1000:1000 ./data ./logs ./exports

# Or recreate with proper permissions
docker-compose down
rm -rf data logs exports
mkdir -p data logs exports
docker-compose up -d
```

### Docker Compose Version Issues

**Symptom**: "Version in docker-compose.yml is unsupported" error

**Cause**: Your Docker Compose version doesn't support version 3.8

**Solution**:
All compose files have been updated to use version 3.3 for maximum compatibility. If you still get errors:

```bash
# Check Docker Compose version
docker-compose --version

# For very old versions, try without version specification
# Edit compose file and remove the version line entirely

# Update Docker Compose (Ubuntu/Debian)
sudo apt remove docker-compose
sudo apt install docker-compose-plugin

# Use newer syntax if available
docker compose -f docker-compose.cpu-compatible.yml up --build
```

**Fixed versions**: All compose files now use `version: '3.3'` and compatible resource limit syntax.

### Memory Issues

**Symptom**: Container killed (OOMKilled)

**Solution**:
```bash
# Increase memory limits in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 2G  # Increase from 1G
```

### SSL/TLS Issues (Production)

**Symptom**: HTTPS not working with Nginx

**Solution**:
```bash
# Check SSL certificates
ls -la ./ssl/

# Regenerate certificates
sudo certbot renew --nginx

# Check Nginx configuration
docker-compose exec nginx nginx -t
```

## Debugging Commands

### Container Inspection
```bash
# Enter running container
docker exec -it restaurant-tracker-app bash

# Check environment variables
docker exec restaurant-tracker-app env

# Check Python packages
docker exec restaurant-tracker-app pip list
```

### Log Analysis
```bash
# Real-time logs
docker-compose logs -f

# Specific service logs
docker-compose logs restaurant-tracker

# Last 100 lines
docker-compose logs --tail=100
```

### Performance Monitoring
```bash
# Container resource usage
docker stats

# Detailed container info
docker inspect restaurant-tracker-app
```

## Prevention Tips

1. **Regular maintenance**:
   ```bash
   # Clean up unused images
   docker system prune -a
   
   # Update containers
   docker-compose pull
   docker-compose up -d
   ```

2. **Monitoring**:
   - Set up log rotation
   - Monitor disk space
   - Check container health regularly

3. **Backup strategy**:
   ```bash
   # Backup data volumes
   tar -czf backup-$(date +%Y%m%d).tar.gz data/ exports/
   ```

## Getting Help

If issues persist:

1. **Collect information**:
   ```bash
   # System info
   uname -a
   docker --version
   docker-compose --version
   
   # CPU capabilities
   lscpu | grep -i flags
   
   # Container logs
   docker-compose logs > debug.log
   ```

2. **Check resource usage**:
   ```bash
   df -h      # Disk space
   free -h    # Memory
   top        # CPU usage
   ```

3. **Verify file structure**:
   ```bash
   ls -la     # Check file permissions
   pwd        # Verify working directory
   ```