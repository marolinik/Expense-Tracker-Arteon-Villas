#!/usr/bin/env bash
# Build script for Render
# This script is executed during the build process on Render

set -o errexit

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run database initialization
python init_db.py 