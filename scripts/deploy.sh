#!/bin/bash

# ============================================================================
# Restaurant Ingredient Tracker - Deployment Script
# ============================================================================
#
# This script provides easy commands for deploying and managing the
# Restaurant Ingredient Tracker application using Docker.
#
# Usage:
#   ./scripts/deploy.sh [command] [options]
#
# Commands:
#   setup     - Initial setup (copy .env, create directories)
#   dev       - Start development environment
#   prod      - Start production environment
#   stop      - Stop all services
#   logs      - View application logs
#   status    - Check service status
#   clean     - Clean up containers and volumes
#   backup    - Create backup of data
#   help      - Show this help message

set -e  # Exit on any error

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$PROJECT_DIR/.env"
ENV_EXAMPLE="$PROJECT_DIR/.env.example"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if Docker is installed and running
check_docker() {
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi

    if ! docker info &> /dev/null; then
        log_error "Docker is not running. Please start Docker first."
        exit 1
    fi

    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
}

# Setup function - initial project setup
setup() {
    log_info "Setting up Restaurant Ingredient Tracker..."

    # Check Docker
    check_docker

    # Copy environment file if it doesn't exist
    if [ ! -f "$ENV_FILE" ]; then
        log_info "Creating .env file from template..."
        cp "$ENV_EXAMPLE" "$ENV_FILE"
        log_success ".env file created. Please edit it with your configuration."
        log_warning "Remember to change the default passwords and secret keys!"
    else
        log_info ".env file already exists."
    fi

    # Create necessary directories
    log_info "Creating necessary directories..."
    mkdir -p "$PROJECT_DIR"/{data,logs,exports,config,ssl,backups}
    chmod 755 "$PROJECT_DIR"/{data,logs,exports}

    # Generate secure keys if needed
    if grep -q "your-secret-key-here" "$ENV_FILE"; then
        log_info "Generating secure session key..."
        SESSION_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))" 2>/dev/null || openssl rand -hex 32)
        sed -i "s/SESSION_SECRET_KEY=your-secret-key-here.*/SESSION_SECRET_KEY=$SESSION_KEY/" "$ENV_FILE"
    fi

    if grep -q "REDIS_PASSWORD=defaultpassword" "$ENV_FILE"; then
        log_info "Generating secure Redis password..."
        REDIS_PASS=$(python3 -c "import secrets; print(secrets.token_urlsafe(16))" 2>/dev/null || openssl rand -base64 16)
        sed -i "s/REDIS_PASSWORD=defaultpassword/REDIS_PASSWORD=$REDIS_PASS/" "$ENV_FILE"
    fi

    log_success "Setup completed successfully!"
    log_info "Next steps:"
    log_info "1. Edit .env file: nano .env"
    log_info "2. Start development: ./scripts/deploy.sh dev"
    log_info "3. Start production: ./scripts/deploy.sh prod"
}

# Start development environment
start_dev() {
    log_info "Starting development environment..."
    check_docker

    cd "$PROJECT_DIR"
    
    # Use development override
    if docker compose version &> /dev/null; then
        docker compose -f docker-compose.yml -f docker-compose.override.yml up -d
    else
        docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d
    fi

    log_success "Development environment started!"
    log_info "Application available at: http://localhost:8501"
    log_info "View logs: ./scripts/deploy.sh logs"
}

# Start production environment
start_prod() {
    log_info "Starting production environment..."
    check_docker

    cd "$PROJECT_DIR"

    # Check if .env exists
    if [ ! -f "$ENV_FILE" ]; then
        log_error ".env file not found. Run './scripts/deploy.sh setup' first."
        exit 1
    fi

    # Start production services
    if docker compose version &> /dev/null; then
        docker compose up -d
    else
        docker-compose up -d
    fi

    log_success "Production environment started!"
    log_info "Application available at: http://localhost:$(grep HOST_PORT .env | cut -d'=' -f2 || echo 8501)"
    log_info "View logs: ./scripts/deploy.sh logs"
}

# Stop all services
stop_services() {
    log_info "Stopping all services..."
    cd "$PROJECT_DIR"

    if docker compose version &> /dev/null; then
        docker compose down
    else
        docker-compose down
    fi

    log_success "All services stopped."
}

# View logs
view_logs() {
    cd "$PROJECT_DIR"
    
    if [ "$1" = "follow" ] || [ "$1" = "-f" ]; then
        log_info "Following logs (Press Ctrl+C to exit)..."
        if docker compose version &> /dev/null; then
            docker compose logs -f restaurant-tracker
        else
            docker-compose logs -f restaurant-tracker
        fi
    else
        log_info "Showing recent logs..."
        if docker compose version &> /dev/null; then
            docker compose logs --tail=50 restaurant-tracker
        else
            docker-compose logs --tail=50 restaurant-tracker
        fi
    fi
}

# Check status
check_status() {
    log_info "Checking service status..."
    cd "$PROJECT_DIR"

    if docker compose version &> /dev/null; then
        docker compose ps
    else
        docker-compose ps
    fi

    # Check health if containers are running
    if docker ps --format "table {{.Names}}" | grep -q "restaurant-tracker-app"; then
        echo ""
        log_info "Health checks:"
        
        # Check main application
        if curl -f -s http://localhost:8501/_stcore/health > /dev/null 2>&1; then
            log_success "✓ Application is healthy"
        else
            log_warning "✗ Application health check failed"
        fi

        # Check Redis if running
        if docker ps --format "table {{.Names}}" | grep -q "restaurant-tracker-redis"; then
            if docker exec restaurant-tracker-redis redis-cli ping > /dev/null 2>&1; then
                log_success "✓ Redis is healthy"
            else
                log_warning "✗ Redis health check failed"
            fi
        fi
    fi
}

# Clean up containers and volumes
cleanup() {
    log_warning "This will remove all containers, networks, and volumes."
    read -p "Are you sure? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Cleaning up..."
        cd "$PROJECT_DIR"

        if docker compose version &> /dev/null; then
            docker compose down -v --remove-orphans
        else
            docker-compose down -v --remove-orphans
        fi

        # Clean up Docker system
        docker system prune -f

        log_success "Cleanup completed."
    else
        log_info "Cleanup cancelled."
    fi
}

# Create backup
create_backup() {
    log_info "Creating backup..."
    
    BACKUP_DIR="$PROJECT_DIR/backups/$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"

    # Backup data directory
    if [ -d "$PROJECT_DIR/data" ]; then
        log_info "Backing up data directory..."
        tar -czf "$BACKUP_DIR/data.tar.gz" -C "$PROJECT_DIR" data/
    fi

    # Backup logs
    if [ -d "$PROJECT_DIR/logs" ]; then
        log_info "Backing up logs..."
        tar -czf "$BACKUP_DIR/logs.tar.gz" -C "$PROJECT_DIR" logs/
    fi

    # Backup configuration
    log_info "Backing up configuration..."
    tar -czf "$BACKUP_DIR/config.tar.gz" -C "$PROJECT_DIR" .env docker-compose.yml

    # Backup Redis data if running
    if docker ps --format "table {{.Names}}" | grep -q "restaurant-tracker-redis"; then
        log_info "Backing up Redis data..."
        docker exec restaurant-tracker-redis redis-cli BGSAVE
        docker cp restaurant-tracker-redis:/data/dump.rdb "$BACKUP_DIR/"
    fi

    log_success "Backup created at: $BACKUP_DIR"
}

# Show help
show_help() {
    cat << EOF
Restaurant Ingredient Tracker - Deployment Script

Usage: $0 [command] [options]

Commands:
    setup     Initial setup (copy .env, create directories, generate keys)
    dev       Start development environment with hot reload
    prod      Start production environment
    stop      Stop all services
    logs      View application logs (use 'logs -f' to follow)
    status    Check service status and health
    clean     Clean up containers and volumes (destructive!)
    backup    Create backup of data and configuration
    help      Show this help message

Examples:
    $0 setup                    # Initial setup
    $0 dev                      # Start development
    $0 prod                     # Start production
    $0 logs -f                  # Follow logs
    $0 status                   # Check status
    $0 backup                   # Create backup
    $0 stop                     # Stop services

Environment:
    Configuration is stored in .env file
    Edit .env to customize ports, passwords, and other settings

For more information, see DOCKER_DEPLOYMENT.md

EOF
}

# Main script logic
case "${1:-help}" in
    setup)
        setup
        ;;
    dev|development)
        start_dev
        ;;
    prod|production)
        start_prod
        ;;
    stop)
        stop_services
        ;;
    logs)
        view_logs "$2"
        ;;
    status)
        check_status
        ;;
    clean|cleanup)
        cleanup
        ;;
    backup)
        create_backup
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        log_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac