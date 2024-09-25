#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Program Name: Weather Station
    Description:  This Python program allows to configure the web application.
    
    Author:       JB LAFFOSSE
    Date:         2024-09-24
    Version:      1.0.0
    License:      None
"""

# ==================================================
# Imports
# ==================================================

import os

# ==================================================
# Constants
# ==================================================

# Define the base directory
basedir = os.path.abspath(os.path.dirname(__file__))


# ==================================================
# Functions
# ==================================================

# ==================================================
# Classes
# ==================================================

# Declare the number of different weather stations
# IMPROVEMENT - TODO:
# - Define properly  the class used for the weather stations
# - Retrieve dynamically all the different weather stations declared inside the database
class WeatherStation:
    weather_stations = [
            {
                'id': 101,
                'name': 'Bedroom',
                'description': 'Master bedroom'
            },
            {
                'id': 102,
                'name': 'Salon',
                'description': 'Salon and kitchen'
            }
        ]


# All the configuration parameters within one single class
class Config:

    # Define the IP address used to deployed the web application
    deploy_ip_address = "127.0.0.1"
    
    # Define the port used to deployed the web application
    deploy_port_number = 10500

    # 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')