# Restaurant Ingredient Tracker - System Service Documentation

This document explains how to run the Restaurant Ingredient Tracker as a Linux system service using systemd.

## Quick Start

### 1. Install as Service
```bash
cd "Flask Migration"
sudo ./deploy.sh
```

### 2. Manage Service
```bash
# Start service
sudo systemctl start restaurant-tracker

# Stop service  
sudo systemctl stop restaurant-tracker

# Restart service
sudo systemctl restart restaurant-tracker

# Enable auto-start on boot
sudo systemctl enable restaurant-tracker

# Check status
sudo systemctl status restaurant-tracker

# View logs
sudo journalctl -u restaurant-tracker -f
```

### 3. Use Service Manager Script
```bash
# Make executable
chmod +x service-manager.sh

# Show status
./service-manager.sh status

# Start service
sudo ./service-manager.sh start

# Follow logs
./service-manager.sh follow

# Health check
./service-manager.sh health
```

## Service Configuration

### Service File Location
- `/etc/systemd/system/restaurant-tracker.service`

### Service User
- User: `restaurant-tracker`
- Group: `restaurant-tracker`
- Home Directory: `/opt/restaurant-tracker`

### Application Directory
- Installation Path: `/opt/restaurant-tracker`
- Logs: `/opt/restaurant-tracker/logs/`
- Uploads: `/opt/restaurant-tracker/uploads/`
- Exports: `/opt/restaurant-tracker/exports/`

## Service Management Commands

### Basic Commands
```bash
# Start the service
sudo systemctl start restaurant-tracker

# Stop the service
sudo systemctl stop restaurant-tracker

# Restart the service
sudo systemctl restart restaurant-tracker

# Reload configuration (without stopping)
sudo systemctl reload restaurant-tracker

# Check if service is running
sudo systemctl is-active restaurant-tracker

# Check if service is enabled for auto-start
sudo systemctl is-enabled restaurant-tracker
```

### Auto-Start Configuration
```bash
# Enable auto-start on boot
sudo systemctl enable restaurant-tracker

# Disable auto-start
sudo systemctl disable restaurant-tracker

# Check auto-start status
sudo systemctl is-enabled restaurant-tracker
```

### Service Status and Information
```bash
# Detailed status
sudo systemctl status restaurant-tracker

# Show service properties
sudo systemctl show restaurant-tracker

# List all properties
sudo systemctl show restaurant-tracker --all
```

## Log Management

### View Logs
```bash
# View recent logs
sudo journalctl -u restaurant-tracker

# View last 50 lines
sudo journalctl -u restaurant-tracker -n 50

# Follow logs in real-time
sudo journalctl -u restaurant-tracker -f

# View logs from today
sudo journalctl -u restaurant-tracker --since today

# View logs from specific time
sudo journalctl -u restaurant-tracker --since "2024-01-01 12:00:00"
```

### Application Logs
```bash
# Error logs
sudo tail -f /opt/restaurant-tracker/logs/error.log

# Access logs
sudo tail -f /opt/restaurant-tracker/logs/access.log

# All logs
sudo tail -f /opt/restaurant-tracker/logs/*.log
```

### Log Rotation
Logs are automatically rotated using logrotate configuration:
- `/etc/logrotate.d/restaurant-tracker`
- Daily rotation
- Keep 30 days of logs
- Compress old logs

## Service Configuration Details

### Environment Variables
The service loads environment variables from:
- `/opt/restaurant-tracker/.env`

Key variables:
```bash
FLASK_ENV=production
SECRET_KEY=your-secret-key
PORT=5000
DEBUG=False
```

### Resource Limits
```bash
# View current limits
sudo systemctl show restaurant-tracker | grep -i limit

# CPU usage
sudo systemctl show restaurant-tracker | grep CPUUsage

# Memory usage
sudo systemctl show restaurant-tracker | grep MemoryCurrent
```

### Security Settings
The service runs with enhanced security:
- `NoNewPrivileges=true` - Cannot gain new privileges
- `PrivateTmp=true` - Private /tmp directory
- `ProtectSystem=strict` - Read-only system directories
- `ProtectHome=true` - No access to user home directories

## Troubleshooting

### Service Won't Start
```bash
# Check service status
sudo systemctl status restaurant-tracker

# Check recent logs
sudo journalctl -u restaurant-tracker -n 20

# Check service file syntax
sudo systemd-analyze verify /etc/systemd/system/restaurant-tracker.service

# Reload systemd configuration
sudo systemctl daemon-reload
```

### Common Issues

#### 1. Permission Errors
```bash
# Fix ownership
sudo chown -R restaurant-tracker:restaurant-tracker /opt/restaurant-tracker

# Fix permissions
sudo chmod +x /opt/restaurant-tracker/start.sh
```

#### 2. Port Already in Use
```bash
# Find process using port 5000
sudo lsof -i :5000

# Kill process
sudo kill -9 <PID>
```

#### 3. Python Virtual Environment Issues
```bash
# Recreate virtual environment
sudo -u restaurant-tracker python3 -m venv /opt/restaurant-tracker/venv
sudo -u restaurant-tracker /opt/restaurant-tracker/venv/bin/pip install -r /opt/restaurant-tracker/requirements.txt
```

#### 4. Memory Issues
```bash
# Check memory usage
free -h

# Check service memory usage
sudo systemctl show restaurant-tracker | grep MemoryCurrent

# Reduce worker count in service file
sudo nano /etc/systemd/system/restaurant-tracker.service
# Change --workers 2 to --workers 1
sudo systemctl daemon-reload
sudo systemctl restart restaurant-tracker
```

### Health Checks

#### Manual Health Check
```bash
# Check if service is responding
curl http://localhost:5000/health

# Full health check with service manager
./service-manager.sh health
```

#### Monitoring Script
Create a monitoring script for continuous health checks:

```bash
#!/bin/bash
# /opt/restaurant-tracker/monitor.sh

while true; do
    if ! curl -sf http://localhost:5000/health > /dev/null; then
        echo "$(date): Health check failed, restarting service"
        systemctl restart restaurant-tracker
        sleep 30
    fi
    sleep 60
done
```

Add to crontab for automatic monitoring:
```bash
# Add to root crontab
sudo crontab -e

# Add line:
@reboot /opt/restaurant-tracker/monitor.sh &
```

## Service Manager Script

The included `service-manager.sh` script provides convenient service management:

### Commands
```bash
# Service control
./service-manager.sh start      # Start service
./service-manager.sh stop       # Stop service  
./service-manager.sh restart    # Restart service
./service-manager.sh status     # Show detailed status

# Configuration
./service-manager.sh enable     # Enable auto-start
./service-manager.sh disable    # Disable auto-start

# Monitoring
./service-manager.sh logs       # Show recent logs
./service-manager.sh follow     # Follow logs real-time
./service-manager.sh health     # Comprehensive health check

# Maintenance
./service-manager.sh update     # Update application
```

### Features
- Color-coded output for easy reading
- Comprehensive status information
- Health checking with multiple tests
- Log viewing and following
- Update functionality with automatic backup
- Memory and disk usage monitoring

## Performance Tuning

### Gunicorn Workers
Adjust worker count based on CPU cores:
```bash
# Edit service file
sudo nano /etc/systemd/system/restaurant-tracker.service

# Change --workers count
# Formula: (2 x CPU cores) + 1
# For 2 cores: --workers 5
# For 4 cores: --workers 9

sudo systemctl daemon-reload
sudo systemctl restart restaurant-tracker
```

### Memory Optimization
```bash
# Monitor memory usage
watch -n 5 'sudo systemctl show restaurant-tracker | grep MemoryCurrent'

# Set memory limits in service file
sudo nano /etc/systemd/system/restaurant-tracker.service

# Add under [Service]:
MemoryLimit=512M
MemoryAccounting=yes
```

### CPU Limits
```bash
# Set CPU limits
sudo systemctl set-property restaurant-tracker CPUQuota=50%

# Make permanent by editing service file
sudo nano /etc/systemd/system/restaurant-tracker.service

# Add under [Service]:
CPUQuota=50%
```

## Backup and Recovery

### Service Configuration Backup
```bash
# Backup service file
sudo cp /etc/systemd/system/restaurant-tracker.service /opt/restaurant-tracker/backups/

# Backup nginx configuration
sudo cp /etc/nginx/sites-available/restaurant-tracker /opt/restaurant-tracker/backups/
```

### Application Data Backup
```bash
# Create backup script
#!/bin/bash
DATE=$(date +%Y%m%d-%H%M%S)
tar -czf /backups/restaurant-tracker-$DATE.tar.gz \
    /opt/restaurant-tracker/uploads \
    /opt/restaurant-tracker/exports \
    /opt/restaurant-tracker/logs \
    /opt/restaurant-tracker/.env

# Keep only last 30 days
find /backups -name "restaurant-tracker-*.tar.gz" -mtime +30 -delete
```

### Recovery Procedure
```bash
# Stop service
sudo systemctl stop restaurant-tracker

# Restore from backup
sudo tar -xzf /backups/restaurant-tracker-YYYYMMDD-HHMMSS.tar.gz -C /

# Fix permissions
sudo chown -R restaurant-tracker:restaurant-tracker /opt/restaurant-tracker

# Start service
sudo systemctl start restaurant-tracker
```

## Security Considerations

### Service Security
- Runs as non-privileged user
- Limited filesystem access
- No new privileges allowed
- Private temporary directory

### Network Security
```bash
# Configure firewall
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable

# Block direct access to application port
sudo ufw deny 5000
```

### File Permissions
```bash
# Secure configuration files
sudo chmod 600 /opt/restaurant-tracker/.env
sudo chmod 644 /etc/systemd/system/restaurant-tracker.service

# Secure application directory
sudo chmod 750 /opt/restaurant-tracker
sudo chmod 755 /opt/restaurant-tracker/uploads
sudo chmod 755 /opt/restaurant-tracker/exports
```

This documentation provides comprehensive guidance for running the Restaurant Ingredient Tracker as a production system service with proper monitoring, security, and maintenance procedures.