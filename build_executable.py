#!/usr/bin/env python3
"""
Build script for Logstash Pipeline Formatter
Creates a standalone executable using PyInstaller
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def build_executable():
    """Build the standalone executable"""
    print("Building Logstash Pipeline Formatter executable...")
    
    # Define paths
    script_dir = Path(__file__).parent
    app_file = script_dir / "app.py"
    build_dir = script_dir / "build"
    dist_dir = script_dir / "dist"
    
    # Clean previous builds
    if build_dir.exists():
        shutil.rmtree(build_dir)
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    
    # PyInstaller command
    separator = ";" if sys.platform.startswith('win') else ":"
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",                    # Single executable
        "--windowed",                   # No console window (for Windows)
        "--name=LogstashPipelineFormatter",
        f"--add-data=templates{separator}templates",
        f"--add-data=static{separator}static",
        f"--add-data=utils{separator}utils",
        "--hidden-import=werkzeug.security",
        "--hidden-import=jinja2",
        "--hidden-import=flask",
        str(app_file)
    ]
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        subprocess.run(cmd, check=True, cwd=script_dir)
        print("Build completed successfully!")
        
        # Check if executable was created
        exe_name = "LogstashPipelineFormatter.exe" if sys.platform.startswith('win') else "LogstashPipelineFormatter"
        exe_path = dist_dir / exe_name
        
        if exe_path.exists():
            print(f"Executable created: {exe_path}")
            print(f"File size: {exe_path.stat().st_size / 1024 / 1024:.1f} MB")
        else:
            print("Executable not found!")
            
    except subprocess.CalledProcessError as e:
        print(f"Build failed: {e}")
        return False
    
    return True

def create_distribution_package():
    """Create a complete distribution package"""
    print("Creating distribution package...")
    
    script_dir = Path(__file__).parent
    dist_dir = script_dir / "dist"
    package_dir = script_dir / "LogstashPipelineFormatter_Distribution"
    
    # Clean and create package directory
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    # Copy executable
    exe_name = "LogstashPipelineFormatter.exe" if sys.platform.startswith('win') else "LogstashPipelineFormatter"
    exe_path = dist_dir / exe_name
    
    if exe_path.exists():
        shutil.copy2(exe_path, package_dir)
        print(f"Copied executable to package")
    
    # Create README for distribution
    readme_content = """# Logstash Pipeline Formatter

## Installation & Usage

1. Extract this zip file to any folder
2. Double-click `LogstashPipelineFormatter.exe` to start the application
3. Your default browser will open automatically
4. Use the web interface to format and validate your Logstash pipeline files
5. Click the "✕ Close Application" button in the top-right corner to exit

## Features

- ✅ Automatic syntax error detection and fixing
- ✅ Quote validation and correction
- ✅ Brace matching and auto-completion
- ✅ Whitespace cleanup
- ✅ Pipeline structure validation
- ✅ Support for file upload and direct text input

## System Requirements

- Windows 7 or later
- No additional software installation required
- Modern web browser (Chrome, Firefox, Edge)

## Troubleshooting

If the application doesn't start:
1. Make sure no antivirus is blocking the executable
2. Run as administrator if needed
3. Check Windows Defender/Security settings

## Version Info

Built with PyInstaller for standalone deployment.
All dependencies are bundled within the executable.
"""
    
    (package_dir / "README.txt").write_text(readme_content)
    print("Created README.txt")
    
    # Create batch file for easy startup (Windows)
    if sys.platform.startswith('win'):
        batch_content = """@echo off
echo Starting Logstash Pipeline Formatter...
LogstashPipelineFormatter.exe
pause"""
        (package_dir / "Start_LogstashFormatter.bat").write_text(batch_content)
        print("Created startup batch file")
    
    print(f"Distribution package created in: {package_dir}")
    
    # Create zip file
    zip_path = script_dir / "LogstashPipelineFormatter_Portable"
    shutil.make_archive(str(zip_path), 'zip', package_dir)
    print(f"Zip file created: {zip_path}.zip")

if __name__ == "__main__":
    print("=" * 60)
    print("    Logstash Pipeline Formatter - Build Script")
    print("=" * 60)
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print(f"PyInstaller found: {PyInstaller.__version__}")
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("PyInstaller installed")
    
    # Build executable
    if build_executable():
        create_distribution_package()
        print("\nBuild process completed successfully!")
        print("Ready for distribution: LogstashPipelineFormatter_Portable.zip")
    else:
        print("\nBuild process failed!")
        sys.exit(1)
