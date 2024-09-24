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



# ==================================================
# Constants
# ==================================================

# Flask Web Server Configuration
deploy_ip_address = "127.0.0.1"
deploy_port_number = 10500

# ==================================================
# Functions
# ==================================================

# ==================================================
# Classes
# ==================================================

# Declare the number of different weather stations
# IMPROVEMENT - TODO need to dynamically create this variable by detecting
# all the different weather stations declared inside the database
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


