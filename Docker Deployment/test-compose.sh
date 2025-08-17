#!/bin/bash

# Test script to validate Docker Compose configurations
echo "🧪 Testing Docker Compose Configurations"
echo "========================================"

# Test simplified configuration
echo "Testing docker-compose.simple.yml..."
if docker-compose -f docker-compose.simple.yml config > /dev/null 2>&1; then
    echo "✅ docker-compose.simple.yml - Valid"
else
    echo "❌ docker-compose.simple.yml - Invalid"
    docker-compose -f docker-compose.simple.yml config
fi

echo ""

# Test CPU-compatible configuration  
echo "Testing docker-compose.cpu-compatible.yml..."
if docker-compose -f docker-compose.cpu-compatible.yml config > /dev/null 2>&1; then
    echo "✅ docker-compose.cpu-compatible.yml - Valid"
else
    echo "❌ docker-compose.cpu-compatible.yml - Invalid"
    docker-compose -f docker-compose.cpu-compatible.yml config
fi

echo ""

# Test main configuration
echo "Testing docker-compose.yml..."
if docker-compose -f docker-compose.yml config > /dev/null 2>&1; then
    echo "✅ docker-compose.yml - Valid"
else
    echo "❌ docker-compose.yml - Invalid"
    docker-compose -f docker-compose.yml config
fi

echo ""
echo "🎉 Configuration validation complete!"