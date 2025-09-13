"""
Authentication Manager for Hospital Management System
Handles user login, logout, and session management
"""

import hashlib
from datetime import datetime, timedelta

class AuthenticationManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.current_user = None
        self.session_timeout = timedelta(hours=8)
        
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
        
    def authenticate(self, username, password):
        """Authenticate user credentials"""
        password_hash = self.hash_password(password)
        
        query = '''
            SELECT user_id, username, role, full_name, email, phone, is_active
            FROM users 
            WHERE username = ? AND password_hash = ? AND is_active = 1
        '''
        
        result = self.db_manager.execute_query(query, (username, password_hash))
        
        if result:
            user_data = dict(result[0])
            user_data['login_time'] = datetime.now()
            self.current_user = user_data
            return user_data
        return None
        
    def create_user(self, username, password, role, full_name, email=None, phone=None):
        """Create a new user account"""
        password_hash = self.hash_password(password)
        
        query = '''
            INSERT INTO users (username, password_hash, role, full_name, email, phone)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        
        try:
            user_id = self.db_manager.execute_insert(
                query, (username, password_hash, role, full_name, email, phone)
            )
            return user_id
        except Exception as e:
            return None
            
    def change_password(self, user_id, old_password, new_password):
        """Change user password"""
        old_hash = self.hash_password(old_password)
        new_hash = self.hash_password(new_password)
        
        # Verify old password
        query = "SELECT user_id FROM users WHERE user_id = ? AND password_hash = ?"
        result = self.db_manager.execute_query(query, (user_id, old_hash))
        
        if not result:
            return False
            
        # Update password
        update_query = "UPDATE users SET password_hash = ? WHERE user_id = ?"
        rows_affected = self.db_manager.execute_update(update_query, (new_hash, user_id))
        
        return rows_affected > 0
        
    def is_session_valid(self):
        """Check if current session is still valid"""
        if not self.current_user:
            return False
            
        login_time = self.current_user.get('login_time')
        if not login_time:
            return False
            
        return datetime.now() - login_time < self.session_timeout
        
    def logout(self):
        """Logout current user"""
        self.current_user = None
        
    def get_current_user(self):
        """Get current logged in user"""
        if self.is_session_valid():
            return self.current_user
        return None
        
    def has_permission(self, required_role):
        """Check if current user has required role"""
        if not self.current_user:
            return False
            
        user_role = self.current_user.get('role', '').lower()
        required_role = required_role.lower()
        
        # Role hierarchy: admin > doctor > nurse > staff > user
        role_levels = {
            'admin': 5,
            'doctor': 4, 
            'nurse': 3,
            'staff': 2,
            'user': 1
        }
        
        user_level = role_levels.get(user_role, 0)
        required_level = role_levels.get(required_role, 0)
        
        return user_level >= required_level
