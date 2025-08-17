#!/bin/bash

# ============================================================================
# Restaurant Ingredient Tracker - Legacy CPU Compatible Deployment Script
# ============================================================================
# For Docker Compose 1.25.x and CPUs with only SSE4a support

set -e

echo "🔧 Restaurant Ingredient Tracker - Legacy CPU Compatible Build"
echo "=============================================================="
echo "For Docker Compose 1.25.x and CPUs with only SSE4a support"
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

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check Docker Compose version
COMPOSE_VERSION=$(docker-compose --version | grep -oE '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
echo "📋 Using Docker Compose version: $COMPOSE_VERSION"

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p data logs exports

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file..."
    cp .env.example .env 2>/dev/null || echo "# Legacy deployment" > .env
    echo "✅ Created .env file."
fi

echo "🏗️  Building CPU-compatible Docker image (Legacy Mode)..."
echo "This may take 10-15 minutes as packages are compiled from source..."
echo ""

# Use legacy compose file
COMPOSE_FILE="docker-compose.cpu-compatible-legacy.yml"

# Stop any existing containers
echo "Stopping any existing containers..."
docker-compose -f $COMPOSE_FILE down --remove-orphans 2>/dev/null || true

echo "Building image with CPU-compatible packages..."
if ! docker-compose -f $COMPOSE_FILE build --no-cache; then
    echo "❌ Failed to build Docker image. Check the error messages above."
    exit 1
fi

echo "🚀 Starting Restaurant Ingredient Tracker (Legacy CPU Compatible)..."
if ! docker-compose -f $COMPOSE_FILE up -d; then
    echo "❌ Failed to start containers. Check the error messages above."
    exit 1
fi

# Wait for the service to be ready
echo "⏳ Waiting for application to start (this may take 2-3 minutes)..."
sleep 30

# Check container status (simplified for legacy)
echo "Checking container status..."
CONTAINER_RUNNING=false

for i in {1..18}; do
    if docker ps | grep -q "restaurant-tracker-cpu-compatible.*Up"; then
        echo "✅ Application is running!"
        CONTAINER_RUNNING=true
        break
    elif [ $i -eq 18 ]; then
        echo "⚠️  Application is taking longer than expected to start."
        echo "📋 Checking logs..."
        docker-compose -f $COMPOSE_FILE logs --tail=50
        break
    else
        echo "   Waiting... ($i/18) - $(date '+%H:%M:%S')"
        sleep 10
    fi
done

# Final status check
if docker ps | grep -q "restaurant-tracker-cpu-compatible.*Up" || [ "$CONTAINER_RUNNING" = true ]; then
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
    echo "   docker-compose -f $COMPOSE_FILE logs -f     # View logs"
    echo "   docker-compose -f $COMPOSE_FILE down        # Stop application"
    echo "   docker-compose -f $COMPOSE_FILE restart     # Restart application"
    echo ""
    echo "💡 This build uses packages compiled from source for CPU compatibility."
    echo "🔧 Legacy mode for Docker Compose $COMPOSE_VERSION"
else
    echo "❌ Application failed to start. Showing recent logs:"
    echo "=================================================="
    docker-compose -f $COMPOSE_FILE logs --tail=100
    echo "=================================================="
    echo ""
    echo "🔧 Troubleshooting tips:"
    echo "1. Check if port 8501 is already in use: sudo lsof -i :8501"
    echo "2. Try restarting Docker: sudo systemctl restart docker"
    echo "3. Check available disk space: df -h"
    echo "4. View full logs: docker-compose -f $COMPOSE_FILE logs"
    exit 1
fi