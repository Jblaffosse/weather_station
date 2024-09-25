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

# All the configuration parameters within one single class
class Config:

    # Define the IP address used to deployed the web application
    deploy_ip_address = "127.0.0.1"
    
    # Define the port used to deployed the web application
    deploy_port_number = 10500
    
    # Define the name of the HTML files used for the application
    index_html_file = 'index.html'
    forecasts_html_file = 'forecasts.html'

    # Define the location of the application's database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')