# 🍽️ Paddys Restaurant Food Inventory Tracker

A comprehensive Streamlit-based web application designed to help restaurants analyze ingredient usage, waste, and costs. Track your restaurant's inventory efficiency, reduce waste costs, and optimize ingredient purchasing with powerful analytics and reporting capabilities.

## 🚀 Features

### 🔐 Enterprise Authentication
- **Replit Auth Integration**: Seamless authentication using Replit's enterprise-grade system
- **Firebase & Google Cloud Security**: Powered by enterprise infrastructure
- **Automatic Detection**: Smart environment detection (Replit vs local/demo mode)
- **Demo Mode**: Fallback authentication for testing and development

### 📊 Data Analysis & Processing
- **Multi-CSV Upload**: Support for ingredient info, stock, usage, and waste data
- **Comprehensive Validation**: Duplicate detection, negative value checks, empty data handling
- **Smart Calculations**: Automatic computation of shrinkage, costs, and efficiency metrics
- **Real-time Processing**: Instant report generation with error handling

### 📈 Advanced Analytics
- **Interactive Dashboard**: Quick stats overview with key performance metrics
- **Filtering & Sorting**: Advanced options for data analysis
- **Top Items Analysis**: Identify highest cost and waste items
- **Cost Breakdown**: Detailed analysis of used, waste, and shrinkage costs
- **Visual Highlighting**: Color-coded alerts for high shrinkage items

### 📤 Reporting & Export
- **PDF Reports**: Professional formatted reports with pagination
- **Excel Exports**: Structured spreadsheets with formulas and insights
- **Summary Statistics**: Comprehensive cost analysis and percentages
- **Downloadable Files**: Instant export with timestamps

### 🎯 Smart Insights
- **Shrinkage Alerts**: Automatic warnings for items with high shrinkage (>$10)
- **Missing Stock Notifications**: Alerts for inventory discrepancies
- **Waste Optimization**: Identify opportunities to reduce waste costs
- **Percentage Tracking**: Monitor waste and shrinkage as percentage of total costs

## 🏗️ Architecture

### Frontend
- **Framework**: Streamlit with wide layout configuration
- **Navigation**: Multi-page sidebar system (Dashboard, Analytics, Reports, Settings)
- **Authentication**: Enterprise-grade Replit Auth with session management
- **Responsive Design**: Optimized for various screen sizes

### Data Processing
- **Engine**: Pandas-based data processing and transformation
- **Validation**: Comprehensive CSV structure and data integrity checks
- **Calculations**: Automated metric computation with error handling
- **Memory Management**: Efficient in-memory data operations

### Export System
- **PDF Generation**: FPDF library with custom formatting
- **Excel Export**: XlsxWriter with advanced spreadsheet features
- **Report Templates**: Structured output with professional formatting

## 📋 Data Format Requirements

### Ingredient Information CSV
```
Ingredient,Unit Cost
Tomatoes,2.50
Lettuce,1.75
Chicken Breast,8.99
```

### Stock Received CSV  
```
Ingredient,Received Qty
Tomatoes,100
Lettuce,50
Chicken Breast,25
```

### Usage Data CSV
```
Ingredient,Used Qty
Tomatoes,80
Lettuce,45
Chicken Breast,20
```

### Waste Data CSV
```
Ingredient,Wasted Qty
Tomatoes,5
Lettuce,2
Chicken Breast,1
```

## 🧮 Calculations

The application automatically calculates:

- **Expected Use** = Used Quantity + Wasted Quantity
- **Used Cost** = Used Quantity × Unit Cost
- **Waste Cost** = Wasted Quantity × Unit Cost
- **Shrinkage Cost** = (Stocked Quantity × Unit Cost) - (Expected Use × Unit Cost)
- **Total Cost** = Used Cost + Waste Cost + Shrinkage Cost

## 🎮 Usage

### Getting Started
1. **Authentication**: Log in through Replit Auth (automatic) or demo mode
2. **Data Upload**: Upload your four CSV files or try sample data
3. **Generate Report**: Click "Run Report" to process your data
4. **Analyze Results**: Use the interactive dashboard and analytics pages
5. **Export Reports**: Download PDF or Excel reports as needed

### Navigation
- **🏠 Dashboard**: Main interface for data upload and quick stats
- **📊 Analytics**: Detailed analysis with filtering and sorting options
- **📤 Reports**: Export functionality and summary statistics
- **⚙️ Settings**: User information and help documentation

### Demo Accounts
For testing outside Replit environment:
- **Admin**: `admin` / `admin123`
- **Manager**: `manager` / `manager456`
- **Staff**: `staff` / `staff789`

## 🔧 Technical Details

### Dependencies
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **FPDF2**: PDF report generation
- **XlsxWriter**: Excel export functionality

### Environment Variables
- `REPL_ID`: Replit environment identifier
- `REPL_OWNER`: Repository owner information
- `REPLIT_USER`: Authenticated user information
- `REPLIT_DOMAINS`: Available domains for deployment

### Configuration
- Server runs on port 5000 with headless configuration
- Wide layout for optimal data visualization
- Expanded sidebar for easy navigation

## 🚀 Deployment

### On Replit
1. The app runs automatically with Replit Auth
2. No additional configuration required
3. Automatic authentication for logged-in users

### Local Installation (Ubuntu/Linux)

#### Prerequisites
- Ubuntu 20.04+ or similar Linux distribution
- Python 3.8+ and pip

#### Quick Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv git -y

# Create project directory
mkdir ~/restaurant-tracker && cd ~/restaurant-tracker

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install streamlit pandas fpdf2 xlsxwriter openpyxl

# Download application files (copy app.py and sample CSV files)

# Create Streamlit configuration
mkdir .streamlit
cat > .streamlit/config.toml << EOF
[server]
headless = true
address = "0.0.0.0"
port = 5000

[theme]
primaryColor = "#ff6b6b"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
EOF

# Run application
streamlit run app.py --server.port 5000
```

#### Production Deployment

**Create Systemd Service:**
```bash
sudo nano /etc/systemd/system/restaurant-tracker.service
```

Add service configuration:
```ini
[Unit]
Description=Restaurant Ingredient Tracker
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/restaurant-tracker
Environment=PATH=/home/ubuntu/restaurant-tracker/venv/bin
ExecStart=/home/ubuntu/restaurant-tracker/venv/bin/streamlit run app.py --server.port 5000
Restart=always

[Install]
WantedBy=multi-user.target
```

**Enable and start service:**
```bash
sudo systemctl daemon-reload
sudo systemctl enable restaurant-tracker
sudo systemctl start restaurant-tracker
sudo systemctl status restaurant-tracker
```

**Configure firewall:**
```bash
sudo ufw allow 5000/tcp
sudo ufw enable
```

#### Optional: Nginx Reverse Proxy
```bash
# Install Nginx
sudo apt install nginx -y

# Configure virtual host
sudo nano /etc/nginx/sites-available/restaurant-tracker
```

Add configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/restaurant-tracker /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl restart nginx
```

### Windows Installation

#### Using Command Prompt/PowerShell:
```cmd
# Install Python from python.org if not installed

# Create project directory
mkdir restaurant-tracker
cd restaurant-tracker

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install streamlit pandas fpdf2 xlsxwriter openpyxl

# Create .streamlit directory and config
mkdir .streamlit
echo [server] > .streamlit\config.toml
echo headless = true >> .streamlit\config.toml
echo address = "0.0.0.0" >> .streamlit\config.toml
echo port = 5000 >> .streamlit\config.toml

# Run application
streamlit run app.py --server.port 5000
```

### macOS Installation

```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python

# Create project directory
mkdir ~/restaurant-tracker && cd ~/restaurant-tracker

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install streamlit pandas fpdf2 xlsxwriter openpyxl

# Create Streamlit configuration
mkdir .streamlit
cat > .streamlit/config.toml << EOF
[server]
headless = true
address = "0.0.0.0"
port = 5000
EOF

# Run application
streamlit run app.py --server.port 5000
```

## 📊 Key Metrics

The application tracks and analyzes:
- Total ingredient costs and investments
- Waste percentages and cost impact
- Shrinkage identification and alerts
- High-cost items requiring attention
- Efficiency trends and optimization opportunities

## 🛡️ Security Features

- Enterprise-grade authentication through Replit
- Secure session management
- Environment-based configuration
- Data validation and sanitization
- Error handling and logging

## 🆕 Recent Updates

- Implemented enterprise Replit Auth with ReplitAuth class
- Added comprehensive navigation system with multi-page layout
- Enhanced login page with feature overview
- Created advanced analytics with filtering and sorting
- Added smart insights and automated alerts
- Improved export functionality with better formatting
- Integrated sample data for easy testing
- Enhanced error handling and user experience
- Added visual highlighting for problem identification
- Implemented secure logout with session cleanup

## 🔧 Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Find process using port 5000
sudo lsof -i :5000
# Kill process if needed
sudo kill <PID>
```

**Permission issues:**
```bash
# Fix ownership (Linux)
sudo chown -R $USER:$USER ~/restaurant-tracker
```

**Virtual environment issues:**
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install streamlit pandas fpdf2 xlsxwriter openpyxl
```

**Service not starting (Linux):**
```bash
# Check service logs
sudo journalctl -u restaurant-tracker -f
# Restart service
sudo systemctl restart restaurant-tracker
```

### Authentication Notes
- **Replit Environment**: Automatic authentication via Replit Auth
- **Local Installation**: Uses demo mode with test accounts
- **Demo Accounts**: admin/admin123, manager/manager456, staff/staff789

### Maintenance Commands (Linux Production)
```bash
# Service management
sudo systemctl start restaurant-tracker
sudo systemctl stop restaurant-tracker
sudo systemctl restart restaurant-tracker
sudo systemctl status restaurant-tracker

# View logs
sudo journalctl -u restaurant-tracker -f
```

## 🤝 Support

- **Replit Users**: Authentication is automatic when logged into Replit
- **Local Users**: Use demo accounts for testing and development
- **Issues**: Check troubleshooting section above for common solutions
- **Performance**: Minimum 2GB RAM, 4GB recommended for production

For detailed deployment instructions, see `DEPLOYMENT.md` in the project repository.

---

**Built with ❤️ for restaurant efficiency and cost optimization**