#!/usr/bin/env python3
"""
Restaurant Ingredient Tracker - Flask Web Application
A web-based application for tracking restaurant ingredient usage, waste, and costs.
"""

import os
import io
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify, send_file, make_response
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash

# Import report generation modules
from reports.pdf_generator import PDFReportGenerator
from reports.excel_generator import ExcelReportGenerator
from utils.data_processor import DataProcessor
from utils.auth import AuthManager

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')

# Configuration
UPLOAD_FOLDER = 'uploads'
EXPORT_FOLDER = 'exports'
ALLOWED_EXTENSIONS = {'csv'}

# Ensure directories exist
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
Path(EXPORT_FOLDER).mkdir(exist_ok=True)

# Initialize components
auth_manager = AuthManager()
data_processor = DataProcessor()
pdf_generator = PDFReportGenerator()
excel_generator = ExcelReportGenerator()

def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def normalize_sort_column(sort_param):
    """Normalize sort parameter to actual column name."""
    column_mapping = {
        'shrinkage_cost': 'Shrinkage Cost',
        'total_cost': 'Total Cost',
        'waste_cost': 'Waste Cost',
        'used_cost': 'Used Cost',
        'waste_percentage': 'Waste %',
        'shrinkage_percentage': 'Shrinkage %',
        'received_qty': 'Received Qty',
        'used_qty': 'Used Qty',
        'wasted_qty': 'Wasted Qty',
        'ingredient': 'Ingredient',
        'unit_cost': 'Unit Cost'
    }
    return column_mapping.get(sort_param, sort_param)

@app.route('/')
def index():
    """Landing page."""
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if auth_manager.authenticate(username, password):
            session['username'] = username
            session['user_role'] = auth_manager.get_user_role(username)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """User logout."""
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/upload', methods=['GET', 'POST'])
def upload_files():
    """File upload page for CSV data."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        files = {}
        required_files = ['ingredient_info', 'input_stock', 'usage', 'waste']
        
        # Check all required files are uploaded
        for file_type in required_files:
            if file_type not in request.files or request.files[file_type].filename == '':
                flash(f'Missing {file_type.replace("_", " ").title()} file', 'error')
                return redirect(request.url)
            
            file = request.files[file_type]
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                safe_filename = f"{file_type}_{timestamp}_{filename}"
                file_path = os.path.join(UPLOAD_FOLDER, safe_filename)
                file.save(file_path)
                files[file_type] = file_path
            else:
                flash(f'Invalid file type for {file_type}. Please upload CSV files only.', 'error')
                return redirect(request.url)
        
        # Process the uploaded files
        try:
            results = data_processor.process_files(files)
            session['current_results'] = results.to_json(orient='records')
            session['upload_timestamp'] = datetime.now().isoformat()
            flash('Files processed successfully!', 'success')
            return redirect(url_for('analytics'))
        except Exception as e:
            flash(f'Error processing files: {str(e)}', 'error')
            return redirect(request.url)
    
    return render_template('upload.html')

@app.route('/analytics')
def analytics():
    """Analytics page showing processed results."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if 'current_results' not in session:
        flash('No data available. Please upload CSV files first.', 'warning')
        return redirect(url_for('upload_files'))
    
    # Load results from session
    results = pd.read_json(session['current_results'], orient='records')
    
    # Apply filters if any
    filter_type = request.args.get('filter', 'all')
    sort_by_param = request.args.get('sort', 'shrinkage_cost')
    sort_by = normalize_sort_column(sort_by_param)
    sort_order = request.args.get('order', 'desc')
    
    filtered_results = data_processor.apply_filters(results, filter_type)
    sorted_results = data_processor.sort_results(filtered_results, sort_by, sort_order)
    
    # Calculate summary statistics
    summary_stats = data_processor.calculate_summary_stats(sorted_results)
    
    # Get alerts and insights
    alerts = data_processor.get_alerts(sorted_results)
    insights = data_processor.get_insights(sorted_results)
    
    return render_template('analytics.html', 
                         results=sorted_results.to_dict('records'),
                         summary_stats=summary_stats,
                         alerts=alerts,
                         insights=insights,
                         current_filter=filter_type,
                         current_sort=sort_by_param,
                         current_order=sort_order)

@app.route('/reports')
def reports():
    """Reports page for generating PDF and Excel exports."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if 'current_results' not in session:
        flash('No data available. Please upload CSV files first.', 'warning')
        return redirect(url_for('upload_files'))
    
    return render_template('reports.html')

@app.route('/export/pdf')
def export_pdf():
    """Generate and download PDF report."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if 'current_results' not in session:
        flash('No data available. Please upload CSV files first.', 'warning')
        return redirect(url_for('upload_files'))
    
    try:
        results = pd.read_json(session['current_results'], orient='records')
        summary_stats = data_processor.calculate_summary_stats(results)
        
        # Generate PDF
        pdf_buffer = pdf_generator.generate_report(results, summary_stats, session['username'])
        
        # Create response
        response = make_response(pdf_buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = f'attachment; filename=ingredient_tracker_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.pdf'
        
        return response
    except Exception as e:
        flash(f'Error generating PDF: {str(e)}', 'error')
        return redirect(url_for('reports'))

@app.route('/export/excel')
def export_excel():
    """Generate and download Excel report."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if 'current_results' not in session:
        flash('No data available. Please upload CSV files first.', 'warning')
        return redirect(url_for('upload_files'))
    
    try:
        results = pd.read_json(session['current_results'], orient='records')
        summary_stats = data_processor.calculate_summary_stats(results)
        insights = data_processor.get_insights(results)
        
        # Generate Excel
        excel_buffer = excel_generator.generate_report(results, summary_stats, insights, session['username'])
        
        # Create response
        response = make_response(excel_buffer.getvalue())
        response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        response.headers['Content-Disposition'] = f'attachment; filename=ingredient_tracker_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        
        return response
    except Exception as e:
        flash(f'Error generating Excel: {str(e)}', 'error')
        return redirect(url_for('reports'))

@app.route('/sample-data')
def sample_data():
    """Load sample data for testing."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    try:
        # Load sample data from the Flask Migration directory
        sample_files = {
            'ingredient_info': 'sample_ingredient_info.csv',
            'input_stock': 'sample_input_stock.csv', 
            'usage': 'sample_usage.csv',
            'waste': 'sample_waste.csv'
        }
        
        # Verify all sample files exist
        for file_type, filename in sample_files.items():
            if not os.path.exists(filename):
                raise FileNotFoundError(f"Sample file not found: {filename}")
        
        results = data_processor.process_files(sample_files)
        session['current_results'] = results.to_json(orient='records')
        session['upload_timestamp'] = datetime.now().isoformat()
        flash('Sample data loaded successfully!', 'success')
        return redirect(url_for('analytics'))
    except Exception as e:
        flash(f'Error loading sample data: {str(e)}', 'error')
        return redirect(url_for('upload_files'))

@app.route('/api/data')
def api_data():
    """API endpoint to get current data as JSON."""
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    if 'current_results' not in session:
        return jsonify({'error': 'No data available'}), 404
    
    results = pd.read_json(session['current_results'], orient='records')
    return jsonify(results.to_dict('records'))

@app.route('/settings')
def settings():
    """Settings page."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    return render_template('settings.html', 
                         username=session['username'],
                         user_role=session.get('user_role', 'user'))

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors."""
    return render_template('error.html', error_code=404, error_message="Page not found"), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return render_template('error.html', error_code=500, error_message="Internal server error"), 500

if __name__ == '__main__':
    # Development server
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    app.run(host='0.0.0.0', port=port, debug=debug)