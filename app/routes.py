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
from flask import request, jsonify
from flask import render_template, redirect, url_for

# Import configuration parameters
from app.config import Config

# Import database model for the weather station
from app.models import WeatherStation, WeatherData

# Import all the functions related to the SQLAlchemy database library
# (The library can be imported only if the databased was correctly declared and initialized)
from app.database_utils import *

# Import librairies to change timezone and display of timestamps
from datetime import datetime
import pytz

# ==================================================
# Constants
# ==================================================

# Define target timezone (example : UTC-5)
target_timezone = pytz.timezone('America/New_York')

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
        
    # Initialize the variable for the template
    web_page_content = {
            'title' : 'Home Page'
            }
            
    # Retrieve the list of all the weather stations
    current_list_of_ws, execution_code = sql_db_retrieve_all_weather_stations(app, db)

    return render_template(Config.index_html_file, web_page_content=web_page_content, weather_stations=current_list_of_ws)

@app.route("/get_station_data_by_name/<string:station_name>")
def get_station_data(station_name):
    """
    Flask route to retrieve all the weather data related to the given weather station
    
    Returns:
        str: Rendered HTML page
    """
        
    # Initialize the variable for the template
    web_page_content = {
            'title' : 'Get Weather Station'
            }
    
    # DEBUG - sql_db_display_weather_data_for_one_ws(app, db, station_name)

    # Fetch weather data for the selected station
    weather_data, execution_code = sql_db_retrieve_all_weather_data_for_one_ws(app, db, station_name)
    
    # Prepare the data for the graph
    data = {
        "timestamps": [data.timestamp.astimezone(target_timezone).strftime('%Y-%m-%d %H:%M') for data in weather_data],
        "temperatures": [data.temperature for data in weather_data],
        "humidities": [data.humidity for data in weather_data]
    }
    return jsonify(data)

@app.route('/forecasts', methods=['GET', 'POST'])
def forecasts():
    """
    Flask route to render the forecast web page.
    
    Returns:
        str: Rendered HTML page
    """

    # Initialize the variable for the template
    web_page_content = {
            'title' : 'Forecast'
            }
            
    if (request.method == 'POST') and (request.form['back_button'] == 'back'):
        return redirect( url_for('index') )
    else:
        return render_template(Config.forecasts_html_file, web_page_content=web_page_content)

@app.route('/configuration', methods=['GET', 'POST'])
def configuration():
    """
    Flask route to render the configuration page.
    
    Returns:
        str: Rendered HTML page
    """

    # Initialize the variable for the template
    web_page_content = {
            'title' : 'Configuration'
            }
            
    if (request.method == 'POST') and (request.form['back_button'] == 'back'):
        return redirect( url_for('index') )
    else:
        return render_template(Config.configuration_page, web_page_content=web_page_content)
        
# ==================================================
# Classes
# ==================================================

