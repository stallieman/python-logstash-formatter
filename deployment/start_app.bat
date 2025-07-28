@echo off
echo Starting Logstash Pipeline Formatter...
echo.
echo This will start the web application on http://localhost:5001
echo Press Ctrl+C to stop the application
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python not found with 'python' command. Trying 'py'...
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo ERROR: Python is not installed or not in PATH
        echo Please install Python 3.7+ and try again
        pause
        exit /b 1
    )
    echo Starting with 'py' command...
    py app.py
) else (
    echo Starting with 'python' command...
    python app.py
)

pause
