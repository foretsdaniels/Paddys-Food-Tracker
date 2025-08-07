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
- Added visual highlighting system for easy identification of problematic items
- Implemented alert system for high shrinkage items and missing stock notifications
- Added color-coded rows (red for high shrinkage, orange for missing stock)
- Enhanced UX with warning and info notice boxes for immediate issue identification
- Implemented Replit Auth integration with automatic authentication in Replit environment
- Added smart environment detection (Replit vs local/demo mode)
- Maintained demo accounts for non-Replit environments with fallback authentication
- Included seamless user experience with zero-config authentication on Replit platform
- Added comprehensive navigation system with multi-page layout (Dashboard, Analytics, Reports, Settings)
- Created enhanced login landing page with feature overview and improved UX
- Implemented sidebar navigation with logout button and user information
- Added quick stats dashboard with key metrics overview
- Separated analytics into dedicated page with advanced filtering and sorting
- Created dedicated reports page with export functionality and summary statistics
- Added settings page with help information and data management options
- Enhanced logout functionality with complete session state cleanup
- Improved responsive design with expanded sidebar configuration
- Implemented enterprise-grade Replit Auth with ReplitAuth class
- Added automatic authentication detection and session management
- Created comprehensive authentication flow with troubleshooting features
- Enhanced user experience with seamless Replit platform integration
- Added authentication status display and user session information
- Integrated Firebase, Google Cloud Identity Platform security infrastructure
- Added fraud prevention and global scalability features through enterprise auth system

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: Streamlit web framework for rapid development of data applications
- **Layout**: Wide layout configuration for better data visualization
- **Authentication**: Enterprise-grade Replit Auth with ReplitAuth class integration
- **User Interface**: File upload widgets for CSV inputs, data tables for results display, and export buttons for report generation
- **Navigation**: Multi-page sidebar navigation system (Dashboard, Analytics, Reports, Settings)
- **Session Management**: Secure user session handling with automatic authentication

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