#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Program Name: Flask Web Application
    Description:  This Python program allows to create a simple
                  Python Web Application using the flash framework.
                  
                  For more information concerning Flask framework,
                  please see the following website(s):
                  https://realpython.com/python-web-applications/
    
    Author:       JB LAFFOSSE
    Date:         2024-09-04
    Version:      1.0.0
    License:      None
"""

# ==================================================
# Imports
# ==================================================

from flask import Flask

# ==================================================
# Constants
# ==================================================

# Flask Web Server Configuration
deploy_ip_address = "127.0.0.1"
deploy_port_number = 10500
app = Flask(__name__)

# ==================================================
# Functions
# ==================================================


# ==================================================
# Main Program Entry
# ==================================================

@app.route("/")
def index():
    return "Congratulations, this is your first web app!"
    
    
if __name__ == "__main__":
    try:
        app.run(host=deploy_ip_address, port=deploy_port_number, debug=True)
    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Cleaning up resources...")
        # Add any cleanup code here if necessary
