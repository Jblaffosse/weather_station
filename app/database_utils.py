#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Program Name: Weather Station
    Description:  This Python program allows to declare the library of
                  functions used to manipulate the SQLAlchemy database.
                  
                  Following functions are present inside the library:
                  - sql_db_verify_if_db_exists(): 
                    Allows to verify if the SQLAlchemy database exists or not.
                    
                  - sql_db_delete_all_weather_data_related_to_one_WS(): 
                    Allows to delete all the weather data related to the given weather station
                    
                  - sql_db_delete_all_database(): 
                    Allows to delete all the data inside the given database.
                    WARNING!! This is an irreversible action!
                    
                  - sql_db_display_weather_stations(): 
                    Allows to display all the weather stations present inside the database.
                    
                  - sql_db_display_weather_data_for_one_ws(): 
                    Allows to display all the weather data related to a given weather station.
                    
                  - sql_db_retrieve_all_weather_stations(): 
                    Allows to retrieve all the weather stations stored inside the provided database.
                    
                  - sql_db_retrieve_all_weather_data_for_one_ws(): 
                    Allows to retrieve all the weather data for one given weather station.
                    
                  - sql_db_verify_if_db_is_empty(): 
                    Allows to verify if the given database is empty or not.
                    
                  - sql_db_verify_if_ws_exist_in_db(): 
                    Allows to verify if the given weather station is already present inside the database.
                    
                  - sql_db_retrieve_weather_station(): 
                    Allows to retrieve the weather station inside the database corresponding to the given the station name.
                    
                  - sql_db_add_weather_station_into_db(): 
                    Allows to add one weather station inside the provided database.
                    
                  - sql_db_add_weather_data_for_one_ws(): 
                    Allows to add one complete weather data for one WS inside the database.
    
    Author:       JB LAFFOSSE
    Date:         2025-01-16
    Version:      1.0.0
    License:      None
"""

# ==================================================
# Imports
# ==================================================

# Import OS.PATH to verify if the database exists or not
import os.path

# Import for SQLAlchemy 
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm import Session

# Import configuration parameters
from app.config import Config

# Import database model for the weather station and the related data
from app.models import WeatherStation, WeatherData

# ==================================================
# Constants
# ==================================================

# ==================================================
# Functions
# ==================================================

def sql_db_verify_if_db_exists(input_application, input_database):
    """
    Allows to verify if the SQLAlchemy database exists or not.
    
    Returns:
        - True: When the database exists
        - False: When the database does not exist
    """
    # Initialize the Empty status to an error
    db_exists = False
    
    # Try to retrieve all the weather stations inside the provided database
    try:
        # Set up an application context
        with input_application.app_context():
            # Construct the query to retrieve all the weather stations
            query = sa.select(WeatherStation)
        
            # Apply the query to the SQLAlchemy database
            weather_stations = input_database.session.scalars(query).all()
            
    except Exception as e:
        print("An error occurred:", e)
        # An error occurs during the query,
        # Please verify the following pre-requisites:
        # - the database shall be properly initialized
        # - the provided arguments are correct (flask application and database)
        db_exists = False
    else:
        # The query has been successfully executed on the database
        # This means that the database exists, we can set the status to "True"
        db_exists = True

    return db_exists

##################

def sql_db_show_all_tables(input_application, input_database):
    """
    Allows to show all the tables present in the database.
    
    Execution Code:
        - 0: When no error has been detected during the display of the tables
        - 1: When an error occurs during the display of the tables
    """
    # Initialize the Empty status to an error
    execution_code = 1
    
    # First, verify if the database exists
    if sql_db_verify_if_db_exists(input_application, input_database):
    
        # Then, try to retrieve all the tables inside the provided database
        try:
            # Set up an application context
            with input_application.app_context():
                # Get the table names
                all_tables = input_database.metadata.tables.keys()
            
                # Display all the tables
                print("Configured Tables in the Database:")
                for table in all_tables:
                    print(f"- {table}")
                
        except Exception as e:
            print("An error occurred:", e)
            # An error occurs during the query,
            # Please verify the following pre-requisites:
            # - The database shall be properly initialized
            # - At least one table shall be declared inside the database
            execution_code = 1
        else:
            # The query has been successfully executed on the database
            # This means that the database exists, we can set the status to "True"
            execution_code = 0

    return execution_code

##################

def sql_db_delete_all_weather_data_related_to_one_WS(input_application, input_database, input_weather_station):
    """
    Allows to delete all the weather data related to the given weather station
    WARNING! this is an irreversible action!
    
    Execution Code:
        - 0: When all the data have been successfully removed
        - 1: When an error occurs during the deletion
    """
    # Initialize the execution status to an error
    execution_code = 1
    
    # First, verify if the database exists
    if sql_db_verify_if_db_exists(input_application, input_database):
    
        # Try to retrieve all the weather stations inside the provided database
        try:
            # Set up an application context
            with input_application.app_context():
                # Construct the query to retrieve all the weather data related to the given weather station
                query = input_weather_station.weather_datas.select()
            
                # Apply the query to the SQLAlchemy database
                list_weather_data = input_database.session.scalars(query).all()
        except Exception as e:
            print("An error occurred:", e)
            # An error occurs during the query,
            # Please verify the following pre-requisites:
            # - the database shall be properly initialized
            # - at least one weather station shall be declared inside it
            execution_code = 1
        else:
            # Delete one by one all the weather data
            for weather_data in list_weather_data:
                with input_application.app_context():
                    input_database.session.delete(weather_data)
                    input_database.session.commit()
            
            # Set the execution code to 0 as all the weather stations have been successfully retrieved
            execution_code = 0
    
    return execution_code

##################

def sql_db_delete_all_database(input_application, input_database):
    """
    Allows to delete all the data inside the given database.
    WARNING! this is an irreversible action!
    
    Execution Code:
        - 0: When the list has been successfully deleted
        - 1: When an error occurs during the deletion
    """
    # Initialize the execution status to an error
    execution_code = 1
    
    # Create a session to interact with the database
    with input_application.app_context():
        try:
            # Start a session
            current_session = input_database.session
        
            # Delete all records from the WeatherData table
            current_session.query(WeatherData).delete()

            # Delete all records from the WeatherStation table
            current_session.query(WeatherStation).delete()

            # Commit the changes
            current_session.commit()
            print("Database content deleted successfully.")
            
            # Set the execution code to 0 as all the weather stations have been successfully retrieved
            execution_code = 0
            
        except Exception as e:
            # Rollback if something goes wrong
            current_session.rollback()
            print("An error occurred:", e)
        else:
            # Set the execution code to 0 as all the weather stations have been successfully retrieved
            execution_code = 0
    
    return execution_code

##################

def sql_db_display_weather_stations(input_application, input_database):
    """
    Allows to display all the weather stations present inside the database.
    
    Execution Code:
        - 0: When the list has been successfully displayed
        - 1: When an error occurs during the display
    """
    # Initialize the execution status to an error
    execution_code = 1
    
    # First, verify if the database exists
    if sql_db_verify_if_db_exists(input_application, input_database):
    
        # Try to retrieve all the weather stations inside the provided database
        try:
            # Set up an application context
            with input_application.app_context():
                # Construct the query to retrieve all the weather stations
                query = sa.select(WeatherStation)
            
                # Apply the query to the SQLAlchemy database
                weather_stations = input_database.session.scalars(query).all()
                
                # Print all the weather stations present inside the database
                for weather_station in weather_stations:
                    print("Here the information of the weather station " + str(weather_station.id) + ":")
                    print("- Name of the weather station: " + weather_station.station_name)
                    print("- Description for the weather station: " + weather_station.station_description)
                
                # Set the execution code to 0 as the display was successfull
                execution_code = 0
        
        except Exception as e:
            print("An error occurred:", e)
            # An error occurs during the query,
            # Please verify the following pre-requisites:
            # - the database shall be properly initialized
            # - at least one weather station shall be declared inside it
            execution_code = 1

    return execution_code

##################

def sql_db_display_weather_data_for_one_ws(input_application, input_database, input_weather_station_name):
    """
    Allows to display all the weather data related to a given weather station.
    
    Execution Code:
        - 0: When the list has been successfully displayed
        - 1: When an error occurs during the display
    """
    # Initialize the execution status to an error
    execution_code = 1
    
    # First, verify if the database exists
    if sql_db_verify_if_db_exists(input_application, input_database):
    
        # Try to retrieve all the weather stations inside the provided database
        try:
            # Set up an application context
            with input_application.app_context():
                
                # Start a session
                current_session = input_database.session
                
                # Construct the query to retrieve all the weather stations
                query = sa.select(WeatherStation)
            
                # Apply the query to the SQLAlchemy database
                weather_stations = current_session.scalars(query).all()
                
                # Parse all the weather stations present inside the database
                for weather_station in weather_stations:
                
                    # Check the name of the weather station
                    if weather_station.station_name == input_weather_station_name:
                           
                        # We can display all the related weather data
                        
                        # Construct the query to retrieve all the weather data
                        data_query = weather_station.weather_datas.select()
                        
                        # Apply the query to the SQLAlchemy database
                        weather_data = current_session.scalars(data_query).all()
                        
                        # Print all the weather data related to the given weather station
                        for weather_data in weather_data:
                            print("# Weather data " + str(weather_data.id) + ":")
                            print("\t- Temperature: " + str(weather_data.temperature))
                            print("\t- Humidity: " + str(weather_data.humidity))
                            print("\t- Luminosity: " + str(weather_data.luminosity))
       
                        # Set the execution code to 0 as the display was successfull
                        execution_code = 0
        except Exception as e:
            print("An error occurred:", e)
        
            # An error occurs during the query,
            # Please verify the following pre-requisites:
            # - the database shall be properly initialized
            # - at least one weather station shall be declared inside it
            execution_code = 1

    return execution_code

##################

def sql_db_retrieve_all_weather_stations(input_application, input_database):
    """
    Allows to retrieve all the weather stations stored inside the provided database.
    
    Returns:
        - The list of weather stations
        - Execution Code: 
            - 0 when the weather stations are successfully retrieved from the database
            - 1 when an error has been detected during the request
    """
    # Initialize the list of weather station
    list_weather_stations = []
    
    # Initialize the execution status to an error
    execution_code = 1
    
    # First, verify if the database exists
    if sql_db_verify_if_db_exists(input_application, input_database):
    
        # Try to retrieve all the weather stations inside the provided database
        try:
            # Set up an application context
            with input_application.app_context():
                # Construct the query to retrieve all the weather stations
                query = sa.select(WeatherStation)
            
                # Apply the query to the SQLAlchemy database
                list_weather_stations = input_database.session.scalars(query).all()
        except Exception as e:
            print("An error occurred:", e)
            # An error occurs during the query,
            # Please verify the following pre-requisites:
            # - the database shall be properly initialized
            # - at least one weather station shall be declared inside it
            execution_code = 1
        else:            
            # No error has been detected during the query, we can return Success
            execution_code = 0

    return list_weather_stations, execution_code

##################

def sql_db_retrieve_all_weather_data_for_one_ws(input_application, input_database, input_weather_station_name):
    """
    Allows to retrieve all the weather data for one given weather station
    
    Returns:
        Execution Code: 
            - 0 when the weather data are successfully retrieved
            - 1 when an error has been detected during the request
    """
    # Initialize the list of weather data
    list_weather_data = []
    
    # Initialize the execution status to an error
    execution_code = 1
    
    # First, verify if the database exists
    if sql_db_verify_if_db_exists(input_application, input_database):
    
        # Try to retrieve all the weather stations inside the provided database
        try:
            # Set up an application context
            with input_application.app_context():
                
                # Start a session
                current_session = input_database.session
                
                # Construct the query to retrieve all the weather stations
                query = sa.select(WeatherStation)
            
                # Apply the query to the SQLAlchemy database
                weather_stations = current_session.scalars(query).all()
                
                # Parse all the weather stations present inside the database
                for weather_station in weather_stations:
                
                    # Check the name of the weather station
                    if weather_station.station_name == input_weather_station_name:
                    
                        # We have found the corresponding weather station inside the database
                        # We can display all the related weather data
                        
                        # Construct the query to retrieve all the weather data
                        data_query = weather_station.weather_datas.select()
                        
                        # Apply the query to the SQLAlchemy database
                        list_weather_data = current_session.scalars(data_query).all()
        except Exception as e:
            print("An error occurred:", e)
        
            # An error occurs during the query,
            # Please verify the following pre-requisites:
            # - the database shall be properly initialized
            # - at least one weather station shall be declared inside it
            execution_code = 1
        else:            
            # No error has been detected during the query, we can return Success
            execution_code = 0

    return list_weather_data, execution_code

##################

def sql_db_verify_if_db_is_empty(input_application, input_database):
    """
    Allows to verify if the given database is empty or not
    
    Returns:
        Empty Status: 
            - True when the database is empty
            - False when the database is not empty
    """
    # Initialize the Empty status to an error
    db_is_empty = True
    
    # First, verify if the database exists
    if sql_db_verify_if_db_exists(input_application, input_database):
    
        # Try to retrieve all the weather stations inside the provided database
        try:
            # Set up an application context
            with input_application.app_context():
                # Construct the query to retrieve all the weather stations
                query = sa.select(WeatherStation)
            
                # Apply the query to the SQLAlchemy database
                weather_stations = input_database.session.scalars(query).all()
                
                # Check the size of the list with all the weather stations
                if len(weather_stations) > 0:
                    
                    # If at least one weather station has been found inside the database
                    db_is_empty = False
        except Exception as e:
            print("An error occurred:", e)
            # An error occurs during the query,
            # Please verify the following pre-requisites:
            # - the database shall be properly initialized
            # - at least one weather station shall be declared inside it
            db_is_empty = True

    return db_is_empty

##################

def sql_db_verify_if_ws_exist_in_db(input_application, input_database, input_weather_station):
    """
    Allows to verify if the given weather station is already present inside the database
    
    Returns:
        Execution Status: 
            - True when the given weather station is present inside the database
            - False when the given weather station is not present inside the database
    """
    # Initialize the execution status to an error
    present_in_db = False
    
    # First, verify if the database exists
    if sql_db_verify_if_db_exists(input_application, input_database):
    
        # Try to retrieve all the weather stations inside the provided database
        try:
            # Set up an application context
            with input_application.app_context():
                
                # Start a session
                current_session = input_database.session
                
                # Construct the query to retrieve all the weather stations
                query = sa.select(WeatherStation)
            
                # Apply the query to the SQLAlchemy database
                weather_stations = current_session.scalars(query).all()
                
                # Parse all the weather stations present inside the database
                for weather_station in weather_stations:
                
                    # Check the name of the weather station
                    if weather_station.station_name == input_weather_station.station_name:
                    
                        # If the given weather station is already present in database
                        present_in_db = True
        except Exception as e:
            print("An error occurred:", e)
        
            # An error occurs during the query,
            # Please verify the following pre-requisites:
            # - the database shall be properly initialized
            # - at least one weather station shall be declared inside it
            present_in_db = False

    return present_in_db

##################

def sql_db_retrieve_weather_station(input_application, input_database, input_station_name):
    """
   Allows to retrieve the weather station inside the database corresponding to the given the station name.
    
    Returns: The weather station inside the database corresponding to the given the station name.
    """
    # Initialize the execution status to an error
    out_weather_station = WeatherStation(station_name='ERROR', station_description='ERROR')
    
    # First, verify if the database exists
    if sql_db_verify_if_db_exists(input_application, input_database):
    
        # Try to retrieve all the weather stations inside the provided database
        try:
            # Set up an application context
            with input_application.app_context():
                
                # Start a session
                current_session = input_database.session
                
                # Construct the query to retrieve all the weather stations
                query = sa.select(WeatherStation)
            
                # Apply the query to the SQLAlchemy database
                weather_stations = current_session.scalars(query).all()
                
                # Parse all the weather stations present inside the database
                for weather_station in weather_stations:
                
                    # Check the name of the weather station
                    if weather_station.station_name == input_station_name:
                    
                        # If the given weather station is present in database, save the weather station
                        out_weather_station = weather_station
        except Exception as e:
            print("An error occurred:", e)
        
            # An error occurs during the query,
            # Please verify the following pre-requisites:
            # - the database shall be properly initialized
            # - The given weather station shall be present inside it
            out_weather_station = WeatherStation(station_name='ERROR', station_description='ERROR')

    return out_weather_station

##################

def sql_db_add_weather_station_into_db(input_application, input_database, input_weather_station):
    """
    Allows to add one weather station inside the provided database.
    
    Returns:
        Execution Status: 
            - 0 when the weather station has been successfully added to the database
            - 1 when an error has been detected during the creation of the weather station
    """
    # Initialize the execution status to an error
    execution_code = 1
    
    if sql_db_verify_if_db_is_empty(input_application, input_database):
        
        with input_application.app_context():
            # If the input database is empty, we can directly add the input weather station
            input_database.session.add(input_weather_station)
            input_database.session.commit()
            print("The following weather station has been successfully added to the database: " + input_weather_station.station_name)
        
        # The weather stations was successfully added
        execution_code = 0
        
    else:
        # Verify if the input weather station is not already declared inside the database
        if sql_db_verify_if_ws_exist_in_db(input_application, input_database, input_weather_station):
            print("WARNING! The following weather station is already present in the database: " + input_weather_station.station_name)
        else:
        
            with input_application.app_context():
                # If the input database is empty, we can directly add the input weather station
                input_database.session.add(input_weather_station)
                input_database.session.commit()
                
                print("The following weather station has been successfully added to the database: " + input_weather_station.station_name)
            
            # The weather stations was successfully added
            execution_code = 0

    return execution_code

##################

def sql_db_add_weather_data_for_one_ws(input_application, input_database, input_weather_station, input_weather_data):
    """
    Allows to add one complete weather data for one WS inside the database.
    
    Returns:
        Execution Status: 
            - 0 when the weather data has been successfully added to the database
            - 1 when an error has been detected during the creation of the weather data
    """
    # Initialize the execution status to an error
    execution_code = 1
    
    # First, verify if the database exists
    if sql_db_verify_if_db_exists(input_application, input_database):
    
        # Try to retrieve all the weather stations inside the provided database
        try:
            # Set up an application context
            with input_application.app_context():
                
                # Start a session
                current_session = input_database.session
                
                # Construct the query to retrieve all the weather stations
                query = sa.select(WeatherStation)
            
                # Apply the query to the SQLAlchemy database
                weather_stations = current_session.scalars(query).all()
                
                # Parse all the weather stations present inside the database
                for weather_station in weather_stations:
                
                    # Check the name of the weather station
                    if weather_station.station_name == input_weather_station.station_name:
                    
                        # We have found the corresponding weather station inside the database
                        # We can add the weather data and commit the change to the database
                        current_session.add(input_weather_data)
                        current_session.commit()
                    
                        # If the given weather station is already present in database
                        execution_code = 0
        except Exception as e:
            print("An error occurred:", e)
        
            # An error occurs during the query,
            # Please verify the following pre-requisites:
            # - the database shall be properly initialized
            # - at least one weather station shall be declared inside it
            execution_code = 1

    return execution_code

# ==================================================
# Classes
# ==================================================
    