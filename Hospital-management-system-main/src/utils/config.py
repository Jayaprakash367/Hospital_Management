"""
Configuration settings for Hospital Management System
"""

import os
from datetime import timedelta

class Config:
    def __init__(self):
        # Database configuration
        self.DATABASE_PATH = "data/hospital.db"
        self.BACKUP_PATH = "data/backups/"
        
        # Security settings
        self.SESSION_TIMEOUT = timedelta(hours=8)
        self.PASSWORD_MIN_LENGTH = 6
        self.MAX_LOGIN_ATTEMPTS = 3
        
        # Application settings
        self.APP_NAME = "Hospital Management System"
        self.APP_VERSION = "2.0"
        self.COMPANY_NAME = "HealthCare Solutions Inc."
        
        # UI settings
        self.WINDOW_WIDTH = 1400
        self.WINDOW_HEIGHT = 900
        self.THEME = "modern"
        
        # Colors
        self.COLORS = {
            'primary': '#3498db',
            'secondary': '#2c3e50',
            'success': '#27ae60',
            'warning': '#f39c12',
            'danger': '#e74c3c',
            'info': '#17a2b8',
            'light': '#f8f9fa',
            'dark': '#343a40',
            'background': '#ecf0f1',
            'text': '#2c3e50'
        }
        
        # Default settings
        self.DEFAULT_APPOINTMENT_DURATION = 30  # minutes
        self.WORKING_HOURS_START = "08:00"
        self.WORKING_HOURS_END = "18:00"
        
        # File paths
        self.LOGS_PATH = "logs/"
        self.REPORTS_PATH = "reports/"
        self.TEMP_PATH = "temp/"
        
        # Ensure directories exist
        self.ensure_directories()
        
    def ensure_directories(self):
        """Create necessary directories if they don't exist"""
        directories = [
            os.path.dirname(self.DATABASE_PATH),
            self.BACKUP_PATH,
            self.LOGS_PATH,
            self.REPORTS_PATH,
            self.TEMP_PATH
        ]
        
        for directory in directories:
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
                
    def get_connection_string(self):
        """Get database connection string"""
        return self.DATABASE_PATH
        
    def get_backup_filename(self):
        """Generate backup filename with timestamp"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{self.BACKUP_PATH}hospital_backup_{timestamp}.db"
