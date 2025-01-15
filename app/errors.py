#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Program Name: Weather Station
    Description:  This Python program allows to define all the error pages for the web application.
    
    Author:       JB LAFFOSSE
    Date:         2025-01-15
    Version:      1.0.0
    License:      None
"""

# ==================================================
# Imports
# ==================================================

from app import app

# Different imports corresponding to flask framework
from flask import render_template

# Import configuration parameters
from app.config import Config

# Import database for the weather station
from app import app, db

# ==================================================
# Constants
# ==================================================

# ==================================================
# Functions
# ==================================================

# Declare the error page when the requested URL is incorrect
@app.errorhandler(404)
def not_found_error(error):
    return render_template(Config.error_404_page), 404
    
# Declare the error page 500 when an internal error has occured inside the server
@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template(Config.error_500_page), 500

# ==================================================
# Classes
# ==================================================

