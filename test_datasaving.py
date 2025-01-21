#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Program Name: Weather Station Data Logger
    Description:  This Python program allows to test the retrieval and the
                  storage of data into the database.
    
    Author:       JB LAFFOSSE
    Date:         2025-01-16
    Version:      1.0.0
    License:      None
"""

# ==================================================
# Imports
# ==================================================

# Only for test purpose in order to generate random numbers:
import random

# Import time
import time
from datetime import datetime, timezone

# Import os in order to verify if the database was already created
import os

# JBL TODO test following imports:
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app

# Different imports corresponding to flask framework
from flask import Flask

# Import for SQLAlchemy to manipulate the SQL database
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

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

# Create flask application as an instance of the Flask class
app = Flask(__name__)
app.config.from_object(Config)

# Create an SQLAlchemy database instance
db = SQLAlchemy()

# Declare the number of different weather stations
# IMPROVEMENT - TODO:
# - Define properly  the class used for the weather stations
# - Retrieve dynamically all the different weather stations declared inside the database
class WeatherStation(db.Model):

    # Declare primary key used to navigate withing the database
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    
    # Declare the name for the corresponding weather station
    station_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    
    # Declare a quick description to define the corresponding weather station
    station_description: so.Mapped[str] = so.mapped_column(sa.String(128), index=True)
    
    # Declare the relationship between the data and the weather station
    weather_datas: so.WriteOnlyMapped['WeatherData'] = so.relationship(back_populates='related_station', cascade="all, delete-orphan", passive_deletes=True)
    
    # Return the id of the current weather station
    def get_station_id(self):
        return self.id
    
    # Define how to print the useful information of any instance
    def __repr__(self):
        return 'Weather station: {0}'.format(self.station_name)

class WeatherData(db.Model):
    
    # Declare primary key used to navigate withing the database
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    
    # Declare the time when the data were measured (TBD)
    timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
    
    # Declare the temperature (in celsius) (TBD)
    temperature: so.Mapped[float] = so.mapped_column(nullable=False)
    
    # Declare the humidity rate (TBD)
    humidity: so.Mapped[float] = so.mapped_column(nullable=False)
    
    # Declare the luminosity level (TBD)
    luminosity: so.Mapped[float] = so.mapped_column(nullable=False)
    
    # Declare the weather station which has measured the data
    station_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(WeatherStation.id, ondelete="CASCADE"), index=True)
    
    # Declare the relationship between the data and the weather station
    related_station: so.Mapped[WeatherStation] = so.relationship(back_populates='weather_datas')
    
    # Define how to print the useful information of any instance
    def __repr__(self):
        return 'Weather station {0} has registed the following temperature: {1}'.format(self.station_id, self.temperature)

db.init_app(app)
with app.app_context():
    db.create_all()

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
    sql_db_retrieve_all_weather_stations(app, db)
    
    
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
    sql_db_retrieve_all_weather_stations(app, db)
    
    
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
    
    
    print("####################")
    print("###### Test 10 ######")
    print("####################")
    print("Purpose:")
    print("Check that three previous weather data can be retrieved from the database.")
    print("Expected Result:")
    print("The three weather data are present inside the database!")
    print("Obtained Result:")
    
    # Display all the weather data for one given weather station
    sql_db_retrieve_all_weather_data_for_one_ws(app, db, weather_stations[0])
        
    # Finally, clean any modifications done during the test
    sql_db_delete_all_database(app, db)
        
    
