#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Program Name: Weather Station Data Logger
    Description:  This Python program allows to test the retrieval and the
                  storage of data into the database.
    
    Author:       JB LAFFOSSE
    Date:         2025-01-16
    Version:      1.0.1
    License:      None
"""

# ==================================================
# Imports
# ==================================================

# First initialize all the environment and application
from app import app, db

# db.init_app(app)
with app.app_context():
    db.create_all()

# Only for test purpose in order to generate random numbers:
import random

# Import threading used to execute the UDP server inside a dedicated thread
import threading

# Import time
import time
from datetime import datetime, timezone

# For the UDP server
# from app.data_transmission_utils import *

# Import for SQLAlchemy 
import sqlalchemy as sa
import sqlalchemy.orm as so

# Different imports corresponding to flask framework
from flask import Flask

# Import for SQLAlchemy to manipulate the SQL database
from flask_sqlalchemy import SQLAlchemy

# Import configuration parameters
from app.config import Config

# ==================================================
# Constants
# ==================================================

# Only for test purpose: Declare the minimum and maximum to generate random temperature
min_temperature = 15.0
max_temperature = 25.0

# Only for test purpose: Declare the minimum and maximum to generate random humidity
min_humidity = 50.0
max_humidity = 90.0

# Only for test purpose: Declare the minimum and maximum to generate random luminosity
min_luminosity = 0.0
max_luminosity = 100.0

# Import all the functions related to the SQLAlchemy database library
# (The library can be imported only if the databased was correctly declared and initialized)
from app.database_utils import *

# Only for test purpose: Declare two fake weather stations
weather_stations = [
                    WeatherStation(station_name='Bedroom',
                                    station_description='Master bedroom'),
                    WeatherStation(station_name='Living Room',
                                    station_description='Living room with kitchen')
                                    ]

# ==================================================
# Functions
# ==================================================

def test_create_weather_data(input_station_id):
    """
    Allows to create fake weather data (temperature, humidity and luminosity)
    for one given station id.
    
    Returns:
        WeatherData: instance of the class with all the values
    """
    
    fake_temperature = random.uniform(min_temperature, max_temperature)
    fake_humidity = random.uniform(min_humidity, max_humidity)
    fake_luminosity = random.uniform(min_luminosity, max_luminosity)
    
    fake_weather_data = WeatherData(temperature = fake_temperature, humidity = fake_humidity, luminosity = fake_luminosity, station_id = input_station_id)
    
    
    return fake_weather_data

# ==================================================
# Main Program Entry
# ==================================================

if __name__ == "__main__":

    print("####################")
    print("###### Test 1 ######")
    print("####################")
    print("Purpose:")
    print("Check that sql_db_verify_if_db_exists() detects if the SQLAlchemy database is correctly initialized and configured.")
    print("Expected Result:")
    print("The SQLAlchemy database is properly initialized and configured!")
    print("Obtained Result:")

    # Test the following function: sql_db_verify_if_db_exists()
    if sql_db_verify_if_db_exists(app, db):
        print("The SQLAlchemy database is properly initialized and configured!")
    else:
        print("The database does not exist, please make sure to initialize and configure properly the SQLAlchemy database")

    # First, reset any previous data
    sql_db_delete_all_database(app, db)
    
    # Display the content of the database
    sql_db_display_weather_stations(app, db)
    
    
    print("####################")
    print("###### Test 2 ######")
    print("####################")
    print("Purpose:")
    print("Check that sql_db_add_weather_station_into_db() adds correctly one weather station inside the database.")
    print("Expected Result:")
    print("The following weather station has been successfully added to the database: Living Room")
    print("Obtained Result:")
    
    # Add one weather station inside the database
    sql_db_add_weather_station_into_db(app, db, weather_stations[1])
    
    
    print("####################")
    print("###### Test 3 ######")
    print("####################")
    print("Purpose:")
    print("Check that two similar weather stations cannot be present inside the database.")
    print("Expected Result:")
    print("WARNING! The following weather station is already present in the database: Living Room")
    print("Obtained Result:")
    
    # Verify the following robustness case:
    # Every weather station shall be unique, therefore two similar
    # weather stations cannot be present inside the database
    sql_db_add_weather_station_into_db(app, db, weather_stations[1])
    
    
    print("####################")
    print("###### Test 4 ######")
    print("####################")
    print("Purpose:")
    print("Check that sql_db_add_weather_station_into_db() adds correctly one weather station inside the database.")
    print("Expected Result:")
    print("The following weather station has been successfully added to the database: Bedroom")
    print("Obtained Result:")
    
    # Add a second weather station inside the database
    sql_db_add_weather_station_into_db(app, db, weather_stations[0])
    
    
    print("####################")
    print("###### Test 5 ######")
    print("####################")
    print("Purpose:")
    print("Check that two similar weather stations cannot be present inside the database.")
    print("Expected Result:")
    print("WARNING! The following weather station is already present in the database: Bedroom")
    print("Obtained Result:")
    
    # Verify the following robustness case:
    # Every weather station shall be unique, therefore two similar
    # weather stations cannot be present inside the database
    sql_db_add_weather_station_into_db(app, db, weather_stations[0])
    
    
    print("####################")
    print("###### Test 6 ######")
    print("####################")
    print("Purpose:")
    print("Check that two weather stations are present inside the database.")
    print("Expected Result:")
    print("The weather stations related to Living room and bedroom are present inside the database")
    print("Obtained Result:")
    
    # Display the content of the database
    sql_db_display_weather_stations(app, db)
    
    
    print("####################")
    print("###### Test 7 ######")
    print("####################")
    print("Purpose:")
    print("Check that weather data can be added to one weather station.")
    print("Expected Result:")
    print("The weather data has been successfully added inside the database!")
    print("Obtained Result:")
    
    # Add several weather data for one weather station
    test_weather_data1 = test_create_weather_data(weather_stations[0].id)
    if sql_db_add_weather_data_for_one_ws(app, db, weather_stations[0], test_weather_data1) == 0:
        print("The weather data has been successfully added inside the database!")
    else:
        print("An error occurs during the adding of the weather data inside the database...")
    
    
    print("####################")
    print("###### Test 8 ######")
    print("####################")
    print("Purpose:")
    print("Check that weather data can be added to one weather station.")
    print("Expected Result:")
    print("The weather data has been successfully added inside the database!")
    print("Obtained Result:")
    
    test_weather_data2 = test_create_weather_data(weather_stations[0].id)
    if sql_db_add_weather_data_for_one_ws(app, db, weather_stations[0], test_weather_data2) == 0:
        print("The weather data has been successfully added inside the database!")
    else:
        print("An error occurs during the adding of the weather data inside the database...")
    
    
    print("####################")
    print("###### Test 9 ######")
    print("####################")
    print("Purpose:")
    print("Check that weather data can be added to one weather station.")
    print("Expected Result:")
    print("The weather data has been successfully added inside the database!")
    print("Obtained Result:")
    
    test_weather_data3 = test_create_weather_data(weather_stations[0].id)
    if sql_db_add_weather_data_for_one_ws(app, db, weather_stations[0], test_weather_data3) == 0:
        print("The weather data has been successfully added inside the database!")
    else:
        print("An error occurs during the adding of the weather data inside the database...")
    
    
    print("#####################")
    print("###### Test 10 ######")
    print("#####################")
    print("Purpose:")
    print("Check that three previous weather data can be retrieved from the database.")
    print("Expected Result:")
    print("The three weather data are present inside the database!")
    print("Obtained Result:")
    
    # Display all the weather data for one given weather station
    sql_db_display_weather_data_for_one_ws(app, db, weather_stations[0])
    
    print("#####################")
    print("###### Test 11 ######")
    print("#####################")
    print("Purpose:")
    print("Check the following points:\
    \n- The UDP server is well configured,\
    \n- The UDP server retrieves properly all the messages,\
    \n- The UDP server stores correctly all the messages inside the database,\
    \n- The UDP server sends back correctly the acknowledgment to the UDP client.")
    print("Expected Result:")
    print("The following weather station has been successfully added to the database: ...")
    print("Obtained Result:")
    
    try:
        while(True):
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Cleaning up resources...")
        # Add any cleanup code here if necessary
    
    # Finally, clean any modifications done during the test
    sql_db_delete_all_database(app, db)
        
    
