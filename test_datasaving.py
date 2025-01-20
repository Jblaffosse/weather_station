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

def test_create_weather_data():
    """
    Allows to create fake weather data (temperature, humidity and luminosity).
    
    Returns:
        WeatherData: instance of the class with all the values
    """
    
    fake_temperature = random.uniform(min_temperature, max_temperature)
    fake_humidity = random.uniform(min_humidity, max_humidity)
    fake_luminosity = random.uniform(min_luminosity, max_luminosity)
    random_station_id = weather_stations[random.randint(0,1)].get_station_id()
    
    fake_weather_data = WeatherData(temperature = fake_temperature, humidity = fake_humidity, luminosity = fake_luminosity, station_id = random_station_id)
    
    
    return fake_weather_data

# ==================================================
# Main Program Entry
# ==================================================

if __name__ == "__main__":

    # First, reset any previous data
    sql_db_delete_all_database(app, db)
    
    sql_db_retrieve_all_weather_stations(app, db)
    
    # Add one weather station inside the database
    sql_db_add_weather_station_into_db(app, db, weather_stations[1])
    sql_db_add_weather_station_into_db(app, db, weather_stations[1])
    sql_db_add_weather_station_into_db(app, db, weather_stations[0])
    sql_db_add_weather_station_into_db(app, db, weather_stations[0])
    
    sql_db_retrieve_all_weather_stations(app, db)
        
    # Finally, clean any modifications done during the test
    sql_db_delete_all_database(app, db)
        
    
