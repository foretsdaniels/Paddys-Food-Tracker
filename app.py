import streamlit as st
import pandas as pd
import io
from fpdf import FPDF
import xlsxwriter
from typing import Optional, Tuple

# Page configuration
st.set_page_config(
    page_title="Restaurant Ingredient Tracker",
    page_icon="🍽️",
    layout="wide"
)

def validate_csv_structure(df: pd.DataFrame, required_columns: list, file_type: str) -> bool:
    """Validate that the CSV has the required columns and numeric data."""
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"{file_type} is missing required columns: {', '.join(missing_columns)}")
        return False

    # Check that expected numeric columns can be parsed as numbers
    numeric_columns = [col for col in required_columns if col.lower() != 'ingredient']
    for col in numeric_columns:
        converted = pd.to_numeric(df[col], errors='coerce')
        if converted.isna().any():
            st.error(f"{file_type} has non-numeric values in column '{col}'")
            return False

    # Warn about any unexpected extra columns (potential typos)
    extra_columns = [col for col in df.columns if col not in required_columns]
    if extra_columns:
        st.warning(f"{file_type} has unexpected columns: {', '.join(extra_columns)}")

    return True

def process_ingredient_data(ingredient_info: pd.DataFrame, input_stock: pd.DataFrame, 
                          usage: pd.DataFrame, waste: pd.DataFrame) -> pd.DataFrame:
    """Process the ingredient data and calculate metrics."""
    try:
        # Create a copy of ingredient info as the base dataframe
        df = ingredient_info.copy()
        df = df.set_index('Ingredient')
        
        # Merge data from other CSVs
        usage_indexed = usage.set_index('Ingredient')
        waste_indexed = waste.set_index('Ingredient')
        stock_indexed = input_stock.set_index('Ingredient')
        
        # Add quantities to the main dataframe
        df['Used'] = usage_indexed['Used Qty'].reindex(df.index).fillna(0)
        df['Wasted'] = waste_indexed['Wasted Qty'].reindex(df.index).fillna(0)
        df['Stocked'] = stock_indexed['Received Qty'].reindex(df.index).fillna(0)
        
        # Calculate derived metrics
        df['Expected Use'] = df['Used'] + df['Wasted']
        df['Shrinkage'] = df['Stocked'] - df['Expected Use']
        df['Used Cost'] = df['Used'] * df['Unit Cost']
        df['Waste Cost'] = df['Wasted'] * df['Unit Cost']
        df['Shrinkage Cost'] = df['Shrinkage'] * df['Unit Cost']
        df['Total Cost'] = df['Used Cost'] + df['Waste Cost'] + df['Shrinkage Cost']
        
        # Reset index to make Ingredient a column again
        df.reset_index(inplace=True)
        
        return df
        
    except Exception as e:
        st.error(f"Error processing data: {str(e)}")
        return pd.DataFrame()

def create_pdf_report(df: pd.DataFrame) -> bytes:
    """Generate a PDF report from the dataframe."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Restaurant Ingredient Tracking Report", ln=True, align="C")
    pdf.ln(10)
    
    # Table headers
    pdf.set_font("Arial", "B", 8)
    col_width = 25
    headers = ['Ingredient', 'Unit Cost', 'Used', 'Wasted', 'Stocked', 'Shrinkage', 'Used Cost', 'Waste Cost', 'Shrinkage Cost']
    
    for header in headers:
        pdf.cell(col_width, 8, header, border=1, align="C")
    pdf.ln()
    
    # Table data
    pdf.set_font("Arial", size=7)
    for _, row in df.iterrows():
        pdf.cell(col_width, 6, str(row['Ingredient'])[:15], border=1)
        pdf.cell(col_width, 6, f"${row['Unit Cost']:.2f}", border=1, align="R")
        pdf.cell(col_width, 6, f"{row['Used']:.2f}", border=1, align="R")
        pdf.cell(col_width, 6, f"{row['Wasted']:.2f}", border=1, align="R")
        pdf.cell(col_width, 6, f"{row['Stocked']:.2f}", border=1, align="R")
        pdf.cell(col_width, 6, f"{row['Shrinkage']:.2f}", border=1, align="R")
        pdf.cell(col_width, 6, f"${row['Used Cost']:.2f}", border=1, align="R")
        pdf.cell(col_width, 6, f"${row['Waste Cost']:.2f}", border=1, align="R")
        pdf.cell(col_width, 6, f"${row['Shrinkage Cost']:.2f}", border=1, align="R")
        pdf.ln()
    
    # Summary totals
    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Summary Totals:", ln=True)
    pdf.set_font("Arial", size=10)
    
    total_used_cost = df['Used Cost'].sum()
    total_waste_cost = df['Waste Cost'].sum()
    total_shrinkage_cost = df['Shrinkage Cost'].sum()
    grand_total = df['Total Cost'].sum()
    
    pdf.cell(0, 6, f"Total Used Cost: ${total_used_cost:.2f}", ln=True)
    pdf.cell(0, 6, f"Total Waste Cost: ${total_waste_cost:.2f}", ln=True)
    pdf.cell(0, 6, f"Total Shrinkage Cost: ${total_shrinkage_cost:.2f}", ln=True)
    pdf.cell(0, 6, f"Grand Total Cost: ${grand_total:.2f}", ln=True)
    
    return bytes(pdf.output(dest='S'), 'latin1')

def create_excel_report(df: pd.DataFrame) -> bytes:
    """Generate an Excel report from the dataframe."""
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter', options={'remove_timezone': True}) as writer:
        # Write the main data
        df.to_excel(writer, sheet_name='Ingredient Report', index=False)
        
        # Get workbook and worksheet objects
        workbook = writer.book
        worksheet = writer.sheets['Ingredient Report']
        
        # Add formatting
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'fg_color': '#D7E4BC',
            'border': 1
        })
        
        money_format = workbook.add_format({'num_format': '$#,##0.00'})
        number_format = workbook.add_format({'num_format': '#,##0.00'})
        
        # Apply header formatting
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
        
        # Apply number formatting to appropriate columns
        money_columns = ['Unit Cost', 'Used Cost', 'Waste Cost', 'Shrinkage Cost', 'Total Cost']
        number_columns = ['Used', 'Wasted', 'Stocked', 'Shrinkage']
        
        for col_name in money_columns:
            if col_name in df.columns:
                col_idx = df.columns.get_loc(col_name)
                worksheet.set_column(col_idx, col_idx, 12, money_format)
        
        for col_name in number_columns:
            if col_name in df.columns:
                col_idx = df.columns.get_loc(col_name)
                worksheet.set_column(col_idx, col_idx, 10, number_format)
        
        # Add summary totals
        start_row = len(df) + 3
        worksheet.write(start_row, 0, 'Summary Totals:', workbook.add_format({'bold': True}))
        
        worksheet.write(start_row + 1, 0, 'Total Used Cost:')
        worksheet.write(start_row + 1, 1, df['Used Cost'].sum(), money_format)
        
        worksheet.write(start_row + 2, 0, 'Total Waste Cost:')
        worksheet.write(start_row + 2, 1, df['Waste Cost'].sum(), money_format)
        
        worksheet.write(start_row + 3, 0, 'Total Shrinkage Cost:')
        worksheet.write(start_row + 3, 1, df['Shrinkage Cost'].sum(), money_format)
        
        worksheet.write(start_row + 4, 0, 'Grand Total Cost:')
        worksheet.write(start_row + 4, 1, df['Total Cost'].sum(), money_format)
    
    output.seek(0)
    return output.getvalue()

# Main application
def main():
    st.title("🍽️ Restaurant Ingredient Tracker")
    st.markdown("Upload your CSV files to analyze ingredient usage, waste, and costs.")
    
    # Initialize session state
    if 'processed_data' not in st.session_state:
        st.session_state.processed_data = None
    
    # File upload section
    st.header("📁 Upload CSV Files")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Ingredient Information")
        ingredient_file = st.file_uploader(
            "Upload ingredient info CSV (Ingredient, Unit Cost)", 
            type=['csv'], 
            key="ingredient"
        )
        st.caption("Required columns: Ingredient, Unit Cost")
        
        st.subheader("Usage Data")
        usage_file = st.file_uploader(
            "Upload usage CSV (Ingredient, Used Qty)", 
            type=['csv'], 
            key="usage"
        )
        st.caption("Required columns: Ingredient, Used Qty")
    
    with col2:
        st.subheader("Stock/Inventory")
        stock_file = st.file_uploader(
            "Upload stock CSV (Ingredient, Received Qty)", 
            type=['csv'], 
            key="stock"
        )
        st.caption("Required columns: Ingredient, Received Qty")
        
        st.subheader("Waste Data")
        waste_file = st.file_uploader(
            "Upload waste CSV (Ingredient, Wasted Qty)", 
            type=['csv'], 
            key="waste"
        )
        st.caption("Required columns: Ingredient, Wasted Qty")
    
    # Process button
    st.header("📊 Generate Report")
    
    if st.button("🔄 Run Report", type="primary"):
        if all([ingredient_file, stock_file, usage_file, waste_file]):
            try:
                # Read CSV files
                ingredient_df = pd.read_csv(ingredient_file)
                stock_df = pd.read_csv(stock_file)
                usage_df = pd.read_csv(usage_file)
                waste_df = pd.read_csv(waste_file)
                
                # Validate CSV structures
                validations = [
                    validate_csv_structure(ingredient_df, ['Ingredient', 'Unit Cost'], 'Ingredient Info CSV'),
                    validate_csv_structure(stock_df, ['Ingredient', 'Received Qty'], 'Stock CSV'),
                    validate_csv_structure(usage_df, ['Ingredient', 'Used Qty'], 'Usage CSV'),
                    validate_csv_structure(waste_df, ['Ingredient', 'Wasted Qty'], 'Waste CSV')
                ]
                
                if all(validations):
                    # Process the data
                    processed_df = process_ingredient_data(ingredient_df, stock_df, usage_df, waste_df)
                    
                    if not processed_df.empty:
                        st.session_state.processed_data = processed_df
                        st.success("✅ Report generated successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to process data. Please check your CSV files.")
                
            except Exception as e:
                st.error(f"❌ Error reading CSV files: {str(e)}")
                st.info("Please ensure your CSV files are properly formatted and contain the required columns.")
        else:
            st.warning("⚠️ Please upload all four CSV files before running the report.")
    
    # Display results
    if st.session_state.processed_data is not None and not st.session_state.processed_data.empty:
        st.header("📋 Report Results")
        
        df = st.session_state.processed_data
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Used Cost", f"${df['Used Cost'].sum():.2f}")
        with col2:
            st.metric("Total Waste Cost", f"${df['Waste Cost'].sum():.2f}")
        with col3:
            st.metric("Total Shrinkage Cost", f"${df['Shrinkage Cost'].sum():.2f}")
        with col4:
            st.metric("Grand Total Cost", f"${df['Total Cost'].sum():.2f}")
        
        # Data table
        st.subheader("Detailed Results")
        
        # Format numeric columns for display
        display_df = df.copy()
        money_columns = ['Unit Cost', 'Used Cost', 'Waste Cost', 'Shrinkage Cost', 'Total Cost']
        for col in money_columns:
            if col in display_df.columns:
                display_df[col] = display_df[col].apply(lambda x: f"${x:.2f}")
        
        number_columns = ['Used', 'Wasted', 'Stocked', 'Shrinkage']
        for col in number_columns:
            if col in display_df.columns:
                display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}")
        
        st.dataframe(display_df, use_container_width=True)
        
        # Export buttons
        st.header("📤 Export Options")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📊 Export to Excel", type="secondary"):
                try:
                    excel_data = create_excel_report(df)
                    st.download_button(
                        label="⬇️ Download Excel Report",
                        data=excel_data,
                        file_name="ingredient_report.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                except Exception as e:
                    st.error(f"❌ Error creating Excel report: {str(e)}")
        
        with col2:
            if st.button("📄 Export to PDF", type="secondary"):
                try:
                    pdf_data = create_pdf_report(df)
                    st.download_button(
                        label="⬇️ Download PDF Report",
                        data=pdf_data,
                        file_name="ingredient_report.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"❌ Error creating PDF report: {str(e)}")
    
    # Instructions
    with st.expander("ℹ️ How to Use This Tool"):
        st.markdown("""
        **Step 1:** Prepare your CSV files with the following formats:
        
        **Ingredient Info CSV:**
        - Columns: `Ingredient`, `Unit Cost`
        - Example: Tomatoes, 2.50
        
        **Stock CSV:**
        - Columns: `Ingredient`, `Received Qty`
        - Example: Tomatoes, 100
        
        **Usage CSV:**
        - Columns: `Ingredient`, `Used Qty`
        - Example: Tomatoes, 80
        
        **Waste CSV:**
        - Columns: `Ingredient`, `Wasted Qty`
        - Example: Tomatoes, 5
        
        **Step 2:** Upload all four CSV files using the file uploaders above.
        
        **Step 3:** Click "Run Report" to process your data.
        
        **Step 4:** View the results and export to Excel or PDF as needed.
        
        **Calculations:**
        - **Shrinkage** = Stocked - (Used + Wasted)
        - **Used Cost** = Used Qty × Unit Cost
        - **Waste Cost** = Wasted Qty × Unit Cost
        - **Shrinkage Cost** = Shrinkage × Unit Cost
        """)

if __name__ == "__main__":
    main()
