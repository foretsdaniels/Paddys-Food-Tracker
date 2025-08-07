# 🍽️ Restaurant Ingredient Tracker

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

### Local Development
1. Install dependencies: `pip install streamlit pandas fpdf2 xlsxwriter`
2. Run: `streamlit run app.py --server.port 5000`
3. Use demo accounts for authentication

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

## 🤝 Support

This application uses Replit's built-in authentication system and is optimized for the Replit platform. For authentication issues, ensure you're logged into Replit and refresh the application if needed.

---

**Built with ❤️ for restaurant efficiency and cost optimization**