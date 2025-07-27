#!/bin/bash
echo "======================================"
echo " Logstash Pipeline Formatter Builder"
echo "======================================"
echo

echo "Installing build dependencies..."
pip3 install -r requirements-build.txt

echo
echo "Building executable..."
python3 build_executable.py

echo
echo "Build process completed!"
