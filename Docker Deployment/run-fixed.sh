#!/bin/bash

# ============================================================================
# Restaurant Ingredient Tracker - Fixed Docker Deployment Script
# ============================================================================
# This script resolves the "Illegal instruction (core dumped)" error

set -e

echo "🐳 Restaurant Ingredient Tracker - Fixed Docker Deployment"
echo "========================================================"

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

# Build and start the simplified configuration
echo "🚀 Starting Restaurant Ingredient Tracker (Fixed Version)..."
docker-compose -f docker-compose.simple.yml down --remove-orphans
docker-compose -f docker-compose.simple.yml build --no-cache
docker-compose -f docker-compose.simple.yml up -d

# Wait for the service to be healthy
echo "⏳ Waiting for application to start..."
sleep 10

# Check if the service is running
if docker-compose -f docker-compose.simple.yml ps | grep -q "restaurant-tracker-app.*Up"; then
    echo "✅ Application started successfully!"
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
    echo "   docker-compose -f docker-compose.simple.yml logs -f     # View logs"
    echo "   docker-compose -f docker-compose.simple.yml down        # Stop application"
    echo "   docker-compose -f docker-compose.simple.yml restart     # Restart application"
else
    echo "❌ Application failed to start. Check logs:"
    docker-compose -f docker-compose.simple.yml logs
    exit 1
fi