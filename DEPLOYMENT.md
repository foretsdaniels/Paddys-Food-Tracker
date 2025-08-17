# Ubuntu Deployment Guide

Complete guide for deploying the Restaurant Ingredient Tracker on Ubuntu from scratch.

## Prerequisites

Fresh Ubuntu 20.04+ installation with sudo access.

## Step 1: System Update and Dependencies

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Install Python 3 and pip
sudo apt install python3 python3-pip python3-venv git curl -y

# Verify Python installation
python3 --version
pip3 --version
```

## Step 2: Create Application Directory

```bash
# Create app directory
mkdir ~/restaurant-tracker
cd ~/restaurant-tracker

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
# Install required Python packages
pip install streamlit pandas fpdf2 xlsxwriter openpyxl

# Verify installation
streamlit --version
```

## Step 4: Download Application Files

### Option A: From Repository
```bash
# If you have the code in a repository
git clone <your-repository-url> .
```

### Option B: Manual File Creation
Create the following files in your project directory:

1. **Create app.py** - Copy the complete application code
2. **Create .streamlit/config.toml**:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
primaryColor = "#ff6b6b"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

3. **Create sample data files** (optional):
   - sample_ingredient_info.csv
   - sample_input_stock.csv
   - sample_usage.csv
   - sample_waste.csv

## Step 5: Test Local Deployment

```bash
# Ensure virtual environment is active
source venv/bin/activate

# Run the application
streamlit run app.py --server.port 5000
```

Access at: http://localhost:5000

## Step 6: Production Deployment Options

### Option A: Simple Background Process

```bash
# Run in background with nohup
nohup streamlit run app.py --server.port 5000 > streamlit.log 2>&1 &

# Check if running
ps aux | grep streamlit
```

### Option B: Using Screen Session

```bash
# Install screen
sudo apt install screen -y

# Start screen session
screen -S restaurant-tracker

# Run application in screen
streamlit run app.py --server.port 5000

# Detach: Ctrl+A, then D
# Reattach: screen -r restaurant-tracker
```

### Option C: Systemd Service (Recommended)

```bash
# Create service file
sudo nano /etc/systemd/system/restaurant-tracker.service
```

Add the following content:
```ini
[Unit]
Description=Restaurant Ingredient Tracker
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/restaurant-tracker
Environment=PATH=/home/ubuntu/restaurant-tracker/venv/bin
ExecStart=/home/ubuntu/restaurant-tracker/venv/bin/streamlit run app.py --server.port 5000
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable restaurant-tracker
sudo systemctl start restaurant-tracker

# Check status
sudo systemctl status restaurant-tracker

# View logs
sudo journalctl -u restaurant-tracker -f
```

## Step 7: Firewall Configuration

```bash
# Allow port 5000 through firewall
sudo ufw allow 5000/tcp

# Enable firewall if not already enabled
sudo ufw enable

# Check firewall status
sudo ufw status
```

## Step 8: Reverse Proxy with Nginx (Optional)

For production with custom domain:

```bash
# Install Nginx
sudo apt install nginx -y

# Create nginx configuration
sudo nano /etc/nginx/sites-available/restaurant-tracker
```

Add configuration:
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
}
```

Enable the site:
```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/restaurant-tracker /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Step 9: SSL Certificate (Optional)

```bash
# Install Certbot
sudo apt install snapd -y
sudo snap install core; sudo snap refresh core
sudo snap install --classic certbot

# Create certificate
sudo certbot --nginx -d your-domain.com
```

## Troubleshooting

### Common Issues

1. **Port already in use**:
```bash
# Find process using port 5000
sudo lsof -i :5000
# Kill process if needed
sudo kill <PID>
```

2. **Permission issues**:
```bash
# Fix ownership
sudo chown -R $USER:$USER ~/restaurant-tracker
```

3. **Virtual environment issues**:
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install streamlit pandas fpdf2 xlsxwriter openpyxl
```

4. **Service not starting**:
```bash
# Check service logs
sudo journalctl -u restaurant-tracker -f
# Restart service
sudo systemctl restart restaurant-tracker
```

## Maintenance Commands

```bash
# Start service
sudo systemctl start restaurant-tracker

# Stop service
sudo systemctl stop restaurant-tracker

# Restart service
sudo systemctl restart restaurant-tracker

# Check service status
sudo systemctl status restaurant-tracker

# View real-time logs
sudo journalctl -u restaurant-tracker -f

# Update application (after code changes)
sudo systemctl stop restaurant-tracker
# Update files
sudo systemctl start restaurant-tracker
```

## Security Considerations

1. **Firewall**: Only open necessary ports
2. **User permissions**: Run service as non-root user
3. **Updates**: Keep system and packages updated
4. **SSL**: Use HTTPS for production deployments
5. **Access**: Limit access to known IP ranges if needed

## Environment Variables

For Replit Auth features, the app will automatically fall back to demo mode on Ubuntu since Replit environment variables won't be available.

Demo accounts available:
- admin / admin123
- manager / manager456  
- staff / staff789

## Performance Optimization

1. **Server specs**: 2GB RAM minimum, 4GB recommended
2. **Storage**: 10GB free space minimum
3. **Network**: Stable internet connection for package updates
4. **Monitoring**: Consider setting up monitoring for production use

## Backup Strategy

```bash
# Create backup script
nano ~/backup-tracker.sh
```

Add:
```bash
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf ~/restaurant-tracker-backup-$DATE.tar.gz ~/restaurant-tracker
```

Make executable and run:
```bash
chmod +x ~/backup-tracker.sh
./backup-tracker.sh
```

Your Restaurant Ingredient Tracker should now be fully deployed and accessible on Ubuntu!

## Docker Deployment (Alternative)

For containerized deployment, see the `Docker Deployment/` directory which includes:

### Quick Docker Start
```bash
cd "Docker Deployment"

# For standard systems
./run-fixed.sh

# For CPUs with only SSE4a support (older AMD processors)
./run-cpu-compatible.sh
```

### Docker Configurations Available
- **Standard**: `docker-compose.yml` - Full production setup with Redis and Nginx
- **Simplified**: `docker-compose.simple.yml` - Streamlit only, no dependencies
- **CPU-Compatible**: `docker-compose.cpu-compatible.yml` - For SSE4a-only processors

### CPU Compatibility Notes
If you encounter "Illegal instruction (core dumped)" errors, your CPU likely only supports SSE4a (not SSE4.1/SSE4.2/AVX). Use the CPU-compatible configuration which:
- Compiles NumPy and Pandas from source
- Uses older package versions known to work on SSE4a-only CPUs
- Takes 10-15 minutes to build but guarantees compatibility

### Docker Benefits
- Consistent environment across different systems
- Automated dependency management
- Production-ready with health checks and restart policies
- Easy scaling and deployment options