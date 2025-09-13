#!/usr/bin/env python3
"""
Advanced Hospital Management System
Created by: Hospital Management Team
Version: 2.0
Features: Patient Management, Doctor Management, Appointments, Billing, Reports
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta
import os
import sys

# Import custom modules
from src.database.db_manager import DatabaseManager
from src.gui.main_window import MainWindow
from src.utils.config import Config
from src.auth.authentication import AuthenticationManager

class HospitalManagementSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Hospital Management System v2.0")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize components
        self.db_manager = DatabaseManager()
        self.auth_manager = AuthenticationManager(self.db_manager)
        self.config = Config()
        
        # Create database tables
        self.setup_database()
        
        # Initialize GUI
        self.init_gui()
        
    def setup_database(self):
        """Initialize database with required tables"""
        self.db_manager.create_tables()
        self.db_manager.create_default_admin()
        
    def init_gui(self):
        """Initialize the main GUI"""
        # Apply modern theme
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'), foreground='#34495e')
        
        # Show login window first
        self.show_login()
        
    def show_login(self):
        """Display login window"""
        from src.gui.login_window import LoginWindow
        login_window = LoginWindow(self.root, self.auth_manager, self.on_login_success)
        
    def on_login_success(self, user_data):
        """Handle successful login"""
        self.current_user = user_data
        self.main_window = MainWindow(self.root, self.db_manager, self.current_user)
        
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            self.db_manager.close()

if __name__ == "__main__":
    app = HospitalManagementSystem()
    app.run()
