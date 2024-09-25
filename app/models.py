#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Program Name: Weather Station
    Description:  This Python program allows to define the class for the weather station.
    
    Author:       JB LAFFOSSE
    Date:         2024-09-25
    Version:      1.0.0
    License:      None
"""

# ==================================================
# Imports
# ==================================================

from datetime import datetime, timezone

# Import for SQLAlchemy 
import sqlalchemy as sa
import sqlalchemy.orm as so

from app import db

# ==================================================
# Constants
# ==================================================

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
class WeatherStation(db.Model):

    # Declare primary key used to navigate withing the database
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    
    # Declare the name for the corresponding weather station
    station_name: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    
    # Declare a quick description to define the corresponding weather station
    station_description: so.Mapped[str] = so.mapped_column(sa.String(128), index=True)
    
    # Declare the relationship between the data and the weather station
    weather_datas: so.WriteOnlyMapped['WeatherData'] = so.relationship(back_populates='related_station')
    
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
    station_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(WeatherStation.id), index=True)
    
    # Declare the relationship between the data and the weather station
    related_station: so.Mapped[WeatherStation] = so.relationship(back_populates='weather_datas')
    
    # Define how to print the useful information of any instance
    def __repr__(self):
        return 'Weather station {0} has registed the following temperature: {1}'.format(self.station_id, self.temperature)
    