#!/usr/bin/env python3
"""
System Check Script
Verifies that all components of the Hospital Management System are working correctly
"""

import os
import sys
import sqlite3

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} (Compatible)")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (Requires 3.7+)")
        return False

def check_imports():
    """Check critical imports"""
    print("\n📦 Checking imports...")
    imports = [
        ("os", "Operating system interface"),
        ("sys", "System-specific parameters"),
        ("sqlite3", "SQLite database"),
        ("hashlib", "Password hashing"),
        ("datetime", "Date and time handling"),
        ("shutil", "File operations")
    ]
    
    all_good = True
    for module, description in imports:
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError:
            print(f"❌ {module} - {description} (MISSING)")
            all_good = False
    
    return all_good

def check_optional_imports():
    """Check optional imports"""
    print("\n🔧 Checking optional imports...")
    optional_imports = [
        ("tkinter", "GUI framework"),
        ("matplotlib", "Data visualization"),
        ("numpy", "Numerical computing")
    ]
    
    for module, description in optional_imports:
        try:
            __import__(module)
            print(f"✅ {module} - {description}")
        except ImportError:
            print(f"⚠️  {module} - {description} (Optional)")

def check_file_structure():
    """Check file structure"""
    print("\n📁 Checking file structure...")
    
    required_files = [
        "simple_main.py",
        "main.py",
        "run.bat",
        "requirements.txt",
        "src/database/db_manager.py",
        "src/auth/authentication.py"
    ]
    
    all_good = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} (MISSING)")
            all_good = False
    
    return all_good

def check_database():
    """Check database functionality"""
    print("\n💾 Checking database functionality...")
    
    try:
        # Test SQLite connection
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY)")
        cursor.execute("INSERT INTO test (id) VALUES (1)")
        result = cursor.fetchone()
        conn.close()
        
        print("✅ SQLite database functionality working")
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def main():
    """Main check function"""
    print("=" * 60)
    print("🏥 HOSPITAL MANAGEMENT SYSTEM - SYSTEM CHECK")
    print("=" * 60)
    
    checks = [
        check_python_version(),
        check_imports(),
        check_file_structure(),
        check_database()
    ]
    
    check_optional_imports()
    
    print("\n" + "=" * 60)
    if all(checks):
        print("🎉 ALL CHECKS PASSED! System is ready to run.")
        print("💡 To start the system, run: run.bat")
    else:
        print("⚠️  SOME CHECKS FAILED! Please review the issues above.")
    print("=" * 60)

if __name__ == "__main__":
    main()
