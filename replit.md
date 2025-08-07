# Overview

The Restaurant Ingredient Tracker is a Streamlit-based web application designed to help restaurants analyze their ingredient usage, waste, and costs. The application processes multiple CSV data sources (ingredient information, stock received, usage, and waste) to calculate key metrics including shrinkage, cost breakdowns, and provide comprehensive reporting capabilities with PDF and Excel export functionality.

## Recent Changes
- Completely reworked and enhanced the application architecture
- Fixed all LSP diagnostics and code quality issues 
- Added comprehensive data validation (duplicates, negatives, empty data)
- Enhanced PDF reports with better formatting and pagination support
- Improved Excel exports with percentages, insights, and timestamps
- Added advanced filtering and sorting options for results analysis
- Integrated sample data functionality for easy testing and demonstration
- Added smart insights and warnings for high waste/shrinkage percentages
- Updated README.md with comprehensive documentation of all new features
- Improved error handling and user experience throughout the application
- Corrected shrinkage calculation to show dollar value of missing/stolen inventory
- Updated filtering to focus on shrinkage > $10 as most important metric for tracking
- Modified default sorting to prioritize shrinkage cost analysis

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: Streamlit web framework for rapid development of data applications
- **Layout**: Wide layout configuration for better data visualization
- **User Interface**: File upload widgets for CSV inputs, data tables for results display, and export buttons for report generation

## Data Processing Architecture
- **Data Input**: Multiple CSV file upload system supporting:
  - Ingredient information with unit costs
  - Input stock with received quantities
  - Usage data with consumed amounts
  - Waste data with wasted quantities
- **Data Validation**: CSV structure validation ensuring required columns are present
- **Data Transformation**: Pandas-based data processing with indexed merging and metric calculations
- **Calculations Engine**: Automated computation of:
  - Expected use (used + wasted)
  - Shrinkage (stocked - expected use)
  - Cost breakdowns (used cost, waste cost, shrinkage cost)
  - Total cost analysis

## Export System
- **PDF Generation**: FPDF library for creating formatted PDF reports
- **Excel Export**: XlsxWriter for generating structured Excel spreadsheets
- **Report Formatting**: Structured output with summary totals and detailed breakdowns

## Data Flow
1. CSV files uploaded through Streamlit interface
2. Data validation ensures structural integrity
3. Pandas processing merges and calculates metrics
4. Results displayed in interactive tables
5. Export functionality generates downloadable reports

# External Dependencies

## Core Libraries
- **Streamlit**: Web application framework for the user interface
- **Pandas**: Data manipulation and analysis library for CSV processing
- **FPDF**: PDF generation library for report creation
- **XlsxWriter**: Excel file generation for spreadsheet exports

## Data Format Dependencies
- **CSV Structure**: Requires specific column naming conventions:
  - Ingredient info: 'Ingredient', 'Unit Cost'
  - Input stock: 'Ingredient', 'Received Qty'
  - Usage data: 'Ingredient', 'Used Qty'
  - Waste data: 'Ingredient', 'Wasted Qty'

## Runtime Environment
- **Python Environment**: Requires Python with scientific computing stack
- **File I/O**: Local file system access for CSV uploads and report downloads
- **Memory Management**: In-memory data processing for multiple DataFrame operations