#!/bin/bash

# ==================================================
# Program Name: install.sh
# Description:
#     This script allows to verify if the relevant python packages
#     are correctly installed on the Raspberry Pi.
#
# Author: JB LAFFOSSE
# Date: 2024-09-08
# Version: 1.0.0
# License: None
# ==================================================

# ==================================================
# Constants
# ==================================================

# List of Python packages to check
REQUIRED_PACKAGES=(
    "time"
    "board"
    "adafruit_ahtx0"
    "adafruit_tsl2591"
    "flask"
    "flask_sqlalchemy"
    "flask_migrate "
)

# Python interpreter (change to python3 if needed)
PYTHON="python3"

# Pip interpreter
PIP="pip3"

# ==================================================
# Functions
# ==================================================

# Function to check if a Python package is installed
check_package() {
    package=$1
    echo "Checking for $package..."
    $PYTHON -c "import $package" 2>/dev/null

    if [ $? -eq 0 ]; then
        echo "[OK] $package is correctly installed."
    else
        echo "[WARNING] $package is NOT installed. Try to install the package..."
        
        $PIP install $package 2>/dev/null
        if [ $? -eq 0 ]; then
            echo "[OK] $package has been successfully installed!"
        else
            echo "[ERROR] An error occurs during the installation of $package... Please retry manually..."
        fi
        #echo "You can install it using: pip install $package"
    fi
}

# ==================================================
# Main script
# ==================================================

echo "Starting Python package check..."
for package in "${REQUIRED_PACKAGES[@]}"; do
    echo "################"
    check_package $package
done

echo "################"
echo "Package check complete."
