@echo off
title Sempra Data Migration Platform - One Click Launcher
color 0b
echo ===============================================================================
echo   SEMPRA ENERGY - SAP DATA MIGRATION RECONCILIATION COCKPIT
echo   Automated Setup ^& Launcher for New Systems
echo ===============================================================================
echo.

:: 1. Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    echo Make sure to check 'Add Python to PATH' during installation.
    pause
    exit /b 1
)

echo [1/3] Python detected successfully.
echo.

:: 2. Install Dependencies
echo [2/3] Checking and installing required packages...
pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo [WARN] Fast pip install failed. Retrying with standard install...
    pip install flask flask-cors openpyxl pandas xlrd reportlab python-docx
)
echo [2/3] Dependencies verified.
echo.

:: 3. Launch Platform
echo [3/3] Launching Background File Watcher Bridge ^& Master Dashboard...
python launch_dashboard.py

pause
