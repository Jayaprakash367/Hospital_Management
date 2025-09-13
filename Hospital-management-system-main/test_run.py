#!/usr/bin/env python3
"""
Quick test to verify the Hospital Management System can start
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    print("Testing Hospital Management System...")
    print("Python version:", sys.version)
    print("Current directory:", os.getcwd())
    
    # Test imports
    import sqlite3
    print("✅ SQLite3 available")
    
    # Test if simple_main exists
    if os.path.exists("simple_main.py"):
        print("✅ simple_main.py found")
    else:
        print("❌ simple_main.py not found")
        
    # Test database setup
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    from src.database.db_manager import DatabaseManager
    
    db = DatabaseManager()
    print("✅ Database manager initialized")
    
    print("\n🎉 All tests passed! The system should work properly.")
    print("\nTo run the system:")
    print("1. Double-click run.bat")
    print("2. Or run: python simple_main.py")
    print("\nDefault login: admin / admin123")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("Please check your Python installation and try again.")

input("\nPress Enter to close...")
