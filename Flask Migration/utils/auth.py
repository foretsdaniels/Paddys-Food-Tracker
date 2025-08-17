"""
Authentication utilities for the Restaurant Ingredient Tracker.
"""

import os
from werkzeug.security import check_password_hash, generate_password_hash


class AuthManager:
    """Handles user authentication and authorization."""
    
    def __init__(self):
        """Initialize authentication manager with demo accounts."""
        # Demo accounts for testing
        self.demo_users = {
            'admin': {
                'password_hash': generate_password_hash('admin123'),
                'role': 'admin'
            },
            'manager': {
                'password_hash': generate_password_hash('manager456'),
                'role': 'manager'
            },
            'staff': {
                'password_hash': generate_password_hash('staff789'),
                'role': 'staff'
            }
        }
        
        # Check if running in Replit environment
        self.is_replit = bool(os.environ.get('REPL_ID'))
        
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate user credentials."""
        if self.is_replit:
            # In Replit, check for Replit Auth headers
            replit_user = os.environ.get('REPLIT_USER_NAME')
            if replit_user and username == replit_user:
                return True
        
        # Fallback to demo accounts
        if username in self.demo_users:
            return check_password_hash(self.demo_users[username]['password_hash'], password)
        
        return False
    
    def get_user_role(self, username: str) -> str:
        """Get user role."""
        if self.is_replit:
            # In Replit, all authenticated users are admins
            return 'admin'
        
        if username in self.demo_users:
            return self.demo_users[username]['role']
        
        return 'user'
    
    def is_admin(self, username: str) -> bool:
        """Check if user is admin."""
        return self.get_user_role(username) == 'admin'
    
    def is_manager_or_above(self, username: str) -> bool:
        """Check if user is manager or admin."""
        role = self.get_user_role(username)
        return role in ['admin', 'manager']