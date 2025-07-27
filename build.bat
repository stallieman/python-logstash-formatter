@echo off
echo ======================================
echo  Logstash Pipeline Formatter Builder
echo ======================================
echo.

echo Installing build dependencies...
pip install -r requirements-build.txt

echo.
echo Building executable...
python build_executable.py

echo.
echo Build process completed!
pause
