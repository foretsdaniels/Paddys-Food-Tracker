# Restaurant Ingredient Tracker

A comprehensive Streamlit-based web application that helps restaurants analyze their ingredient usage, waste, and costs. The application processes multiple CSV data sources to calculate key metrics including shrinkage, cost breakdowns, and provides comprehensive reporting capabilities with advanced PDF and Excel export functionality.

## Features

### 📊 Data Processing & Analysis
- **Multi-CSV Data Processing**: Upload and process ingredient information, stock received, usage, and waste data
- **Advanced Data Validation**: 
  - Checks for missing required columns
  - Validates numeric data types
  - Detects duplicate ingredients
  - Identifies negative values with warnings
  - Validates empty datasets
- **Smart Data Reconciliation**: Automatically handles ingredients present in some files but missing in others
- **Automated Calculations**: 
  - Expected use (used + wasted)
  - Shrinkage (stocked - expected use)
  - Cost breakdowns (used cost, waste cost, shrinkage cost)
  - Total cost analysis with percentages

### 🎯 Interactive Dashboard
- **Real-time Metrics**: Summary cards showing total costs with percentage insights
- **Smart Insights**: Automatic warnings for high waste or shrinkage percentages (>5%)
- **Alert System**: Immediate notifications for items with shrinkage >$10 and missing stock
- **Visual Highlighting**: Color-coded rows to identify high shrinkage (red) and missing stock (orange)
- **Advanced Filtering**: Focus on items with shrinkage >$10 for critical issue tracking
- **Flexible Sorting**: Sort results by ingredient name, total cost, waste cost, or shrinkage cost
- **Data Table**: Interactive results display with formatted currency, numbers, and visual indicators

### 📤 Export Capabilities
- **Enhanced PDF Reports**: 
  - Professional formatting with timestamps
  - Multi-page support with automatic pagination
  - Detailed summary totals section
  - Optimized column widths for readability
- **Advanced Excel Reports**:
  - Formatted spreadsheets with color-coded headers
  - Automatic number and currency formatting
  - Summary totals with percentage calculations
  - Generation timestamps for tracking

### 🎯 User Experience
- **Secure Authentication**: Username/password login system with demo accounts
- **Session Management**: Secure user sessions with logout functionality
- **Sample Data Integration**: Try the app instantly with pre-loaded restaurant data
- **Comprehensive Help**: Built-in instructions with CSV format examples
- **Error Handling**: Clear, actionable error messages with specific guidance
- **Progress Feedback**: Real-time status updates during processing

## Getting Started

### Prerequisites

- Python 3.11+
- Required packages (automatically installed):
  - streamlit
  - pandas
  - fpdf
  - xlsxwriter
  - openpyxl

### Installation

1. Clone this repository
2. Install dependencies using the package manager
3. Run the application:
   ```bash
   streamlit run app.py --server.port 5000
   ```

### Quick Start Options

#### Option 1: Try with Sample Data
1. **Login**: Use demo credentials (admin/admin123, manager/manager456, or staff/staff789)
2. Expand "🎯 Try with Sample Data" section
3. Click "📋 Load Sample Data" to see the app in action
4. Explore the features with pre-loaded restaurant data

#### Option 2: Use Your Own Data

1. **Login**: Use your assigned credentials or demo accounts
2. **Prepare CSV Files**: Create four CSV files with the following formats:

   **Ingredient Info CSV** (`ingredient_info.csv`):
   ```csv
   Ingredient,Unit Cost
   Tomatoes,2.50
   Onions,1.25
   ```

   **Stock CSV** (`input_stock.csv`):
   ```csv
   Ingredient,Received Qty
   Tomatoes,150.0
   Onions,80.0
   ```

   **Usage CSV** (`usage.csv`):
   ```csv
   Ingredient,Used Qty
   Tomatoes,120.0
   Onions,65.0
   ```

   **Waste CSV** (`waste.csv`):
   ```csv
   Ingredient,Wasted Qty
   Tomatoes,8.0
   Onions,3.0
   ```

3. **Upload Files**: Use the file uploaders in the web interface to upload all four CSV files

4. **Generate Report**: Click "Run Report" to process your data

5. **View Results**: Review the calculated metrics including:
   - Total used cost
   - Total waste cost
   - Total shrinkage cost
   - Grand total cost

6. **Analyze Results**: 
   - Review summary metrics with percentage insights
   - Use filtering options to focus on problem areas
   - Sort data by different criteria for analysis
   - Pay attention to automated insights and warnings

7. **Export Reports**: Download professional PDF or Excel reports with detailed formatting

## Authentication

The application includes a secure authentication system:

### Demo Accounts
- **Admin**: Username `admin`, Password `admin123`
- **Manager**: Username `manager`, Password `manager456`
- **Staff**: Username `staff`, Password `staff789`

### Security Features
- Password hashing using SHA256
- Session-based authentication
- Automatic logout functionality
- Session data cleanup on logout

## Sample Data

The repository includes comprehensive sample CSV files for testing:
- `sample_ingredient_info.csv` - 15 common restaurant ingredients with realistic unit costs
- `sample_input_stock.csv` - Sample received quantities 
- `sample_usage.csv` - Realistic usage patterns
- `sample_waste.csv` - Waste data showing common loss patterns

These files demonstrate typical restaurant scenarios including items with high waste, shrinkage issues, and normal usage patterns.

## Calculations & Insights

### Core Calculations
- **Expected Use** = Used Quantity + Wasted Quantity
- **Used Cost** = Used Quantity × Unit Cost
- **Waste Cost** = Wasted Quantity × Unit Cost
- **Expected Use Cost** = Expected Use × Unit Cost
- **Stocked Cost** = Stocked Quantity × Unit Cost
- **Shrinkage Cost** = Stocked Cost - Expected Use Cost (dollar value of missing/stolen inventory)
- **Total Cost** = Used Cost + Waste Cost + Shrinkage Cost

### Advanced Analytics
- **Waste Percentage** = (Total Waste Cost ÷ Grand Total Cost) × 100
- **Shrinkage Percentage** = (Total Shrinkage Cost ÷ Grand Total Cost) × 100
- **Automated Insights** = Warnings when waste or shrinkage exceed 5% of total costs

### Data Quality Features
- Duplicate ingredient detection
- Missing data identification and handling
- Negative value detection with warnings
- Cross-file ingredient reconciliation

## Architecture

### Application Stack
- **Frontend**: Streamlit web framework with wide layout for optimal visualization
- **Data Processing**: Pandas for advanced CSV handling and calculations
- **PDF Generation**: FPDF2 library with custom formatting and pagination
- **Excel Export**: XlsxWriter library with professional formatting
- **Session Management**: Streamlit session state for data persistence
- **Error Handling**: Comprehensive validation and user feedback system

### Key Components
- **Data Validation Engine**: Multi-layer CSV structure and content validation
- **Calculation Engine**: Advanced metric computation with percentage analysis  
- **Export System**: Professional report generation with timestamps and insights
- **UI Components**: Interactive filtering, sorting, and sample data integration
- **Session Management**: Persistent data storage and state management

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Advanced Features

### Data Validation
- **Comprehensive Checks**: Validates column structure, data types, and content quality
- **Smart Warnings**: Identifies potential data quality issues without blocking processing
- **Error Recovery**: Graceful handling of missing or inconsistent data across files

### Export Options
- **PDF Reports**: Multi-page professional reports with automatic pagination
- **Excel Spreadsheets**: Formatted workbooks with conditional formatting and summary analytics
- **Timestamp Tracking**: All exports include generation timestamps for audit trails

### User Interface
- **Responsive Design**: Optimized for different screen sizes with wide layout
- **Interactive Controls**: Real-time filtering and sorting without page reloads  
- **Progress Indicators**: Clear feedback during data processing operations
- **Sample Data Mode**: Instant demonstration capability for new users

## Troubleshooting

### Common Issues
- **CSV Format Errors**: Ensure column names exactly match requirements (case-sensitive)
- **Numeric Data Issues**: Check for non-numeric characters in cost/quantity columns
- **Duplicate Ingredients**: Remove or consolidate duplicate ingredient entries
- **Missing Data**: Use 0 values for ingredients with no usage, waste, or stock data

### Performance Tips
- **File Sizes**: Application handles hundreds of ingredients efficiently
- **Memory Usage**: Large datasets are processed in optimized chunks
- **Export Speed**: PDF generation may take longer for very large datasets

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please create an issue in the GitHub repository. Include sample data files when reporting data processing issues.