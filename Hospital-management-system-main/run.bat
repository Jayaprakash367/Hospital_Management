@echo off
title Hospital Management System v2.0
echo.
echo ========================================
echo    Hospital Management System v2.0
echo         Starting Application...
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
python -c "import sqlite3" >nul 2>&1
if errorlevel 1 (
    echo ERROR: sqlite3 is not available
    echo Please ensure Python was installed with sqlite3 support
    pause
    exit /b 1
)

REM Install requirements if needed
if exist requirements.txt (
    echo Installing/updating dependencies...
    pip install -r requirements.txt --quiet
)

REM Start the application
echo.
echo Starting Hospital Management System...
echo.
echo Default Login Credentials:
echo Username: admin
echo Password: admin123
echo.
echo NOTE: This is a CONSOLE APPLICATION (not a webpage)
echo All interactions happen in this console window.
echo.

python simple_main.py

REM If default python doesn't work, try with virtual environment
if errorlevel 1 (
    echo Trying with virtual environment...
    d:/Hospital-management-system/.venv/Scripts/python.exe simple_main.py
)

if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start
    echo.
    echo Troubleshooting options:
    echo 1. Run: python test_system.py    (Test core functions)
    echo 2. Run: python diagnose.py      (Detailed diagnostics)
    echo 3. Check console output for error details
    echo.
    pause
)

echo.
echo Application closed.
pause
