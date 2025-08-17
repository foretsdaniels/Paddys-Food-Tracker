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

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
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
docker-compose -f docker-compose.cpu-compatible.yml down --remove-orphans

echo "Building image with CPU-compatible packages..."
docker-compose -f docker-compose.cpu-compatible.yml build --no-cache

echo "🚀 Starting Restaurant Ingredient Tracker (CPU Compatible)..."
docker-compose -f docker-compose.cpu-compatible.yml up -d

# Wait for the service to be healthy
echo "⏳ Waiting for application to start (this may take 2-3 minutes)..."
sleep 30

# Check health status
for i in {1..24}; do
    if docker-compose -f docker-compose.cpu-compatible.yml ps | grep -q "restaurant-tracker-cpu-compatible.*Up.*healthy"; then
        echo "✅ Application started successfully!"
        break
    elif [ $i -eq 24 ]; then
        echo "⚠️  Application is taking longer than expected to start."
        echo "📋 Checking logs..."
        docker-compose -f docker-compose.cpu-compatible.yml logs --tail=50
        break
    else
        echo "   Waiting... ($i/24)"
        sleep 10
    fi
done

# Final status check
if docker-compose -f docker-compose.cpu-compatible.yml ps | grep -q "restaurant-tracker-cpu-compatible.*Up"; then
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
    echo "   docker-compose -f docker-compose.cpu-compatible.yml logs -f     # View logs"
    echo "   docker-compose -f docker-compose.cpu-compatible.yml down        # Stop application"
    echo "   docker-compose -f docker-compose.cpu-compatible.yml restart     # Restart application"
    echo ""
    echo "💡 This build uses packages compiled from source for CPU compatibility."
else
    echo "❌ Application failed to start. Check logs:"
    docker-compose -f docker-compose.cpu-compatible.yml logs
    exit 1
fi