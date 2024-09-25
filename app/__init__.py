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
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# ==================================================
# Constants
# ==================================================

# Configuration parameters have been declared inside "config.py"

# Create the SQLAlchemy database
db = SQLAlchemy()

# Create flask application as an instance of the Flask class
app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
with app.app_context():
    db.create_all()

#  Create the migration engine related to the flask application and the database
migrate = Migrate(app, db)

# Import routes and models following the initialization 
# of the flask app and the SQLAlchemy database
from app import routes, models


# ==================================================
# Functions
# ==================================================

