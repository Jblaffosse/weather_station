#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Program Name: Flask Web Application
    Description:  This Python program allows to create a simple
                  Python Web Application using the flash framework.
                  
                  For more information concerning Flask framework,
                  please see the following website(s):
                  https://realpython.com/python-web-applications/
                  https://realpython.com/flask-javascript-frontend-for-rest-api/
                  https://realpython.com/html-css-python/
    
    Author:       JB LAFFOSSE
    Date:         2024-09-04
    Version:      1.0.0
    License:      None
"""

# ==================================================
# Imports
# ==================================================

from flask import Flask
from flask import request

# ==================================================
# Constants
# ==================================================

# Flask Web Server Configuration
deploy_ip_address = "192.168.4.46"
deploy_port_number = 10500
app = Flask(__name__)

# ==================================================
# Functions
# ==================================================
@app.route('/')
def index():
    """
    Flask route to render the main web page with welcome message.
    
    Returns:
        str: Rendered HTML page
    """
    # Submit your the input value into a HTTP GET request
    celsius = request.args.get("celsius", "")
    # If input celsius value is detected
    if celsius:
        # Start the conversion
        fahrenheit = fahrenheit_from(celsius)
        msg_after_conversion = celsius + " °C = " + fahrenheit + " F"
    else:
        msg_after_conversion = ""

    return (
        """<form action="" method="get">
                Celsius temperature: <input type="text" name="celsius">
                <input type="submit" value="Convert">
            </form>"""
        + "Congratulations, this is your first web app! "
        + "Please enter any celsius value you want to convert... <br>"
        + msg_after_conversion
    )

@app.route('/<int:celsius>')
def fahrenheit_from(celsius):
    """
    Convert the input Celsius value into Fahrenheit degrees.
    
    Returns:
        str: Converted value in Fahrenheit
    """
    try:
        # Convert the input celsius value into Fahrenheit
        fahrenheit = float(celsius) * 9 / 5 + 32
        
        # Round to three decimal places
        fahrenheit = round(fahrenheit, 3) 
        
        # Return the converted value
        return str(fahrenheit)
    except ValueError:
        return "invalid input"

# ==================================================
# Main Program Entry
# ==================================================
    
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
