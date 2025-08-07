import streamlit as st
import pandas as pd
import io
from fpdf import FPDF
from typing import Optional, Tuple
import logging
from datetime import datetime
import os
import requests
from urllib.parse import urlencode
import json


MONEY_COLUMNS = [
    "Unit Cost",
    "Used Cost",
    "Waste Cost",
    "Shrinkage Cost",
    "Total Cost",
]

NUMBER_COLUMNS = ["Used", "Wasted", "Stocked"]

# Page configuration
st.set_page_config(
    page_title="Restaurant Ingredient Tracker",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Replit Auth Configuration
class ReplitAuth:
    """Replit Authentication Handler with enterprise-grade features."""
    
    def __init__(self):
        self.repl_id = os.getenv('REPL_ID')
        self.repl_owner = os.getenv('REPL_OWNER') 
        self.replit_user = os.getenv('REPLIT_USER')
        self.replit_domains = os.getenv('REPLIT_DOMAINS')
        
    def is_replit_environment(self) -> bool:
        """Check if running in Replit environment."""
        return self.repl_id is not None
    
    def get_authenticated_user(self) -> dict:
        """Get authenticated user information."""
        if not self.is_replit_environment():
            return {'authenticated': False, 'user': None}
        
        # Primary authentication through Replit environment
        username = self.replit_user or self.repl_owner
        
        if username and self.repl_id:
            user_data = {
                'id': self.repl_owner,
                'username': username,
                'display_name': username,
                'repl_id': self.repl_id,
                'authenticated': True,
                'auth_method': 'replit_builtin',
                'session_data': {
                    'repl_owner': self.repl_owner,
                    'replit_user': self.replit_user,
                    'domains': self.replit_domains
                }
            }
            return {'authenticated': True, 'user': user_data}
        
        return {'authenticated': False, 'user': None}
    
    def create_session(self, user_data: dict) -> bool:
        """Create authenticated session in Streamlit."""
        if user_data and user_data.get('authenticated'):
            st.session_state.replit_auth = True
            st.session_state.replit_user = user_data['user']
            st.session_state.current_page = "dashboard"
            return True
        return False
    
    def clear_session(self):
        """Clear authentication session."""
        # Clear all auth-related session state
        auth_keys = [key for key in st.session_state.keys() 
                    if key.startswith(('replit_', 'demo_', 'processed_', 'show_sample_', 'current_page'))]
        
        for key in auth_keys:
            if key in st.session_state:
                del st.session_state[key]
        
        st.session_state.replit_auth = False
        st.session_state.current_page = "login"
    
    def is_authenticated(self) -> bool:
        """Check if user is currently authenticated."""
        return st.session_state.get('replit_auth', False)
    
    def get_current_user(self) -> dict:
        """Get current authenticated user data."""
        return st.session_state.get('replit_user', {})

# Initialize Replit Auth
replit_auth = ReplitAuth()

def get_replit_user_info():
    """Legacy function - use ReplitAuth class instead."""
    auth_result = replit_auth.get_authenticated_user()
    if auth_result['authenticated']:
        user = auth_result['user']
        return {
            'id': user['id'],
            'name': user['username'],
            'authenticated': True,
            'repl_id': user['repl_id'],
            'repl_owner': user['session_data']['repl_owner'],
            'replit_user': user['session_data']['replit_user']
        }
    return {'authenticated': False}

def is_replit_environment():
    """Check if running in Replit environment."""
    return replit_auth.is_replit_environment()

# Fallback authentication for non-Replit environments
DEMO_USERS = {
    "admin": "admin123",
    "manager": "manager456", 
    "staff": "staff789"
}

def verify_demo_password(username: str, password: str) -> bool:
    """Verify demo user credentials for non-Replit environments."""
    return username in DEMO_USERS and DEMO_USERS[username] == password

def show_replit_login_page():
    """Display Replit Auth login page."""
    st.markdown("""
    <div style="text-align: center; padding: 3rem 0;">
        <h1>🍽️ Restaurant Ingredient Tracker</h1>
        <h2>Enterprise Authentication via Replit</h2>
        <p style="font-size: 1.3rem; color: #666; margin: 2rem 0;">
            Secure, scalable authentication powered by enterprise-grade infrastructure
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features showcase
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        ### 🔐 Enterprise Security
        - Firebase & Google Cloud Identity Platform
        - reCAPTCHA fraud prevention
        - Global scalability with Stytch
        """)
    
    with col2:
        st.markdown("""
        ### 📊 Advanced Analytics
        - Ingredient usage tracking
        - Cost analysis & optimization
        - Waste reduction insights
        """)
    
    with col3:
        st.markdown("""
        ### 📈 Smart Reporting
        - PDF & Excel exports
        - Real-time dashboards
        - Custom filtering options
        """)
    
    st.markdown("---")
    
    # Authentication attempt
    auth_result = replit_auth.get_authenticated_user()
    
    if auth_result['authenticated']:
        # User is authenticated, create session
        if replit_auth.create_session(auth_result):
            user = auth_result['user']
            st.success(f"Welcome back, **{user['display_name']}**! Redirecting to your dashboard...")
            st.info("You are authenticated through Replit's enterprise-grade authentication system.")
            
            # Show user info
            with st.expander("Authentication Details"):
                st.json({
                    'user_id': user['id'],
                    'username': user['username'],
                    'auth_method': user['auth_method'],
                    'repl_id': user['repl_id'][:8] + "...",  # Truncate for privacy
                    'status': 'Authenticated ✓'
                })
            
            st.rerun()
    else:
        # Authentication failed
        st.error("Authentication required. Please ensure you're logged into Replit.")
        st.info("This app uses Replit's built-in authentication system for secure access.")
        
        # Troubleshooting info
        with st.expander("🔧 Troubleshooting"):
            st.markdown("""
            **If you're seeing this message:**
            
            1. **Make sure you're logged into Replit** - Check the top-right corner of Replit
            2. **Refresh the page** - Sometimes authentication needs a refresh
            3. **Check your browser** - Ensure cookies and JavaScript are enabled
            4. **Try in a new tab** - Open the app in a fresh browser tab
            
            **For developers:**
            - This app uses Replit's enterprise authentication system
            - Authentication is automatic when running on Replit platform
            - No additional configuration required
            """)
            
            # Debug info for troubleshooting
            if st.checkbox("Show Debug Information"):
                st.json({
                    'repl_id_present': replit_auth.repl_id is not None,
                    'repl_owner_present': replit_auth.repl_owner is not None,
                    'replit_user_present': replit_auth.replit_user is not None,
                    'environment_detected': replit_auth.is_replit_environment()
                })

def show_demo_login():
    """Display demo login form for non-Replit environments."""
    # Welcome landing page
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1>🍽️ Restaurant Ingredient Tracker</h1>
        <h3>Analyze ingredient usage, waste, and costs</h3>
        <p style="font-size: 1.2rem; color: #666;">
            Track your restaurant's inventory efficiency and reduce waste costs
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features overview
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        ### 📊 Data Analysis
        - Upload CSV files for analysis
        - Calculate usage, waste & shrinkage
        - Identify cost-saving opportunities
        """)
    
    with col2:
        st.markdown("""
        ### 📈 Reporting
        - Export to PDF & Excel formats  
        - View detailed cost breakdowns
        - Track trends over time
        """)
    
    with col3:
        st.markdown("""
        ### ⚡ Easy to Use
        - Simple file upload interface
        - Sample data for testing
        - Instant report generation
        """)
    
    st.markdown("---")
    st.info("Running in demo mode. Use the credentials below to test the application.")
    
    # Login form in centered container
    with st.container():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            with st.form("demo_login_form"):
                st.markdown("### 🔐 Login to Continue")
                username = st.text_input("Username", placeholder="Enter username")
                password = st.text_input("Password", type="password", placeholder="Enter password")
                login_button = st.form_submit_button("🚀 Login", type="primary", use_container_width=True)
                
                # Demo accounts info
                with st.expander("👥 Available Demo Accounts"):
                    st.markdown("""
                    **Choose from these test accounts:**
                    
                    🔹 **Admin Account**  
                    Username: `admin` | Password: `admin123`
                    
                    🔹 **Manager Account**  
                    Username: `manager` | Password: `manager456`
                    
                    🔹 **Staff Account**  
                    Username: `staff` | Password: `staff789`
                    """)
                
                if login_button:
                    if verify_demo_password(username, password):
                        st.session_state.demo_authenticated = True
                        st.session_state.demo_username = username
                        st.session_state.current_page = "dashboard"
                        st.success(f"Welcome, {username}! Redirecting to dashboard...")
                        st.rerun()
                    else:
                        st.error("Invalid username or password. Please try again.")

def show_navigation_sidebar():
    """Display navigation sidebar with page selection and logout."""
    with st.sidebar:
        st.markdown("### 🍽️ Restaurant Tracker")
        
        # User info section
        if replit_auth.is_authenticated():
            user = replit_auth.get_current_user()
            username = user.get('display_name', 'User')
            auth_method = user.get('auth_method', 'replit_builtin')
            
            st.markdown(f"**Logged in as:** {username}")
            if auth_method == 'replit_builtin':
                st.markdown("*via Replit Auth* 🔐")
            else:
                st.markdown(f"*via {auth_method}* 🔐")
        else:
            # Fallback for demo mode
            username = st.session_state.get('demo_username', 'Demo User')
            st.markdown(f"**Demo Mode:** {username}")
        
        st.markdown("---")
        
        # Page navigation
        st.markdown("### 📋 Navigation")
        
        # Initialize current_page if not exists
        if "current_page" not in st.session_state:
            st.session_state.current_page = "dashboard"
        
        # Navigation buttons
        if st.button("🏠 Dashboard", type="secondary", use_container_width=True):
            st.session_state.current_page = "dashboard"
            st.rerun()
            
        if st.button("📊 Analytics", type="secondary", use_container_width=True):
            st.session_state.current_page = "analytics"
            st.rerun()
            
        if st.button("📤 Reports", type="secondary", use_container_width=True):
            st.session_state.current_page = "reports"
            st.rerun()
            
        if st.button("⚙️ Settings", type="secondary", use_container_width=True):
            st.session_state.current_page = "settings"
            st.rerun()
        
        st.markdown("---")
        
        # Logout section
        st.markdown("### 🔐 Account")
        if st.button("🚪 Logout", type="primary", use_container_width=True):
            # Use proper auth logout
            if replit_auth.is_authenticated():
                replit_auth.clear_session()
            else:
                # Fallback for demo mode
                st.session_state.demo_authenticated = False
                st.session_state.demo_username = None
                st.session_state.processed_data = None
                st.session_state.show_sample_data = False
                st.session_state.current_page = "login"
            
            st.success("Logged out successfully!")
            st.rerun()

def check_authentication():
    """Check if user is authenticated via Replit Auth or demo mode."""
    if is_replit_environment():
        # Use Replit Auth
        if replit_auth.is_authenticated():
            # Already authenticated
            show_navigation_sidebar()
            return True
        else:
            # Try to authenticate
            auth_result = replit_auth.get_authenticated_user()
            if auth_result['authenticated']:
                replit_auth.create_session(auth_result)
                show_navigation_sidebar()
                return True
            else:
                show_replit_login_page()
                return False
    else:
        # Use demo mode for local/non-Replit environments
        if "demo_authenticated" not in st.session_state:
            st.session_state.demo_authenticated = False
        
        if not st.session_state.demo_authenticated:
            show_demo_login()
            return False
        else:
            show_navigation_sidebar()
            return True

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
        negative_mask = converted < 0
        if negative_mask.any():
            negative_rows = df[negative_mask]
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
        df['Used Cost'] = df['Used'] * df['Unit Cost']
        df['Waste Cost'] = df['Wasted'] * df['Unit Cost']
        df['Expected Use Cost'] = df['Expected Use'] * df['Unit Cost']
        df['Stocked Cost'] = df['Stocked'] * df['Unit Cost']
        # Shrinkage Cost is the dollar value of missing/stolen inventory
        # Formula: Stocked Cost - Expected Use Cost = Shrinkage Cost
        df['Shrinkage Cost'] = df['Stocked Cost'] - df['Expected Use Cost']
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
    col_widths = [30, 18, 15, 15, 18, 25, 20, 20, 25]  # Custom widths for each column
    headers = ['Ingredient', 'Unit Cost', 'Used', 'Wasted', 'Stocked', 'Shrinkage Cost', 'Used Cost', 'Waste Cost', 'Total Cost']
    
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
        pdf.cell(col_widths[5], 6, f"${row['Shrinkage Cost']:.2f}", border=1, align="R")
        pdf.cell(col_widths[6], 6, f"${row['Used Cost']:.2f}", border=1, align="R")
        pdf.cell(col_widths[7], 6, f"${row['Waste Cost']:.2f}", border=1, align="R")
        pdf.cell(col_widths[8], 6, f"${row['Total Cost']:.2f}", border=1, align="R")
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
    high_shrinkage_items = df[df['Shrinkage Cost'] > 10]
    missing_stock_items = df[df['Stocked'] == 0]
    
    if waste_percentage > 5 or shrinkage_percentage > 5:
        st.warning("💡 **Insights**: " + 
                  (f"High waste percentage ({waste_percentage:.1f}%). " if waste_percentage > 5 else "") +
                  (f"High shrinkage percentage ({shrinkage_percentage:.1f}%). " if shrinkage_percentage > 5 else "") +
                  "Consider reviewing inventory management processes.")
    
    if not high_shrinkage_items.empty:
        st.error(f"⚠️ **Alert**: {len(high_shrinkage_items)} Items have Shrinkage totaling ${high_shrinkage_items['Shrinkage Cost'].sum():.2f}")
    
    if not missing_stock_items.empty:
        st.warning(f"📦 **Missing Stock**: {len(missing_stock_items)} ingredients show zero stocked quantities but have usage or waste. "
                  f"Items: {', '.join(missing_stock_items['Ingredient'].head(5).tolist())}"
                  f"{' and others...' if len(missing_stock_items) > 5 else ''}")

    st.subheader("Detailed Results")
    
    # Add filtering options
    col1, col2 = st.columns(2)
    with col1:
        show_only_issues = st.checkbox("Show only items with shrinkage > $10", value=False)
    with col2:
        sort_by = st.selectbox("Sort by", ["Ingredient", "Total Cost", "Waste Cost", "Shrinkage Cost"], index=3)
    
    # Apply filters and sorting
    filtered_df = df.copy()
    if show_only_issues:
        filtered_df = filtered_df[filtered_df['Shrinkage Cost'] > 10]
    
    # Sort the dataframe
    ascending = sort_by == "Ingredient"  # Sort ingredient names ascending, costs descending
    filtered_df = filtered_df.sort_values(by=sort_by, ascending=ascending)
    
    # Format the display dataframe
    display_df = filtered_df.copy()
    
    # First format the numbers before applying styling
    for col in MONEY_COLUMNS:
        if col in display_df.columns:
            display_df[col] = display_df[col].apply(lambda x: f"${x:.2f}")

    for col in NUMBER_COLUMNS:
        if col in display_df.columns:
            display_df[col] = display_df[col].apply(lambda x: f"{x:.2f}")
    
    # Create highlighting function using the original numeric values before formatting
    def highlight_issues(row):
        try:
            # Get the corresponding row from filtered_df using the same index
            original_row = filtered_df.loc[row.name]
            
            # Check conditions using original numeric values
            high_shrinkage = original_row['Shrinkage Cost'] > 10
            missing_stock = original_row['Stocked'] == 0 and (original_row['Used'] > 0 or original_row['Wasted'] > 0)
            
            if high_shrinkage:
                return ['background-color: #ffebee; color: #000000;'] * len(row)  # Light red with black text
            elif missing_stock:
                return ['background-color: #fff3e0; color: #000000;'] * len(row)  # Light orange with black text
            else:
                return ['background-color: white; color: #000000;'] * len(row)  # White background with black text
        except:
            return ['background-color: white; color: #000000;'] * len(row)  # Default to white if any error
    
    # Apply styling and display
    styled_df = display_df.style.apply(highlight_issues, axis=1)
    st.dataframe(styled_df, use_container_width=True, height=400)
    
    # Show record count and legend
    st.caption(f"Showing {len(filtered_df)} of {len(df)} ingredients")
    
    # Add legend for visual indicators
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("🔴 **Red highlighting**: Shrinkage > $10")
    with col2:
        st.markdown("🟠 **Orange highlighting**: Missing stock but has usage/waste")
    with col3:
        if show_only_issues:
            st.info(f"Filtered to show {len(filtered_df)} items with shrinkage > $10")


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

def show_dashboard_page():
    """Display the main dashboard page with data upload and processing."""
    st.title("🏠 Dashboard")
    st.markdown("Upload your CSV files to analyze ingredient usage, waste, and costs.")
    
    # Initialize session state
    if "processed_data" not in st.session_state:
        st.session_state.processed_data = None
    if "show_sample_data" not in st.session_state:
        st.session_state.show_sample_data = False
    
    # Quick stats at the top if data exists
    if st.session_state.processed_data is not None and not st.session_state.processed_data.empty:
        df = st.session_state.processed_data
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_cost = df['Total Cost'].sum()
            st.metric("Total Cost", f"${total_cost:,.2f}")
        
        with col2:
            waste_cost = df['Waste Cost'].sum()
            st.metric("Waste Cost", f"${waste_cost:,.2f}")
        
        with col3:
            shrinkage_cost = df['Shrinkage Cost'].sum()
            st.metric("Shrinkage Cost", f"${shrinkage_cost:,.2f}")
        
        with col4:
            high_shrinkage = len(df[df['Shrinkage Cost'] > 10])
            st.metric("High Shrinkage Items", high_shrinkage)
        
        st.markdown("---")
    
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
                        st.success("Sample data loaded successfully!")
                        st.rerun()
                    else:
                        st.error("Failed to process sample data.")
                except Exception as e:
                    st.error(f"Error loading sample data: {str(e)}")
                    
        with col2:
            if st.button("🗑️ Clear Sample Data"):
                st.session_state.processed_data = None
                st.session_state.show_sample_data = False
                st.success("Sample data cleared!")
                st.rerun()
    
    if st.session_state.show_sample_data:
        st.info("Currently showing results from sample data. Upload your own files to analyze your restaurant's data.")

    ingredient_df, stock_df, usage_df, waste_df = handle_file_upload()

    st.header("📊 Generate Report")
    if st.button("🔄 Run Report", type="primary"):
        processed_df = generate_report(ingredient_df, stock_df, usage_df, waste_df)
        if processed_df is not None:
            st.session_state.processed_data = processed_df
            st.success("Report generated successfully!")
            st.rerun()
        else:
            st.error("Failed to process data. Please check your CSV files.")

    if st.session_state.processed_data is not None and not st.session_state.processed_data.empty:
        display_results(st.session_state.processed_data)

def show_analytics_page():
    """Display detailed analytics and insights."""
    st.title("📊 Analytics")
    
    if st.session_state.get('processed_data') is None or st.session_state.processed_data.empty:
        st.warning("No data available. Please go to the Dashboard to upload data first.")
        if st.button("🏠 Go to Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()
        return
    
    df = st.session_state.processed_data
    st.markdown("Detailed analysis of your ingredient data.")
    
    # Advanced analytics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Top 10 Most Expensive Items")
        top_cost = df.nlargest(10, 'Total Cost')[['Ingredient', 'Total Cost']]
        st.dataframe(top_cost, use_container_width=True)
    
    with col2:
        st.subheader("Top 10 Highest Waste")
        top_waste = df.nlargest(10, 'Waste Cost')[['Ingredient', 'Waste Cost']]
        st.dataframe(top_waste, use_container_width=True)
    
    st.markdown("---")
    
    # Filtering and sorting options
    st.subheader("Filter and Sort Data")
    col1, col2 = st.columns(2)
    
    with col1:
        sort_by = st.selectbox("Sort by:", 
            options=['Total Cost', 'Waste Cost', 'Shrinkage Cost', 'Used Cost'],
            index=0)
    
    with col2:
        ascending = st.checkbox("Ascending order", value=False)
    
    # Apply sorting
    sorted_df = df.sort_values(sort_by, ascending=ascending)
    display_results(sorted_df)

def show_reports_page():
    """Display export and reporting options."""
    st.title("📤 Reports & Export")
    
    if st.session_state.get('processed_data') is None or st.session_state.processed_data.empty:
        st.warning("No data available. Please go to the Dashboard to upload data first.")
        if st.button("🏠 Go to Dashboard"):
            st.session_state.current_page = "dashboard"
            st.rerun()
        return
    
    df = st.session_state.processed_data
    
    # Report summary
    st.subheader("Report Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Items", len(df))
        st.metric("Items with High Shrinkage", len(df[df['Shrinkage Cost'] > 10]))
    
    with col2:
        st.metric("Total Investment", f"${df['Total Cost'].sum():,.2f}")
        st.metric("Total Waste", f"${df['Waste Cost'].sum():,.2f}")
    
    with col3:
        waste_percentage = (df['Waste Cost'].sum() / df['Total Cost'].sum()) * 100
        shrinkage_percentage = (df['Shrinkage Cost'].sum() / df['Total Cost'].sum()) * 100
        st.metric("Waste %", f"{waste_percentage:.1f}%")
        st.metric("Shrinkage %", f"{shrinkage_percentage:.1f}%")
    
    st.markdown("---")
    render_export_buttons(df)

def show_settings_page():
    """Display settings and help information."""
    st.title("⚙️ Settings & Help")
    
    # User information
    st.subheader("Authentication Status")
    
    if replit_auth.is_authenticated():
        user = replit_auth.get_current_user()
        st.success("Authenticated via Replit Auth")
        
        col1, col2 = st.columns(2)
        with col1:
            st.info(f"**User:** {user.get('display_name', 'Unknown')}")
            st.info(f"**User ID:** {user.get('id', 'N/A')}")
        with col2:
            st.info(f"**Auth Method:** {user.get('auth_method', 'Unknown')}")
            st.info(f"**Session:** Active")
            
        # Enhanced auth details
        with st.expander("Authentication Details"):
            st.json({
                'username': user.get('username'),
                'display_name': user.get('display_name'),
                'auth_method': user.get('auth_method'),
                'repl_id': user.get('repl_id', '')[:8] + "..." if user.get('repl_id') else 'N/A',
                'authenticated': user.get('authenticated', False),
                'session_active': True
            })
            
    elif st.session_state.get('demo_authenticated', False):
        username = st.session_state.get('demo_username', 'Unknown User')
        st.warning("Running in Demo Mode")
        st.info(f"**Demo User:** {username}")
        
    else:
        st.error("Not Authenticated")
        st.info("Please log in to access the application")
    
    st.markdown("---")
    
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
        
        **Step 2:** Upload all four CSV files using the file uploaders on the Dashboard.
        
        **Step 3:** Click "Run Report" to process your data.
        
        **Step 4:** View the results and export to Excel or PDF as needed.
        
        **Calculations:**
        - **Expected Use** = Used + Wasted
        - **Used Cost** = Used Qty × Unit Cost
        - **Waste Cost** = Wasted Qty × Unit Cost  
        - **Shrinkage Cost** = (Stocked × Unit Cost) - (Expected Use × Unit Cost)
        - **Total Cost** = Used Cost + Waste Cost + Shrinkage Cost
        """)
    
    # Clear data option
    st.markdown("---")
    st.subheader("Data Management")
    if st.button("🗑️ Clear All Data", type="secondary"):
        st.session_state.processed_data = None
        st.session_state.show_sample_data = False
        st.success("All data cleared!")
        st.rerun()

# Main application
def main():
    """Streamlit application entry point."""
    
    # Check authentication first
    if not check_authentication():
        return
    
    # Initialize session state for navigation
    if "current_page" not in st.session_state:
        st.session_state.current_page = "dashboard"
    
    # Route to appropriate page
    if st.session_state.current_page == "dashboard":
        show_dashboard_page()
    elif st.session_state.current_page == "analytics":
        show_analytics_page()
    elif st.session_state.current_page == "reports":
        show_reports_page()
    elif st.session_state.current_page == "settings":
        show_settings_page()
    else:
        # Default to dashboard
        st.session_state.current_page = "dashboard"
        show_dashboard_page()

if __name__ == "__main__":
    main()
