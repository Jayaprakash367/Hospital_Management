
"""
Simple diagnostic script to identify GUI issues
"""

import sys
import os

def test_basic_imports():
    """Test basic Python imports"""
    print("Testing basic imports...")
    
    try:
        import tkinter as tk
        print("✓ tkinter imported successfully")
        
        # Test tkinter window creation
        root = tk.Tk()
        root.withdraw()  # Hide the test window
        print("✓ tkinter window creation works")
        root.destroy()
        
    except ImportError as e:
        print(f"❌ tkinter import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ tkinter test failed: {e}")
        return False
        
    try:
        import sqlite3
        print("✓ sqlite3 imported successfully")
    except ImportError as e:
        print(f"❌ sqlite3 import failed: {e}")
        return False
        
    return True

def test_project_imports():
    """Test project-specific imports"""
    print("\nTesting project imports...")
    
    # Add src to path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    try:
        from src.database.db_manager import DatabaseManager
        print("✓ DatabaseManager imported")
        
        from src.auth.authentication import AuthenticationManager
        print("✓ AuthenticationManager imported")
        
        from src.utils.config import Config
        print("✓ Config imported")
        
        return True
        
    except Exception as e:
        print(f"❌ Project import failed: {e}")
        return False

def test_gui_imports():
    """Test GUI imports"""
    print("\nTesting GUI imports...")
    
    try:
        from src.gui.login_window import LoginWindow
        print("✓ LoginWindow imported")
        
        from src.gui.main_window import MainWindow
        print("✓ MainWindow imported")
        
        return True
        
    except Exception as e:
        print(f"❌ GUI import failed: {e}")
        print(f"Error details: {str(e)}")
        return False

def test_database_creation():
    """Test database creation"""
    print("\nTesting database creation...")
    
    try:
        from src.database.db_manager import DatabaseManager
        
        # Create test database
        db = DatabaseManager("test_diagnostic.db")
        db.create_tables()
        print("✓ Database tables created")
        
        db.create_default_admin()
        print("✓ Default admin created")
        
        # Test query
        users = db.execute_query("SELECT COUNT(*) as count FROM users")
        print(f"✓ Database query works - found {users[0]['count']} users")
        
        # Cleanup
        db.close()
        if os.path.exists("test_diagnostic.db"):
            os.remove("test_diagnostic.db")
        print("✓ Database test completed")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def main():
    """Run all diagnostic tests"""
    print("=" * 60)
    print("HOSPITAL MANAGEMENT SYSTEM - DIAGNOSTIC TOOL")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Test basic imports
    if not test_basic_imports():
        all_tests_passed = False
        
    # Test project imports
    if not test_project_imports():
        all_tests_passed = False
        
    # Test GUI imports
    if not test_gui_imports():
        all_tests_passed = False
        
    # Test database
    if not test_database_creation():
        all_tests_passed = False
        
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 ALL TESTS PASSED!")
        print("Your system should work correctly.")
        print("\nTry running: python main.py")
        print("If the GUI still doesn't open, there may be a display issue.")
    else:
        print("❌ SOME TESTS FAILED!")
        print("Please check the errors above and fix the issues.")
        
    print("=" * 60)
    
    # Try to start a simple GUI test
    if all_tests_passed:
        print("\nTesting simple GUI window...")
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.title("HMS Diagnostic Test")
            root.geometry("400x200")
            
            tk.Label(
                root, 
                text="Hospital Management System\nDiagnostic Test Window",
                font=('Arial', 12),
                pady=20
            ).pack()
            
            tk.Button(
                root,
                text="Close Test Window",
                command=root.destroy,
                bg='#3498db',
                fg='white',
                padx=20,
                pady=10
            ).pack(pady=20)
            
            print("✓ Test GUI window created successfully!")
            print("If you can see a test window, your GUI is working.")
            print("Close the test window and try running: python main.py")
            
            root.mainloop()
            
        except Exception as e:
            print(f"❌ GUI test failed: {e}")

if __name__ == "__main__":
    main()
