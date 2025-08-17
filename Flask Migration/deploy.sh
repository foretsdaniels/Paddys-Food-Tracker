#!/bin/bash

# ============================================================================
# Restaurant Ingredient Tracker - Flask Edition Production Deployment Script
# ============================================================================
# This script deploys the application as a system service on Linux

set -e

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "❌ This script must be run as root (use sudo)"
    echo "Usage: sudo ./deploy.sh"
    exit 1
fi

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🍽️ Restaurant Ingredient Tracker - Production Deployment${NC}"
echo "========================================================="
echo ""

# Configuration variables
APP_NAME="restaurant-tracker"
APP_USER="restaurant-tracker"
APP_DIR="/opt/restaurant-tracker"
SERVICE_NAME="restaurant-tracker"
NGINX_AVAILABLE="/etc/nginx/sites-available"
NGINX_ENABLED="/etc/nginx/sites-enabled"

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️ $1${NC}"
}

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$NAME
    VER=$VERSION_ID
else
    print_error "Cannot detect OS. This script supports Ubuntu/Debian and CentOS/RHEL."
    exit 1
fi

print_info "Detected OS: $OS $VER"

# Function to install packages on Debian/Ubuntu
install_debian_packages() {
    print_info "Installing packages for Debian/Ubuntu..."
    apt update
    apt install -y python3 python3-pip python3-venv nginx supervisor curl
    print_status "Packages installed"
}

# Function to install packages on CentOS/RHEL
install_rhel_packages() {
    print_info "Installing packages for CentOS/RHEL..."
    yum update -y
    yum install -y python3 python3-pip nginx supervisor curl
    # Enable and start services
    systemctl enable nginx
    systemctl start nginx
    print_status "Packages installed"
}

# Install system packages based on OS
case $OS in
    *"Ubuntu"*|*"Debian"*)
        install_debian_packages
        ;;
    *"CentOS"*|*"Red Hat"*|*"Rocky"*|*"AlmaLinux"*)
        install_rhel_packages
        ;;
    *)
        print_warning "Unsupported OS: $OS. Continuing with manual package installation..."
        ;;
esac

# Create application user
if id "$APP_USER" &>/dev/null; then
    print_warning "User $APP_USER already exists"
else
    print_info "Creating application user: $APP_USER"
    useradd --system --shell /bin/bash --home $APP_DIR --create-home $APP_USER
    print_status "User created"
fi

# Create application directory and copy files
print_info "Setting up application directory: $APP_DIR"
mkdir -p $APP_DIR
cp -r . $APP_DIR/
chown -R $APP_USER:$APP_USER $APP_DIR

# Set up Python virtual environment
print_info "Setting up Python virtual environment..."
sudo -u $APP_USER python3 -m venv $APP_DIR/venv
sudo -u $APP_USER $APP_DIR/venv/bin/pip install --upgrade pip
sudo -u $APP_USER $APP_DIR/venv/bin/pip install -r $APP_DIR/requirements.txt
sudo -u $APP_USER $APP_DIR/venv/bin/pip install gunicorn  # Ensure gunicorn is installed
print_status "Virtual environment configured"

# Create necessary directories
print_info "Creating application directories..."
sudo -u $APP_USER mkdir -p $APP_DIR/uploads $APP_DIR/exports $APP_DIR/logs $APP_DIR/static
chown -R $APP_USER:$APP_USER $APP_DIR
print_status "Directories created"

# Generate production environment file
print_info "Creating production environment configuration..."
cat > $APP_DIR/.env << EOF
FLASK_ENV=production
SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
PORT=5000
DEBUG=False
UPLOAD_FOLDER=$APP_DIR/uploads
EXPORT_FOLDER=$APP_DIR/exports
EOF
chown $APP_USER:$APP_USER $APP_DIR/.env
chmod 600 $APP_DIR/.env
print_status "Environment configuration created"

# Create systemd service file
print_info "Creating systemd service..."
cat > /etc/systemd/system/$SERVICE_NAME.service << EOF
[Unit]
Description=Restaurant Ingredient Tracker Flask Application
After=network.target

[Service]
Type=notify
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
EnvironmentFile=$APP_DIR/.env
ExecStart=$APP_DIR/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 --access-logfile $APP_DIR/logs/access.log --error-logfile $APP_DIR/logs/error.log app:app
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Create Nginx configuration
if command -v nginx &> /dev/null; then
    print_info "Creating Nginx configuration..."
    
    cat > $NGINX_AVAILABLE/$APP_NAME << EOF
server {
    listen 80;
    server_name _;  # Replace with your domain name
    
    client_max_body_size 50M;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
    
    location /static {
        alias $APP_DIR/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
}
EOF
    
    # Enable site
    if [ -d "$NGINX_ENABLED" ]; then
        ln -sf $NGINX_AVAILABLE/$APP_NAME $NGINX_ENABLED/
        print_status "Nginx configuration created and enabled"
    else
        print_warning "Nginx sites-enabled directory not found. Please manually enable the site."
    fi
else
    print_warning "Nginx not found. Skipping Nginx configuration."
fi

# Create log rotation configuration
print_info "Setting up log rotation..."
cat > /etc/logrotate.d/$APP_NAME << EOF
$APP_DIR/logs/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 $APP_USER $APP_USER
    postrotate
        systemctl reload $SERVICE_NAME
    endscript
}
EOF
print_status "Log rotation configured"

# Set up firewall (if ufw is available)
if command -v ufw &> /dev/null; then
    print_info "Configuring firewall..."
    ufw --force reset
    ufw default deny incoming
    ufw default allow outgoing
    ufw allow ssh
    ufw allow 80
    ufw allow 443
    echo "y" | ufw enable
    print_status "Firewall configured"
else
    print_warning "UFW not found. Please configure firewall manually."
fi

# Reload systemd and start services
print_info "Starting services..."
systemctl daemon-reload
systemctl enable $SERVICE_NAME
systemctl start $SERVICE_NAME

# Test Nginx configuration and restart if available
if command -v nginx &> /dev/null; then
    nginx -t
    if [ $? -eq 0 ]; then
        systemctl enable nginx
        systemctl restart nginx
        print_status "Nginx started"
    else
        print_error "Nginx configuration test failed"
    fi
fi

# Wait a moment for services to start
sleep 5

# Check service status
print_info "Checking service status..."
if systemctl is-active --quiet $SERVICE_NAME; then
    print_status "Application service is running"
else
    print_error "Application service failed to start"
    print_info "Checking logs..."
    journalctl -u $SERVICE_NAME --no-pager -n 20
fi

# Test application
print_info "Testing application..."
if curl -sf http://localhost:5000/ > /dev/null; then
    print_status "Application is responding"
else
    print_warning "Application is not responding. Check logs for details."
fi

# Display final information
echo ""
echo -e "${GREEN}🎉 Deployment completed!${NC}"
echo "========================"
echo ""
print_info "Service Management Commands:"
echo "  sudo systemctl start $SERVICE_NAME     # Start service"
echo "  sudo systemctl stop $SERVICE_NAME      # Stop service"
echo "  sudo systemctl restart $SERVICE_NAME   # Restart service"
echo "  sudo systemctl status $SERVICE_NAME    # Check status"
echo "  sudo systemctl enable $SERVICE_NAME    # Enable auto-start"
echo "  sudo systemctl disable $SERVICE_NAME   # Disable auto-start"
echo ""
print_info "View Logs:"
echo "  sudo journalctl -u $SERVICE_NAME -f   # Follow service logs"
echo "  sudo tail -f $APP_DIR/logs/error.log  # Follow application logs"
echo ""
print_info "Application URLs:"
echo "  http://localhost:5000                  # Direct access"
if command -v nginx &> /dev/null; then
    echo "  http://your-server-ip                 # Through Nginx"
fi
echo ""
print_info "Demo Accounts:"
echo "  admin / admin123"
echo "  manager / manager456"
echo "  staff / staff789"
echo ""
print_warning "Next Steps:"
echo "  1. Replace 'server_name _;' in Nginx config with your domain"
echo "  2. Set up SSL/HTTPS with Let's Encrypt: sudo certbot --nginx"
echo "  3. Update firewall rules if needed"
echo "  4. Test the application thoroughly"
echo ""
print_status "Production deployment completed successfully! 🚀"