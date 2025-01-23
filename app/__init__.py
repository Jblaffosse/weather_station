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
from flask import Flask

# Import configuration parameters
from app.config import Config

# Import for SQLAlchemy 
import sqlalchemy as sa
import sqlalchemy.orm as so
# from app import app

# Import time
import time
from datetime import datetime, timezone

# Import for SQLAlchemy 
from flask_sqlalchemy import SQLAlchemy

# Import threading used to execute the UDP server inside a dedicated thread
import threading

# ==================================================
# Constants
# ==================================================

# Configuration parameters have been declared inside "config.py"

# Create flask application as an instance of the Flask class
app = Flask(__name__)
app.config.from_object(Config)

# Create the SQLAlchemy database
db = SQLAlchemy(app)

# Import routes and models following the initialization 
# of the flask app and the SQLAlchemy database
from app import routes, models, errors

# Import the library used to initialize and start the UDP server
from app.data_transmission_utils import *

if sql_db_show_all_tables(app, db) == 0:
    print("The tables have been properly declared inside the database!")
else:
    print("An error occurs during the retrieving of the tables inside the database...")

# Start the UDP server in a separate thread
udp_thread = threading.Thread(target = udp_initialize_and_start_udp_server, args = (app, db))

# Daemonize thread to close with the app
udp_thread.daemon = True

# Start the thread
udp_thread.start()



# ==================================================
# Functions
# ==================================================

