#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Program Name: Weather Station
    Description:  This Python program allows to create a simple
                  Python Web Application using the flash framework.
                  
                  For more information concerning Flask framework,
                  please see the following website(s):
                  https://realpython.com/python-web-applications/
                  https://realpython.com/flask-javascript-frontend-for-rest-api/
                  https://realpython.com/html-css-python/
                  
                  https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
    
    Author:       JB LAFFOSSE
    Date:         2024-09-24
    Version:      1.0.0
    License:      None
"""

# ==================================================
# Imports
# ==================================================

# Different imports corresponding to flask framework
from app import app
# is it useful ? TBD TODO set FLASK_APP=weather_station.py

# Import configuration parameters
from app.config import Config

# ==================================================
# Constants
# ==================================================

# ==================================================
# Functions
# ==================================================

# ==================================================
# Main Program Entry
# ==================================================
    
if __name__ == "__main__":
    try:
        app.run(host=Config.deploy_ip_address, port=Config.deploy_port_number, debug=True)
    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Cleaning up resources...")
        # Add any cleanup code here if necessary
