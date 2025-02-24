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
    "flask_migrate"
    "sqlalchemy_utils"
)

# Python interpreter (change to python3 if needed)
PYTHON="python3"

# Pip interpreter
PIP="pip3"

# Requirements file defining all the python packages required
REQUIREMENTS_FILE="../requirements.txt"

# ==================================================
# Functions
# ==================================================

# Function to check if a Python package is installed
check_package() {
    package=$1
    echo "[INFO] Checking for $package..."
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

# First, verify if python3 is correctly installed
echo "################"
echo "[INFO] Verify if python3 is installed..."
$PYTHON --version
if [ $? -eq 0 ]; then
    echo "[OK] python3 is correctly installed!"
else
    echo "[ERROR] Please install python3 with the following command:"
    echo "[ERROR] apt install python3"
    echo "[ERROR] exit..."
    exit 3
fi


# Then, install/check dependencies for AHT20 and TSL2591
# as they need to be installed differently from others
# python packages
echo "################"
echo "[INFO] Install Package related to AHT20..."
$PIP install adafruit-circuitpython-ahtx0 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "[OK] Package related to AHT20 is correctly installed!"
else
    echo "[ERROR] An error occurs during the installation of the package for ahtx0..."
    echo "[ERROR] Please try again... exit..."
    exit 5
fi

echo "################"
echo "[INFO] Install Package related to TSL2591..."
$PIP install adafruit-circuitpython-tsl2591 > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "[OK] Package related to TSL2591 is correctly installed!"
else
    echo "[ERROR] An error occurs during the installation of the package for tsl2591..."
    echo "[ERROR] Please try again... exit..."
    exit 7
fi

# Install all the packages as specified inside the "requirements.txt" file
echo "################"
echo "[INFO] Install all required python packages..."
$PIP install -r $REQUIREMENTS_FILE > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "[OK] All python packages have been successfully installed!"
else
    echo "[ERROR] An error occurs during the installation of the python packages..."
    echo "[ERROR] Please try again... exit..."
    exit 9
fi


echo "[INFO] Verify if all the required Python packages are correctly installed..."
for package in "${REQUIRED_PACKAGES[@]}"; do
    echo "################"
    check_package $package
done

echo "################"
echo "Package check complete. Exit the program..."
exit 0
