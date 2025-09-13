#!/usr/bin/env python3
"""
Test script for Hospital Management System
Verifies all imports and basic functionality
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test all required imports"""
    try:
        print("Testing imports...")
        
        # Test database module
        from src.database.db_manager import DatabaseManager
        print("✓ Database manager imported")
        
        # Test authentication
        from src.auth.authentication import AuthenticationManager
        print("✓ Authentication manager imported")
        
        # Test GUI modules
        from src.gui.login_window import LoginWindow
        print("✓ Login window imported")
        
        from src.gui.main_window import MainWindow
        print("✓ Main window imported")
        
        # Test utilities
        from src.utils.config import Config
        print("✓ Config imported")
        
        print("\n✅ All imports successful!")
        return True
        
    except ImportError as e:
        print(f"\n❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

def test_database():
    """Test database functionality"""
    try:
        print("\nTesting database...")
        
        from src.database.db_manager import DatabaseManager
        
        # Create database manager
        db = DatabaseManager("test_hospital.db")
        print("✓ Database manager created")
        
        # Create tables
        db.create_tables()
        print("✓ Database tables created")
        
        # Create default admin
        db.create_default_admin()
        print("✓ Default admin created")
        
        # Test query
        users = db.execute_query("SELECT COUNT(*) as count FROM users")
        print(f"✓ Database query successful - {users[0]['count']} users found")
        
        # Clean up
        db.close()
        os.remove("test_hospital.db")
        print("✓ Test database cleaned up")
        
        print("\n✅ Database tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Database test error: {e}")
        return False

def test_authentication():
    """Test authentication functionality"""
    try:
        print("\nTesting authentication...")
        
        from src.database.db_manager import DatabaseManager
        from src.auth.authentication import AuthenticationManager
        
        # Create test database
        db = DatabaseManager("test_auth.db")
        db.create_tables()
        db.create_default_admin()
        
        # Create auth manager
        auth = AuthenticationManager(db)
        print("✓ Authentication manager created")
        
        # Test login
        user = auth.authenticate("admin", "admin123")
        if user:
            print("✓ Default admin login successful")
        else:
            print("❌ Default admin login failed")
            return False
            
        # Test invalid login
        invalid_user = auth.authenticate("invalid", "password")
        if not invalid_user:
            print("✓ Invalid login correctly rejected")
        else:
            print("❌ Invalid login incorrectly accepted")
            return False
            
        # Clean up
        db.close()
        os.remove("test_auth.db")
        print("✓ Test database cleaned up")
        
        print("\n✅ Authentication tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Authentication test error: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Hospital Management System - Test Suite")
    print("=" * 50)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
        
    # Test database
    if not test_database():
        all_passed = False
        
    # Test authentication
    if not test_authentication():
        all_passed = False
        
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED! System is ready to use.")
        print("\nTo start the application:")
        print("1. Run: python main.py")
        print("2. Or double-click: run.bat")
        print("\nDefault login: admin / admin123")
    else:
        print("❌ SOME TESTS FAILED! Please check the errors above.")
        
    print("=" * 50)

if __name__ == "__main__":
    main()
