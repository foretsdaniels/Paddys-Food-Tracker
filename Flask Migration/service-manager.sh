#!/bin/bash

# ============================================================================
# Restaurant Ingredient Tracker - Service Manager
# ============================================================================
# This script manages the Restaurant Ingredient Tracker service

SERVICE_NAME="restaurant-tracker"
APP_DIR="/opt/restaurant-tracker"
LOG_DIR="$APP_DIR/logs"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

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

print_header() {
    echo -e "${BLUE}🍽️ Restaurant Ingredient Tracker - Service Manager${NC}"
    echo "=================================================="
}

# Function to check if service exists
check_service_exists() {
    if systemctl list-unit-files | grep -q "$SERVICE_NAME.service"; then
        return 0
    else
        return 1
    fi
}

# Function to get service status
get_service_status() {
    if check_service_exists; then
        systemctl is-active --quiet $SERVICE_NAME && echo "running" || echo "stopped"
    else
        echo "not-installed"
    fi
}

# Function to display service information
show_info() {
    print_header
    echo ""
    
    if check_service_exists; then
        STATUS=$(get_service_status)
        print_info "Service Status: $STATUS"
        
        if [ "$STATUS" = "running" ]; then
            print_status "Service is running"
            
            # Show process information
            PID=$(systemctl show --property MainPID --value $SERVICE_NAME)
            if [ "$PID" != "0" ]; then
                print_info "Process ID: $PID"
                
                # Show memory usage
                if command -v ps &> /dev/null; then
                    MEMORY=$(ps -o pid,rss,cmd --no-headers -p $PID 2>/dev/null | awk '{print $2}')
                    if [ -n "$MEMORY" ]; then
                        MEMORY_MB=$((MEMORY / 1024))
                        print_info "Memory Usage: ${MEMORY_MB}MB"
                    fi
                fi
            fi
            
            # Test application response
            if command -v curl &> /dev/null; then
                if curl -sf http://localhost:5000/health > /dev/null 2>&1; then
                    print_status "Application is responding"
                else
                    print_warning "Application is not responding"
                fi
            fi
        else
            print_warning "Service is not running"
        fi
        
        # Show service details
        echo ""
        print_info "Service Details:"
        systemctl show $SERVICE_NAME --no-pager | grep -E "(LoadState|ActiveState|SubState|ExecStart|WorkingDirectory)" | while IFS= read -r line; do
            echo "  $line"
        done
        
    else
        print_error "Service is not installed"
        echo "Run 'sudo ./deploy.sh' to install the service"
    fi
    
    echo ""
}

# Function to start service
start_service() {
    print_info "Starting $SERVICE_NAME service..."
    
    if ! check_service_exists; then
        print_error "Service is not installed. Run 'sudo ./deploy.sh' first."
        exit 1
    fi
    
    if [ "$(get_service_status)" = "running" ]; then
        print_warning "Service is already running"
        return 0
    fi
    
    systemctl start $SERVICE_NAME
    
    if [ $? -eq 0 ]; then
        print_status "Service started successfully"
        
        # Wait a moment and check if it's actually running
        sleep 3
        if [ "$(get_service_status)" = "running" ]; then
            print_status "Service is running and healthy"
        else
            print_error "Service failed to start properly"
            show_logs 10
        fi
    else
        print_error "Failed to start service"
        show_logs 20
    fi
}

# Function to stop service
stop_service() {
    print_info "Stopping $SERVICE_NAME service..."
    
    if ! check_service_exists; then
        print_error "Service is not installed"
        exit 1
    fi
    
    if [ "$(get_service_status)" = "stopped" ]; then
        print_warning "Service is already stopped"
        return 0
    fi
    
    systemctl stop $SERVICE_NAME
    
    if [ $? -eq 0 ]; then
        print_status "Service stopped successfully"
    else
        print_error "Failed to stop service"
    fi
}

# Function to restart service
restart_service() {
    print_info "Restarting $SERVICE_NAME service..."
    
    if ! check_service_exists; then
        print_error "Service is not installed"
        exit 1
    fi
    
    systemctl restart $SERVICE_NAME
    
    if [ $? -eq 0 ]; then
        print_status "Service restarted successfully"
        
        # Wait and verify
        sleep 3
        if [ "$(get_service_status)" = "running" ]; then
            print_status "Service is running after restart"
        else
            print_error "Service failed to start after restart"
            show_logs 10
        fi
    else
        print_error "Failed to restart service"
        show_logs 20
    fi
}

# Function to enable/disable auto-start
enable_service() {
    print_info "Enabling auto-start for $SERVICE_NAME..."
    systemctl enable $SERVICE_NAME
    if [ $? -eq 0 ]; then
        print_status "Auto-start enabled"
    else
        print_error "Failed to enable auto-start"
    fi
}

disable_service() {
    print_info "Disabling auto-start for $SERVICE_NAME..."
    systemctl disable $SERVICE_NAME
    if [ $? -eq 0 ]; then
        print_status "Auto-start disabled"
    else
        print_error "Failed to disable auto-start"
    fi
}

# Function to show logs
show_logs() {
    local lines=${1:-50}
    print_info "Showing last $lines lines of service logs:"
    echo ""
    
    if check_service_exists; then
        # Show systemd logs
        echo "=== Systemd Logs ==="
        journalctl -u $SERVICE_NAME --no-pager -n $lines
        
        # Show application logs if they exist
        if [ -f "$LOG_DIR/error.log" ]; then
            echo ""
            echo "=== Application Error Logs ==="
            tail -n $lines "$LOG_DIR/error.log"
        fi
        
        if [ -f "$LOG_DIR/access.log" ]; then
            echo ""
            echo "=== Application Access Logs ==="
            tail -n $lines "$LOG_DIR/access.log"
        fi
    else
        print_error "Service is not installed"
    fi
}

# Function to follow logs in real-time
follow_logs() {
    print_info "Following logs in real-time (Press Ctrl+C to stop):"
    echo ""
    
    if check_service_exists; then
        journalctl -u $SERVICE_NAME -f
    else
        print_error "Service is not installed"
        exit 1
    fi
}

# Function to check application health
health_check() {
    print_info "Performing health check..."
    
    # Check service status
    local status=$(get_service_status)
    if [ "$status" != "running" ]; then
        print_error "Service is not running"
        return 1
    fi
    
    # Check if port is listening
    if command -v ss &> /dev/null; then
        if ss -tln | grep -q ":5000 "; then
            print_status "Port 5000 is listening"
        else
            print_error "Port 5000 is not listening"
            return 1
        fi
    fi
    
    # Check HTTP response
    if command -v curl &> /dev/null; then
        local response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:5000/ 2>/dev/null)
        if [ "$response" = "200" ]; then
            print_status "Application is responding (HTTP 200)"
        else
            print_error "Application returned HTTP $response"
            return 1
        fi
        
        # Check health endpoint
        if curl -sf http://localhost:5000/health > /dev/null 2>&1; then
            print_status "Health endpoint is responding"
        else
            print_warning "Health endpoint is not responding"
        fi
    fi
    
    # Check disk space
    local disk_usage=$(df -h $APP_DIR | awk 'NR==2 {print $5}' | sed 's/%//')
    if [ "$disk_usage" -gt 90 ]; then
        print_error "Disk usage is at ${disk_usage}% - critically high"
        return 1
    elif [ "$disk_usage" -gt 80 ]; then
        print_warning "Disk usage is at ${disk_usage}% - getting high"
    else
        print_status "Disk usage is at ${disk_usage}% - normal"
    fi
    
    print_status "Health check completed successfully"
}

# Function to update the application
update_app() {
    print_info "Updating application..."
    
    if [ ! -d "$APP_DIR" ]; then
        print_error "Application directory not found: $APP_DIR"
        exit 1
    fi
    
    # Stop service
    print_info "Stopping service for update..."
    systemctl stop $SERVICE_NAME
    
    # Backup current version
    local backup_dir="/opt/restaurant-tracker-backup-$(date +%Y%m%d-%H%M%S)"
    print_info "Creating backup: $backup_dir"
    cp -r "$APP_DIR" "$backup_dir"
    
    # Copy new files (assuming they're in current directory)
    if [ -f "app.py" ]; then
        print_info "Copying new application files..."
        cp -r . "$APP_DIR/"
        chown -R restaurant-tracker:restaurant-tracker "$APP_DIR"
        
        # Update dependencies
        print_info "Updating Python dependencies..."
        sudo -u restaurant-tracker "$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt"
        
        # Restart service
        print_info "Starting service..."
        systemctl start $SERVICE_NAME
        
        # Verify update
        sleep 5
        if health_check; then
            print_status "Update completed successfully"
            print_info "Backup available at: $backup_dir"
        else
            print_error "Update failed - service not healthy"
            print_info "Consider rolling back from: $backup_dir"
        fi
    else
        print_error "No application files found in current directory"
        print_info "Starting service again..."
        systemctl start $SERVICE_NAME
    fi
}

# Function to show usage
show_usage() {
    echo "Usage: $0 {start|stop|restart|status|enable|disable|logs|follow|health|update|help}"
    echo ""
    echo "Commands:"
    echo "  start    - Start the service"
    echo "  stop     - Stop the service"
    echo "  restart  - Restart the service"
    echo "  status   - Show service status and information"
    echo "  enable   - Enable auto-start on boot"
    echo "  disable  - Disable auto-start on boot"
    echo "  logs     - Show recent service logs"
    echo "  follow   - Follow logs in real-time"
    echo "  health   - Perform comprehensive health check"
    echo "  update   - Update application (requires new files in current directory)"
    echo "  help     - Show this help message"
    echo ""
    echo "Examples:"
    echo "  sudo $0 start"
    echo "  sudo $0 status"
    echo "  sudo $0 logs"
    echo "  $0 follow  # No sudo needed for reading logs"
}

# Check if running as root for commands that need it
needs_root() {
    case $1 in
        start|stop|restart|enable|disable|update)
            return 0
            ;;
        *)
            return 1
            ;;
    esac
}

# Main script logic
if [ $# -eq 0 ]; then
    show_usage
    exit 1
fi

case $1 in
    start)
        if needs_root $1 && [ "$EUID" -ne 0 ]; then
            print_error "This command requires root privileges. Use: sudo $0 $1"
            exit 1
        fi
        start_service
        ;;
    stop)
        if needs_root $1 && [ "$EUID" -ne 0 ]; then
            print_error "This command requires root privileges. Use: sudo $0 $1"
            exit 1
        fi
        stop_service
        ;;
    restart)
        if needs_root $1 && [ "$EUID" -ne 0 ]; then
            print_error "This command requires root privileges. Use: sudo $0 $1"
            exit 1
        fi
        restart_service
        ;;
    status|info)
        show_info
        ;;
    enable)
        if needs_root $1 && [ "$EUID" -ne 0 ]; then
            print_error "This command requires root privileges. Use: sudo $0 $1"
            exit 1
        fi
        enable_service
        ;;
    disable)
        if needs_root $1 && [ "$EUID" -ne 0 ]; then
            print_error "This command requires root privileges. Use: sudo $0 $1"
            exit 1
        fi
        disable_service
        ;;
    logs)
        show_logs ${2:-50}
        ;;
    follow)
        follow_logs
        ;;
    health|check)
        health_check
        ;;
    update)
        if needs_root $1 && [ "$EUID" -ne 0 ]; then
            print_error "This command requires root privileges. Use: sudo $0 $1"
            exit 1
        fi
        update_app
        ;;
    help|--help|-h)
        show_usage
        ;;
    *)
        print_error "Unknown command: $1"
        echo ""
        show_usage
        exit 1
        ;;
esac