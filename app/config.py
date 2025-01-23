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

    # Define if the web application is executed 
    deploy_mode = True

    # Define the IP address used to deployed the web application
    # and also the UDP server
    deploy_ip_address = "127.0.0.1"
    
    # Define the port used to deployed the UDP server
    udp_server_port_number = 10501
    
    # Define the port used to deployed the web application
    deploy_port_number = 10500
    
    # Define the size of the UDP packets exchanged between
    # the UDP client and the UDP server
    udp_buffer_size = 1024
    
    # Define the acknowledge message send by the UDP server
    # to the UDP client
    udp_ack_to_client = "OK"
    udp_ack_to_client_bytes = str.encode(udp_ack_to_client)
    
    # Define the name of the HTML files used for the application
    index_html_file = 'index.html'
    forecasts_html_file = 'forecasts.html'
    configuration_page = 'configuration.html'
    error_404_page = '404.html'
    error_500_page = '500.html'

    # Define the location of the application's database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'ws_app.db')
        
    # Define the absolute path to the SQLAlchemy database
    sqlalchemy_absolute_path = os.path.join(basedir, 'ws_app.db')