#!/bin/bash

# ============================================================================
# Restaurant Ingredient Tracker - CPU Compatible Deployment Script
# ============================================================================
# For CPUs with only SSE4a support (no SSE4.1/SSE4.2/AVX)
# Fixes "Illegal instruction (core dumped)" errors

set -e

echo "🔧 Restaurant Ingredient Tracker - CPU Compatible Build"
echo "=================================================="
echo "For CPUs with only SSE4a support (older AMD processors)"
echo ""

# Check CPU capabilities
echo "🔍 Checking CPU capabilities..."
if command -v lscpu &> /dev/null; then
    echo "CPU Info:"
    lscpu | grep -E "(Model name|Flags)" || true
    echo ""
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed (try both docker-compose and docker compose)
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   You can install it with: sudo apt install docker-compose-plugin"
    exit 1
fi

# Determine which docker compose command to use
if command -v docker-compose &> /dev/null; then
    DOCKER_COMPOSE="docker-compose"
else
    DOCKER_COMPOSE="docker compose"
fi

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data logs exports

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env
    echo "✅ Created .env file. Edit it to customize your deployment."
fi

echo "🏗️  Building CPU-compatible Docker image..."
echo "This may take 10-15 minutes as packages are compiled from source..."
echo ""

# Build and start the CPU-compatible configuration
echo "Stopping any existing containers..."
$DOCKER_COMPOSE -f docker-compose.cpu-compatible.yml down --remove-orphans 2>/dev/null || true

echo "Building image with CPU-compatible packages..."
if ! $DOCKER_COMPOSE -f docker-compose.cpu-compatible.yml build --no-cache; then
    echo "❌ Failed to build Docker image. Check the error messages above."
    exit 1
fi

echo "🚀 Starting Restaurant Ingredient Tracker (CPU Compatible)..."
if ! $DOCKER_COMPOSE -f docker-compose.cpu-compatible.yml up -d; then
    echo "❌ Failed to start containers. Check the error messages above."
    exit 1
fi

# Wait for the service to be healthy
echo "⏳ Waiting for application to start (this may take 2-3 minutes)..."
sleep 30

# Check health status
echo "Checking container status..."
CONTAINER_HEALTHY=false

for i in {1..24}; do
    # Check if container is running first
    if $DOCKER_COMPOSE -f docker-compose.cpu-compatible.yml ps --services --filter "status=running" | grep -q "restaurant-tracker"; then
        # Check if it's healthy (if health check is enabled)
        if $DOCKER_COMPOSE -f docker-compose.cpu-compatible.yml ps | grep -q "restaurant-tracker-cpu-compatible.*Up.*healthy"; then
            echo "✅ Application started successfully and is healthy!"
            CONTAINER_HEALTHY=true
            break
        elif $DOCKER_COMPOSE -f docker-compose.cpu-compatible.yml ps | grep -q "restaurant-tracker-cpu-compatible.*Up"; then
            # Container is running but health check might not be ready yet
            if [ $i -ge 12 ]; then  # After 2 minutes, consider it good enough if running
                echo "✅ Application is running (health check pending)!"
                CONTAINER_HEALTHY=true
                break
            fi
        fi
    fi
    
    if [ $i -eq 24 ]; then
        echo "⚠️  Application is taking longer than expected to start."
        echo "📋 Checking logs..."
        $DOCKER_COMPOSE -f docker-compose.cpu-compatible.yml logs --tail=50
        break
    else
        echo "   Waiting... ($i/24) - $(date '+%H:%M:%S')"
        sleep 10
    fi
done

# Final status check
if $DOCKER_COMPOSE -f docker-compose.cpu-compatible.yml ps | grep -q "restaurant-tracker-cpu-compatible.*Up" || [ "$CONTAINER_HEALTHY" = true ]; then
    echo ""
    echo "🌐 Access your application at:"
    echo "   http://localhost:8501"
    echo ""
    echo "🔐 Demo accounts:"
    echo "   admin / admin123"
    echo "   manager / manager456" 
    echo "   staff / staff789"
    echo ""
    echo "📋 Useful commands:"
    echo "   $DOCKER_COMPOSE -f docker-compose.cpu-compatible.yml logs -f     # View logs"
    echo "   $DOCKER_COMPOSE -f docker-compose.cpu-compatible.yml down        # Stop application"
    echo "   $DOCKER_COMPOSE -f docker-compose.cpu-compatible.yml restart     # Restart application"
    echo ""
    echo "💡 This build uses packages compiled from source for CPU compatibility."
    echo "🔧 If the app doesn't respond immediately, wait 1-2 more minutes for full startup."
else
    echo "❌ Application failed to start. Showing recent logs:"
    echo "=================================================="
    $DOCKER_COMPOSE -f docker-compose.cpu-compatible.yml logs --tail=100
    echo "=================================================="
    echo ""
    echo "🔧 Troubleshooting tips:"
    echo "1. Check if port 8501 is already in use: sudo lsof -i :8501"
    echo "2. Try restarting Docker: sudo systemctl restart docker"
    echo "3. Check available disk space: df -h"
    echo "4. View full logs: $DOCKER_COMPOSE -f docker-compose.cpu-compatible.yml logs"
    exit 1
fi