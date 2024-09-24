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

from flask import Flask
from flask import request
from flask import render_template
import config

# ==================================================
# Constants
# ==================================================

# Configuration parameters have been declared inside "config.py"

# Create flask application as an instance of the Flask class
app = Flask(__name__)

# ==================================================
# Functions
# ==================================================
@app.route('/')
@app.route('/index')
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
        
    # Initialize the variable for the template
    web_page_content = {
            'title' : 'Home Page',
            'msg_after_conversion' : msg_after_conversion
            }
    

    return render_template('index.html', web_page_content=web_page_content, weather_stations=config.weather_stations)

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
        app.run(host=config.deploy_ip_address, port=config.deploy_port_number, debug=True)
    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Cleaning up resources...")
        # Add any cleanup code here if necessary
