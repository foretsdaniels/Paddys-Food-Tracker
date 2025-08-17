# Restaurant Ingredient Tracker

> **Multi-Platform Restaurant Inventory Management System**
> 
> A comprehensive web application for tracking ingredient usage, waste, and costs with dual Streamlit and Flask implementations for maximum hosting compatibility.

## 📖 Documentation Index

- **[Main Documentation](#restaurant-ingredient-tracker)** - This file (overview and quick start)
- **[Flask Migration Guide](Flask%20Migration/README.md)** - Complete Flask implementation for universal hosting
- **[Deployment Documentation](DEPLOYMENT.md)** - Production deployment across all platforms
- **[Docker Deployment Guide](Docker%20Deployment/README.md)** - Containerized deployment options
- **[Flask Deployment Guide](Flask%20Migration/DEPLOYMENT.md)** - Flask-specific deployment instructions
- **[System Service Guide](Flask%20Migration/SYSTEMD_SERVICE.md)** - Linux systemd service configuration
- **[Troubleshooting Guide](Docker%20Deployment/TROUBLESHOOTING.md)** - Common issues and solutions
- **[Project Architecture](replit.md)** - Technical specifications and recent changes

## 🏗️ Architecture Overview

This project provides **two complete implementations** of the same restaurant ingredient tracking system:

### 1. **Streamlit Edition** (Development & Testing)
- **Location**: Root directory (`app.py`, `sample_*.csv`)
- **Purpose**: Rapid development, prototyping, and Replit hosting
- **Strengths**: Fast development, built-in widgets, automatic UI generation
- **Best For**: Development, testing, Replit deployment

### 2. **Flask Edition** (Production & Universal Hosting)
- **Location**: [`Flask Migration/`](Flask%20Migration/) directory
- **Purpose**: Production deployment on any hosting platform
- **Strengths**: Universal compatibility, better performance, standard web protocols
- **Best For**: Production, shared hosting, VPS, cloud platforms

> **💡 Both implementations provide identical functionality** - choose based on your hosting requirements.

## 🚀 Quick Start

### Option A: Streamlit (Development)
```bash
# Install dependencies
pip install streamlit pandas fpdf2 xlsxwriter

# Run application
streamlit run app.py
```
Access at `http://localhost:8501`

### Option B: Flask (Production)
```bash
# Setup Flask environment
cd "Flask Migration"
chmod +x setup.sh start.sh
./setup.sh && ./start.sh
```
Access at `http://localhost:5000`

### Demo Accounts
- **admin** / **admin123** - Administrator access
- **manager** / **manager456** - Manager access  
- **staff** / **staff789** - Staff access

## 🎯 Key Features

### Core Functionality
- **Multi-CSV Processing**: Upload ingredient info, stock, usage, and waste data
- **Advanced Analytics**: Real-time cost analysis with filtering and sorting
- **Professional Reports**: PDF and Excel exports with charts and insights
- **Alert System**: Automated notifications for high shrinkage and waste
- **Visual Indicators**: Color-coded tables highlighting problematic items

### Analytics Dashboard
- **Shrinkage Analysis**: Identify potential theft and inventory losses
- **Waste Tracking**: Monitor efficiency and identify process improvements
- **Cost Breakdown**: Detailed analysis of usage, waste, and shrinkage costs
- **Performance Insights**: Smart recommendations based on data patterns

### Report Generation
- **PDF Reports**: Professional summaries with charts and key metrics
- **Excel Workbooks**: Multi-sheet analysis with interactive charts
- **Custom Exports**: Filtered data exports for specific analysis needs

## 📊 Data Requirements

### Required CSV Files

| File | Purpose | Required Columns | Example |
|------|---------|------------------|---------|
| **Ingredient Info** | Unit costs | `Ingredient`, `Unit Cost` | [sample_ingredient_info.csv](sample_ingredient_info.csv) |
| **Input Stock** | Received quantities | `Ingredient`, `Received Qty` | [sample_input_stock.csv](sample_input_stock.csv) |
| **Usage Data** | Used quantities | `Ingredient`, `Used Qty` | [sample_usage.csv](sample_usage.csv) |
| **Waste Data** | Wasted quantities | `Ingredient`, `Wasted Qty` | [sample_waste.csv](sample_waste.csv) |

### Key Metrics Calculated

| Metric | Formula | Purpose |
|--------|---------|---------|
| **Shrinkage** | Received - (Used + Wasted) | Identify theft/loss |
| **Shrinkage Cost** | Shrinkage × Unit Cost | Dollar impact of losses |
| **Waste %** | (Wasted ÷ Received) × 100 | Efficiency measurement |
| **Total Cost** | Used Cost + Waste Cost + Shrinkage Cost | Complete cost analysis |

## 🔧 Deployment Options

### Platform Compatibility

| Platform | Streamlit | Flask | Recommendation |
|----------|-----------|-------|----------------|
| **Replit** | ✅ Native | ✅ Compatible | Use Streamlit |
| **Heroku** | ⚠️ Limited | ✅ Excellent | Use Flask |
| **DigitalOcean** | ⚠️ Complex | ✅ Simple | Use Flask |
| **AWS/GCP** | ⚠️ Complex | ✅ Native | Use Flask |
| **Shared Hosting** | ❌ No support | ✅ Full support | Use Flask |
| **VPS/Dedicated** | ⚠️ Limited | ✅ Full control | Use Flask |

### Quick Deployment Guides

#### Production Flask Deployment
```bash
cd "Flask Migration"
sudo ./deploy.sh  # Automated production setup
```
📖 **See**: [Flask Deployment Guide](Flask%20Migration/DEPLOYMENT.md)

#### Docker Deployment
```bash
cd "Docker Deployment"
./run-cpu-compatible-legacy.sh  # For older systems
```
📖 **See**: [Docker Deployment Guide](Docker%20Deployment/README.md)

#### Development Setup
```bash
streamlit run app.py  # Streamlit development
# OR
cd "Flask Migration" && ./start.sh  # Flask development
```

## 🛠️ Management Tools

### Flask Service Management
```bash
cd "Flask Migration"
./service-manager.sh status   # Check service status
./service-manager.sh health   # Run health checks
./service-manager.sh logs     # View application logs
```
📖 **See**: [System Service Guide](Flask%20Migration/SYSTEMD_SERVICE.md)

### Docker Management
```bash
cd "Docker Deployment"
docker-compose logs -f       # View container logs
docker-compose restart      # Restart services
```

## 🔒 Security Features

### Authentication
- **Replit Auth**: Automatic authentication in Replit environment
- **Demo Accounts**: Secure fallback authentication for standalone deployment
- **Session Management**: Secure session handling with automatic cleanup

### Production Security
- **Service Hardening**: Non-privileged users, restricted file access
- **Network Security**: Firewall configuration, SSL/HTTPS support
- **Data Protection**: Secure file uploads, input validation

## 📈 Performance Comparison

| Feature | Streamlit | Flask |
|---------|-----------|-------|
| **Startup Time** | 30+ seconds | < 5 seconds |
| **Memory Usage** | 200+ MB | < 100 MB |
| **Concurrent Users** | Limited | Excellent |
| **Hosting Options** | Limited | Universal |
| **Mobile Support** | Basic | Excellent |
| **Customization** | Limited | Complete |

## 📋 Sample Data

Test the application with included sample data:
- Load via "Sample Data" button in either interface
- Demonstrates all features with realistic restaurant data
- Includes items with various shrinkage and waste patterns

## 🔍 Troubleshooting

### Common Issues
1. **Port conflicts**: Use different ports or stop conflicting services
2. **File permissions**: Ensure proper read/write access to upload directories
3. **CSV format**: Verify column headers match requirements exactly
4. **Browser compatibility**: Use modern browsers for best experience

### Getting Help
- **Flask Issues**: See [Flask Deployment Guide](Flask%20Migration/DEPLOYMENT.md)
- **Docker Issues**: See [Docker Troubleshooting](Docker%20Deployment/TROUBLESHOOTING.md)
- **System Service**: See [Systemd Service Guide](Flask%20Migration/SYSTEMD_SERVICE.md)
- **General Issues**: Check [Project Architecture](replit.md) for recent changes

## 🚀 Next Steps

1. **Choose Your Implementation**:
   - Development/Testing → Use Streamlit edition
   - Production/Hosting → Use Flask edition

2. **Deploy Your Choice**:
   - Follow platform-specific guides in linked documentation
   - Use provided automation scripts for quick setup

3. **Upload Your Data**:
   - Prepare CSV files according to requirements
   - Test with sample data first

4. **Analyze Results**:
   - Focus on high shrinkage items for theft prevention
   - Monitor waste percentages for efficiency improvements
   - Generate regular reports for management review

---

> **📚 Complete Documentation**: All guides are cross-linked and provide step-by-step instructions for your specific deployment scenario. Start with the [Flask Migration Guide](Flask%20Migration/README.md) for production deployments.