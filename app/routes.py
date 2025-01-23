#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Program Name: Weather Station
    Description:  This Python program allows to define all the routes for the web application.
    
    Author:       JB LAFFOSSE
    Date:         2024-09-25
    Version:      1.0.0
    License:      None
"""

# ==================================================
# Imports
# ==================================================

from app import app, db

# Different imports corresponding to flask framework
from flask import request
from flask import render_template, redirect, url_for

# Import configuration parameters
from app.config import Config

# Import database model for the weather station
from app.models import WeatherStation, WeatherData

# Import all the functions related to the SQLAlchemy database library
# (The library can be imported only if the databased was correctly declared and initialized)
from app.database_utils import *

# ==================================================
# Constants
# ==================================================

# ==================================================
# Functions
# ==================================================

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
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
            
    # Retrieve the list of all the weather stations
    current_list_of_ws, execution_code = sql_db_retrieve_all_weather_stations(app, db)
    # current_list_of_ws = []

    return render_template(Config.index_html_file, web_page_content=web_page_content, weather_stations=current_list_of_ws)

@app.route('/<int:celsius>', methods=['GET'])
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


@app.route('/forecasts', methods=['GET', 'POST'])
def forecasts():

    # Initialize the variable for the template
    web_page_content = {
            'title' : 'Home Page'
            }
            
    if (request.method == 'POST') and (request.form['back_button'] == 'back'):
        return redirect( url_for('index') )
    else:
        return render_template(Config.forecasts_html_file, web_page_content=web_page_content)

# ==================================================
# Classes
# ==================================================

