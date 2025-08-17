#!/bin/bash

# ============================================================================
# Restaurant Ingredient Tracker - Flask Edition Setup Script
# ============================================================================
# This script sets up the development environment for the Flask application

set -e

echo "🍽️ Restaurant Ingredient Tracker - Flask Edition Setup"
echo "======================================================="
echo "Setting up development environment..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.7 or later."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
print_info "Python version: $PYTHON_VERSION"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    print_error "pip3 is not installed. Please install pip3."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_info "Creating virtual environment..."
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_warning "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip

# Install requirements
print_info "Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
    print_status "Dependencies installed successfully"
else
    print_error "requirements.txt not found"
    exit 1
fi

# Create necessary directories
print_info "Creating application directories..."
mkdir -p uploads exports logs static/css static/js
print_status "Directories created"

# Copy sample data if not exists
if [ ! -f "sample_ingredient_info.csv" ]; then
    if [ -f "../sample_ingredient_info.csv" ]; then
        print_info "Copying sample data files..."
        cp ../sample_*.csv .
        print_status "Sample data copied"
    else
        print_warning "Sample data files not found - you'll need to upload your own CSV files"
    fi
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_info "Creating environment configuration..."
    cp .env.example .env
    
    # Generate a random secret key
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_hex(32))")
    
    # Update .env with generated secret key
    if command -v sed &> /dev/null; then
        sed -i "s/your-secret-key-change-this-in-production/$SECRET_KEY/" .env
        print_status "Environment file created with secure secret key"
    else
        print_warning "Environment file created - please update SECRET_KEY in .env"
    fi
else
    print_warning "Environment file already exists"
fi

# Set executable permissions
print_info "Setting script permissions..."
chmod +x start.sh
chmod +x deploy.sh
if [ -f "run.py" ]; then
    chmod +x run.py
fi
print_status "Permissions set"

# Check if all required files exist
print_info "Verifying installation..."
REQUIRED_FILES=("app.py" "requirements.txt" "templates/base.html" "utils/data_processor.py")
MISSING_FILES=()

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        MISSING_FILES+=("$file")
    fi
done

if [ ${#MISSING_FILES[@]} -eq 0 ]; then
    print_status "All required files present"
else
    print_error "Missing required files: ${MISSING_FILES[*]}"
    exit 1
fi

# Test import of main modules
print_info "Testing Python imports..."
python3 -c "
import sys
try:
    import flask
    import pandas
    import xlsxwriter
    from fpdf import FPDF
    print('✅ All required Python modules imported successfully')
except ImportError as e:
    print(f'❌ Import error: {e}')
    sys.exit(1)
"

# Display setup summary
echo ""
echo "🎉 Setup completed successfully!"
echo "================================"
echo ""
print_info "Next steps:"
echo "  1. Run './start.sh' to start the development server"
echo "  2. Open http://localhost:5000 in your browser"
echo "  3. Login with demo accounts:"
echo "     - admin / admin123"
echo "     - manager / manager456"
echo "     - staff / staff789"
echo ""
print_info "Development commands:"
echo "  - Start server: ./start.sh"
echo "  - Run with Python: python3 run.py"
echo "  - Activate venv: source venv/bin/activate"
echo ""
print_info "Production deployment:"
echo "  - Deploy as service: sudo ./deploy.sh"
echo "  - Docker deployment: docker-compose up --build"
echo ""
print_warning "Note: Remember to update the SECRET_KEY in .env for production!"

# Deactivate virtual environment
deactivate 2>/dev/null || true

echo ""
print_status "Setup script completed successfully! 🚀"