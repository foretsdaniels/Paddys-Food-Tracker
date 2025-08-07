# Restaurant Ingredient Tracker

A Streamlit-based web application that helps restaurants analyze their ingredient usage, waste, and costs. The application processes multiple CSV data sources to calculate key metrics including shrinkage, cost breakdowns, and provides comprehensive reporting capabilities with PDF and Excel export functionality.

## Features

- **Multi-CSV Data Processing**: Upload and process ingredient information, stock received, usage, and waste data
- **Automated Calculations**: 
  - Expected use (used + wasted)
  - Shrinkage (stocked - expected use)
  - Cost breakdowns (used cost, waste cost, shrinkage cost)
  - Total cost analysis
- **Interactive Dashboard**: Real-time data visualization with summary metrics
- **Export Capabilities**: Generate formatted PDF reports and Excel spreadsheets
- **Data Validation**: Ensures CSV files have the required column structure

## Getting Started

### Prerequisites

- Python 3.11+
- Required packages (automatically installed):
  - streamlit
  - pandas
  - fpdf2
  - xlsxwriter
  - openpyxl

### Installation

1. Clone this repository
2. Install dependencies using the package manager
3. Run the application:
   ```bash
   streamlit run app.py --server.port 5000
   ```

### Usage

1. **Prepare CSV Files**: Create four CSV files with the following formats:

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

2. **Upload Files**: Use the file uploaders in the web interface to upload all four CSV files

3. **Generate Report**: Click "Run Report" to process your data

4. **View Results**: Review the calculated metrics including:
   - Total used cost
   - Total waste cost
   - Total shrinkage cost
   - Grand total cost

5. **Export Reports**: Download results as PDF or Excel files

## Sample Data

The repository includes sample CSV files for testing:
- `sample_ingredient_info.csv`
- `sample_input_stock.csv`
- `sample_usage.csv`
- `sample_waste.csv`

## Calculations

The application performs the following calculations:

- **Expected Use** = Used Quantity + Wasted Quantity
- **Shrinkage** = Stocked Quantity - Expected Use
- **Used Cost** = Used Quantity × Unit Cost
- **Waste Cost** = Wasted Quantity × Unit Cost
- **Shrinkage Cost** = Shrinkage × Unit Cost
- **Total Cost** = Used Cost + Waste Cost + Shrinkage Cost

## Architecture

- **Frontend**: Streamlit web framework
- **Data Processing**: Pandas for CSV handling and calculations
- **PDF Generation**: FPDF2 library
- **Excel Export**: XlsxWriter library
- **Layout**: Wide layout configuration for optimal data visualization

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please create an issue in the GitHub repository.