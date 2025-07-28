@echo off
echo ============================================================
echo Logstash Pipeline Formatter - Installatie
echo ============================================================
echo.

REM Check if Python is available
echo Controleren van Python installatie...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python niet gevonden met 'python' commando. Proberen met 'py'...
    py --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo.
        echo FOUT: Python is niet geinstalleerd of niet in PATH
        echo.
        echo Instructies:
        echo 1. Download Python 3.7+ van https://www.python.org/downloads/
        echo 2. Installeer Python en zorg dat "Add Python to PATH" is aangevinkt
        echo 3. Herstart deze computer
        echo 4. Probeer deze installatie opnieuw
        echo.
        pause
        exit /b 1
    )
    set PYTHON_CMD=py
) else (
    set PYTHON_CMD=python
)

echo Python gevonden: %PYTHON_CMD%
%PYTHON_CMD% --version

echo.
echo Installeren van vereiste packages...
echo Dit kan enkele minuten duren...
echo.

%PYTHON_CMD% -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo Waarschuwing: Pip upgrade mislukt, proberen zonder upgrade...
)

%PYTHON_CMD% -m pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo.
    echo FOUT: Package installatie mislukt!
    echo.
    echo Mogelijke oplossingen:
    echo 1. Controleer internetverbinding
    echo 2. Probeer als Administrator uit te voeren
    echo 3. Contacteer IT support
    echo.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Installatie succesvol voltooid!
echo ============================================================
echo.
echo Om de applicatie te starten:
echo 1. Dubbelklik op 'start_app.bat', OF
echo 2. Run via command line: %PYTHON_CMD% app.py
echo.
echo De applicatie zal automatisch uw browser openen op:
echo http://localhost:5001
echo.
pause
