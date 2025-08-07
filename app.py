import streamlit as st
import pandas as pd
import io
from fpdf import FPDF
from typing import Optional, Tuple
import logging
from datetime import datetime


MONEY_COLUMNS = [
    "Unit Cost",
    "Used Cost",
    "Waste Cost",
    "Shrinkage Cost",
    "Total Cost",
]

NUMBER_COLUMNS = ["Used", "Wasted", "Stocked", "Shrinkage"]

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

    # Check for empty dataframe
    if df.empty:
        st.error(f"{file_type} is empty. Please provide a CSV file with data.")
        return False

    # Check for duplicate ingredients
    if 'Ingredient' in df.columns:
        duplicates = df[df['Ingredient'].duplicated()]
        if not duplicates.empty:
            st.error(f"{file_type} contains duplicate ingredients: {', '.join(duplicates['Ingredient'].tolist())}")
            return False

    # Check that expected numeric columns can be parsed as numbers
    numeric_columns = [col for col in required_columns if col.lower() != 'ingredient']
    for col in numeric_columns:
        # First check for negative values in cost and quantity columns
        if df[col].dtype in ['object', 'string']:
            converted = pd.to_numeric(df[col], errors='coerce')
        else:
            converted = df[col]
            
        if pd.isna(converted).any():
            invalid_rows = df[pd.isna(converted)]
            st.error(f"{file_type} has non-numeric values in column '{col}' at rows: {invalid_rows.index.tolist()}")
            return False
            
        # Check for negative values (which don't make sense for costs/quantities)
        if (converted < 0).any():
            negative_rows = df[converted < 0]
            st.warning(f"{file_type} has negative values in column '{col}' at rows: {negative_rows.index.tolist()}")

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

        # Identify ingredients present in stock/usage/waste but missing from
        # the ingredient info. Warn the user and include them with zero cost
        # so they appear in the final report.
        all_indices = usage_indexed.index.union(waste_indexed.index).union(stock_indexed.index)
        missing_ingredients = all_indices.difference(df.index)
        if not missing_ingredients.empty:
            st.warning(
                "The following ingredients were found in stock, usage, or waste files but "
                "are missing from the ingredient info: "
                + ", ".join(missing_ingredients)
            )
            # Add the missing ingredients to the dataframe with zero unit cost
            df = df.reindex(df.index.union(missing_ingredients), fill_value=0)

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
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 8, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align="C")
    pdf.ln(10)
    
    # Table headers - adjust column widths for better fit
    pdf.set_font("Arial", "B", 7)
    col_widths = [30, 18, 15, 15, 18, 18, 20, 20, 25]  # Custom widths for each column
    headers = ['Ingredient', 'Unit Cost', 'Used', 'Wasted', 'Stocked', 'Shrinkage', 'Used Cost', 'Waste Cost', 'Shrinkage Cost']
    
    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 8, header, border=1, align="C")
    pdf.ln()
    
    # Table data
    pdf.set_font("Arial", size=6)
    for _, row in df.iterrows():
        # Check if we need a new page
        if pdf.get_y() > 250:
            pdf.add_page()
            # Re-add headers on new page
            pdf.set_font("Arial", "B", 7)
            for i, header in enumerate(headers):
                pdf.cell(col_widths[i], 8, header, border=1, align="C")
            pdf.ln()
            pdf.set_font("Arial", size=6)
            
        pdf.cell(col_widths[0], 6, str(row['Ingredient'])[:20], border=1)
        pdf.cell(col_widths[1], 6, f"${row['Unit Cost']:.2f}", border=1, align="R")
        pdf.cell(col_widths[2], 6, f"{row['Used']:.1f}", border=1, align="R")
        pdf.cell(col_widths[3], 6, f"{row['Wasted']:.1f}", border=1, align="R")
        pdf.cell(col_widths[4], 6, f"{row['Stocked']:.1f}", border=1, align="R")
        pdf.cell(col_widths[5], 6, f"{row['Shrinkage']:.1f}", border=1, align="R")
        pdf.cell(col_widths[6], 6, f"${row['Used Cost']:.2f}", border=1, align="R")
        pdf.cell(col_widths[7], 6, f"${row['Waste Cost']:.2f}", border=1, align="R")
        pdf.cell(col_widths[8], 6, f"${row['Shrinkage Cost']:.2f}", border=1, align="R")
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
    
    pdf_output = pdf.output(dest='S')
    if isinstance(pdf_output, str):
        return pdf_output.encode('latin1')
    return bytes(pdf_output)

def create_excel_report(df: pd.DataFrame) -> bytes:
    """Generate an Excel report from the dataframe."""
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
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
        for col_name in MONEY_COLUMNS:
            if col_name in df.columns:
                col_idx = df.columns.get_loc(col_name)
                worksheet.set_column(col_idx, col_idx, 12, money_format)

        for col_name in NUMBER_COLUMNS:
            if col_name in df.columns:
                col_idx = df.columns.get_loc(col_name)
                worksheet.set_column(col_idx, col_idx, 10, number_format)
        
        # Add summary totals with additional insights
        start_row = len(df) + 3
        bold_format = workbook.add_format({'bold': True})
        
        worksheet.write(start_row, 0, 'Summary Totals:', bold_format)
        
        total_used = df['Used Cost'].sum()
        total_waste = df['Waste Cost'].sum()
        total_shrinkage = df['Shrinkage Cost'].sum()
        grand_total = df['Total Cost'].sum()
        
        worksheet.write(start_row + 1, 0, 'Total Used Cost:')
        worksheet.write(start_row + 1, 1, total_used, money_format)
        
        worksheet.write(start_row + 2, 0, 'Total Waste Cost:')
        worksheet.write(start_row + 2, 1, total_waste, money_format)
        worksheet.write(start_row + 2, 2, f"{(total_waste/grand_total*100):.1f}% of total" if grand_total > 0 else "")
        
        worksheet.write(start_row + 3, 0, 'Total Shrinkage Cost:')
        worksheet.write(start_row + 3, 1, total_shrinkage, money_format)
        worksheet.write(start_row + 3, 2, f"{(total_shrinkage/grand_total*100):.1f}% of total" if grand_total > 0 else "")
        
        worksheet.write(start_row + 4, 0, 'Grand Total Cost:')
        worksheet.write(start_row + 4, 1, grand_total, money_format)
        
        # Add generation timestamp
        worksheet.write(start_row + 6, 0, 'Report Generated:')
        worksheet.write(start_row + 6, 1, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    
    output.seek(0)
    return output.getvalue()


def handle_file_upload() -> Tuple[
    Optional[pd.DataFrame],
    Optional[pd.DataFrame],
    Optional[pd.DataFrame],
    Optional[pd.DataFrame],
]:
    """Display file uploaders and return the uploaded dataframes.

    Returns a tuple containing dataframes for ingredient information, stock,
    usage and waste. Elements will be ``None`` if the file is missing or fails
    validation.
    """

    st.header("📁 Upload CSV Files")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ingredient Information")
        ingredient_file = st.file_uploader(
            "Upload ingredient info CSV (Ingredient, Unit Cost)",
            type=["csv"],
            key="ingredient",
        )
        st.caption("Required columns: Ingredient, Unit Cost")

        st.subheader("Usage Data")
        usage_file = st.file_uploader(
            "Upload usage CSV (Ingredient, Used Qty)",
            type=["csv"],
            key="usage",
        )
        st.caption("Required columns: Ingredient, Used Qty")

    with col2:
        st.subheader("Stock/Inventory")
        stock_file = st.file_uploader(
            "Upload stock CSV (Ingredient, Received Qty)",
            type=["csv"],
            key="stock",
        )
        st.caption("Required columns: Ingredient, Received Qty")

        st.subheader("Waste Data")
        waste_file = st.file_uploader(
            "Upload waste CSV (Ingredient, Wasted Qty)",
            type=["csv"],
            key="waste",
        )
        st.caption("Required columns: Ingredient, Wasted Qty")

    dfs = []
    uploads = [
        (ingredient_file, ["Ingredient", "Unit Cost"], "Ingredient Info CSV"),
        (stock_file, ["Ingredient", "Received Qty"], "Stock CSV"),
        (usage_file, ["Ingredient", "Used Qty"], "Usage CSV"),
        (waste_file, ["Ingredient", "Wasted Qty"], "Waste CSV"),
    ]

    for file, required, msg in uploads:
        if file is None:
            dfs.append(None)
            continue
        try:
            df = pd.read_csv(file)
            dfs.append(df if validate_csv_structure(df, required, msg) else None)
        except Exception as e:
            st.error(f"❌ Error reading {msg}: {str(e)}")
            dfs.append(None)

    return dfs[0], dfs[1], dfs[2], dfs[3]


def generate_report(
    ingredient_df: Optional[pd.DataFrame],
    stock_df: Optional[pd.DataFrame],
    usage_df: Optional[pd.DataFrame],
    waste_df: Optional[pd.DataFrame],
) -> Optional[pd.DataFrame]:
    """Validate inputs and return a processed report dataframe.

    Parameters are dataframes returned from :func:`handle_file_upload`. The
    function yields ``None`` when required data is missing or processing fails.
    """

    if not all([ingredient_df is not None, stock_df is not None, usage_df is not None, waste_df is not None]):
        st.warning("⚠️ Please upload all four CSV files before running the report.")
        return None

    # Type assertion since we've already checked for None values
    assert ingredient_df is not None
    assert stock_df is not None 
    assert usage_df is not None
    assert waste_df is not None
    
    processed_df = process_ingredient_data(ingredient_df, stock_df, usage_df, waste_df)
    return processed_df if not processed_df.empty else None


def display_results(df: pd.DataFrame) -> None:
    """Render summary metrics and a detailed results table."""

    st.header("📋 Report Results")

    # Calculate key metrics
    total_used_cost = df['Used Cost'].sum()
    total_waste_cost = df['Waste Cost'].sum()
    total_shrinkage_cost = df['Shrinkage Cost'].sum()
    grand_total_cost = df['Total Cost'].sum()
    
    # Calculate percentages for better insights
    waste_percentage = (total_waste_cost / grand_total_cost * 100) if grand_total_cost > 0 else 0
    shrinkage_percentage = (total_shrinkage_cost / grand_total_cost * 100) if grand_total_cost > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Used Cost", f"${total_used_cost:.2f}")
    with col2:
        st.metric("Total Waste Cost", f"${total_waste_cost:.2f}", 
                 delta=f"{waste_percentage:.1f}% of total" if waste_percentage > 0 else None)
    with col3:
        st.metric("Total Shrinkage Cost", f"${total_shrinkage_cost:.2f}",
                 delta=f"{shrinkage_percentage:.1f}% of total" if shrinkage_percentage > 0 else None)
    with col4:
        st.metric("Grand Total Cost", f"${grand_total_cost:.2f}")

    # Add insights section
    if waste_percentage > 5 or shrinkage_percentage > 5:
        st.warning("💡 **Insights**: " + 
                  (f"High waste percentage ({waste_percentage:.1f}%). " if waste_percentage > 5 else "") +
                  (f"High shrinkage percentage ({shrinkage_percentage:.1f}%). " if shrinkage_percentage > 5 else "") +
                  "Consider reviewing inventory management processes.")

    st.subheader("Detailed Results")
    
    # Add filtering options
    col1, col2 = st.columns(2)
    with col1:
        show_only_issues = st.checkbox("Show only items with waste or shrinkage > $1", value=False)
    with col2:
        sort_by = st.selectbox("Sort by", ["Ingredient", "Total Cost", "Waste Cost", "Shrinkage Cost"], index=1)
    
    # Apply filters and sorting
    filtered_df = df.copy()
    if show_only_issues:
        filtered_df = filtered_df[(filtered_df['Waste Cost'] > 1) | (filtered_df['Shrinkage Cost'] > 1)]
    
    # Sort the dataframe
    ascending = sort_by != "Total Cost"  # Sort costs in descending order by default
    filtered_df = filtered_df.sort_values(sort_by, ascending=ascending)
    
    # Format the display dataframe
    display_df = filtered_df.copy()
    for col in MONEY_COLUMNS:
        if col in display_df.columns:
            display_df[col] = display_df[col].apply(lambda x: f"${x:.2f}")

    for col in NUMBER_COLUMNS:
        if col in display_df.columns:
            display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}")

    st.dataframe(display_df, use_container_width=True, height=400)
    
    # Show record count
    st.caption(f"Showing {len(filtered_df)} of {len(df)} ingredients")


def render_export_buttons(df: pd.DataFrame) -> None:
    """Display buttons for exporting the report to Excel or PDF."""

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
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
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
                    mime="application/pdf",
                )
            except Exception as e:
                st.error(f"❌ Error creating PDF report: {str(e)}")

# Main application
def main():
    """Streamlit application entry point."""

    st.title("🍽️ Restaurant Ingredient Tracker")
    st.markdown("Upload your CSV files to analyze ingredient usage, waste, and costs.")
    
    # Initialize session state
    if "processed_data" not in st.session_state:
        st.session_state.processed_data = None
    if "show_sample_data" not in st.session_state:
        st.session_state.show_sample_data = False
    
    # Add sample data option
    with st.expander("🎯 Try with Sample Data"):
        st.markdown("Don't have your own data yet? Try the app with our sample restaurant data.")
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📋 Load Sample Data", type="secondary"):
                try:
                    ingredient_df = pd.read_csv("sample_ingredient_info.csv")
                    stock_df = pd.read_csv("sample_input_stock.csv") 
                    usage_df = pd.read_csv("sample_usage.csv")
                    waste_df = pd.read_csv("sample_waste.csv")
                    
                    processed_df = process_ingredient_data(ingredient_df, stock_df, usage_df, waste_df)
                    if not processed_df.empty:
                        st.session_state.processed_data = processed_df
                        st.session_state.show_sample_data = True
                        st.success("✅ Sample data loaded successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to process sample data.")
                except Exception as e:
                    st.error(f"❌ Error loading sample data: {str(e)}")
                    
        with col2:
            if st.button("🗑️ Clear Sample Data"):
                st.session_state.processed_data = None
                st.session_state.show_sample_data = False
                st.success("Sample data cleared!")
                st.rerun()
    
    if st.session_state.show_sample_data:
        st.info("📊 Currently showing results from sample data. Upload your own files to analyze your restaurant's data.")

    ingredient_df, stock_df, usage_df, waste_df = handle_file_upload()

    st.header("📊 Generate Report")
    if st.button("🔄 Run Report", type="primary"):
        processed_df = generate_report(ingredient_df, stock_df, usage_df, waste_df)
        if processed_df is not None:
            st.session_state.processed_data = processed_df
            st.success("✅ Report generated successfully!")
            st.rerun()
        else:
            st.error("❌ Failed to process data. Please check your CSV files.")

    if st.session_state.processed_data is not None and not st.session_state.processed_data.empty:
        display_results(st.session_state.processed_data)
        render_export_buttons(st.session_state.processed_data)

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
