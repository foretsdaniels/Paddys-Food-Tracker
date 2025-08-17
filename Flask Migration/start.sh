#!/bin/bash

# ============================================================================
# Restaurant Ingredient Tracker - Flask Edition Start Script
# ============================================================================
# This script starts the Flask development server

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🍽️ Restaurant Ingredient Tracker - Flask Edition${NC}"
echo "=================================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${RED}❌ Virtual environment not found. Please run './setup.sh' first.${NC}"
    exit 1
fi

# Activate virtual environment
echo -e "${BLUE}📦 Activating virtual environment...${NC}"
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️ .env file not found. Using default configuration.${NC}"
    export FLASK_ENV=development
    export SECRET_KEY=dev-secret-key
    export PORT=5000
    export DEBUG=True
else
    echo -e "${GREEN}✅ Loading environment configuration...${NC}"
    set -o allexport
    source .env
    set +o allexport
fi

# Set default values if not set
export FLASK_ENV=${FLASK_ENV:-development}
export PORT=${PORT:-5000}
export DEBUG=${DEBUG:-True}

# Create necessary directories
mkdir -p uploads exports logs

# Check if app.py exists
if [ ! -f "app.py" ]; then
    echo -e "${RED}❌ app.py not found. Please ensure you're in the correct directory.${NC}"
    exit 1
fi

# Display startup information
echo ""
echo -e "${GREEN}🚀 Starting Restaurant Ingredient Tracker...${NC}"
echo "=============================================="
echo -e "${BLUE}Environment:${NC} $FLASK_ENV"
echo -e "${BLUE}Port:${NC} $PORT"
echo -e "${BLUE}Debug:${NC} $DEBUG"
echo -e "${BLUE}URL:${NC} http://localhost:$PORT"
echo ""
echo -e "${YELLOW}👤 Demo Accounts:${NC}"
echo "   admin / admin123     (Administrator)"
echo "   manager / manager456 (Manager)"
echo "   staff / staff789     (Staff)"
echo ""
echo -e "${YELLOW}📁 Features:${NC}"
echo "   • Upload CSV files for ingredient tracking"
echo "   • Real-time analytics and cost analysis"
echo "   • PDF and Excel report generation"
echo "   • Shrinkage and waste monitoring"
echo "   • Sample data available for testing"
echo ""
echo -e "${GREEN}Press Ctrl+C to stop the server${NC}"
echo "=============================================="
echo ""

# Function to handle cleanup on exit
cleanup() {
    echo ""
    echo -e "${YELLOW}🛑 Stopping server...${NC}"
    echo -e "${GREEN}✅ Server stopped successfully!${NC}"
    deactivate 2>/dev/null || true
    exit 0
}

# Set trap to handle Ctrl+C
trap cleanup SIGINT SIGTERM

# Check if port is already in use
if command -v lsof &> /dev/null; then
    if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null; then
        echo -e "${RED}❌ Port $PORT is already in use.${NC}"
        echo "Please stop the other process or change the PORT in .env"
        echo ""
        echo "To find the process using port $PORT:"
        echo "sudo lsof -i :$PORT"
        echo ""
        echo "To kill the process:"
        echo "sudo kill -9 \$(sudo lsof -t -i:$PORT)"
        exit 1
    fi
fi

# Start the application
if [ "$FLASK_ENV" = "production" ]; then
    echo -e "${BLUE}🏭 Starting in production mode with Gunicorn...${NC}"
    # Check if gunicorn is installed
    if ! command -v gunicorn &> /dev/null; then
        echo -e "${RED}❌ Gunicorn not found. Installing...${NC}"
        pip install gunicorn
    fi
    
    # Start with gunicorn for production
    gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 120 --access-logfile - --error-logfile - app:app
else
    echo -e "${BLUE}🔧 Starting in development mode...${NC}"
    # Start with Flask development server
    python3 run.py
fi

# This should never be reached due to the trap, but just in case
cleanup