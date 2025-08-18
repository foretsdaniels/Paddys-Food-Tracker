#!/usr/bin/env python3
"""Debug session persistence issue."""

import requests
import json

def debug_session():
    """Debug session persistence."""
    session = requests.Session()
    
    # Login
    login_response = session.post('http://localhost:5000/login', data={
        'username': 'admin',
        'password': 'admin123'
    })
    print(f"Login status: {login_response.status_code}")
    print(f"Login cookies: {list(session.cookies.keys())}")
    
    # Load sample data
    sample_response = session.get('http://localhost:5000/sample-data')
    print(f"Sample data status: {sample_response.status_code}")
    print(f"Sample cookies after: {list(session.cookies.keys())}")
    
    # Check analytics
    analytics_response = session.get('http://localhost:5000/analytics')
    print(f"Analytics status: {analytics_response.status_code}")
    
    # Check Excel export
    excel_response = session.get('http://localhost:5000/export/excel')
    print(f"Excel status: {excel_response.status_code}")
    
    if excel_response.status_code == 200:
        print(f"Excel size: {len(excel_response.content)} bytes")
        print("SUCCESS: Excel export working!")
    else:
        print("FAILED: Excel export redirecting")

if __name__ == '__main__':
    debug_session()