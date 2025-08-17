#!/usr/bin/env python3
"""
Development server runner for Restaurant Ingredient Tracker Flask Edition.
"""

import os
from app import app

if __name__ == '__main__':
    # Development configuration
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("🍽️ Restaurant Ingredient Tracker - Flask Edition")
    print("=" * 50)
    print(f"🌐 Server: http://localhost:{port}")
    print("👤 Demo accounts: admin/admin123, manager/manager456, staff/staff789")
    print("📁 Upload CSV files or use sample data to get started")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=port, debug=debug)