#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Program Name: Weather Station
    Description:  This Python program allows to declare the library of functions
                  used to transmit and receive weather data over UDP.
                  
                  Following functions are present inside the library:
                  - udp_encode_weather_data(): 
                    Allows to encode the weather data into one single message.
                    
                  - udp_decode_weather_data(): 
                    Allows to decode the weather data encoded inside one single message.
                    
                  - udp_initialize_and_start_udp_server(): 
                    Allows to initialize and execute the UDP server.
    
    Author:       JB LAFFOSSE
    Date:         2025-01-21
    Version:      1.0.0
    License:      None
"""

# ==================================================
# Imports
# ==================================================

# Import struct to format and parse properly the weather data inside UDP messages
import struct

# For the UDP server
import socket

# Import configuration parameters
from app.config import Config

# Import all the functions related to the SQLAlchemy database library
# (The library can be imported only if the databased was correctly declared and initialized)
from app.database_utils import *

# ==================================================
# Constants
# ==================================================

# ==================================================
# Functions
# ==================================================

def udp_encode_weather_data(
    station_name: str,
    station_description: str,
    temperature: float,
    humidity: float,
    luminosity: float):
    """
    Allows to encode the weather data into one single message.
    
    The message is composed of the following fields in this order:
    - station_name (fixed 32 bytes)
    - station description (fixed 64 bytes)
    - temperature (float)
    - humidity (float)
    - luminosity (float)
    
    Returns: the encoded message with all the weather data
    """
    # Construct the encoded message
    encoded_message = struct.pack(
            '32s64sfff',
            station_name.encode('utf-8'),
            station_description.encode('utf-8'),
            temperature,
            humidity,
            luminosity)

    # Return the encoded message
    return encoded_message

##################

def udp_decode_weather_data(input_encoded_message):
    """
    Allows to decode the weather data encoded inside one single message.
    
    The message is composed of the following fields in this order:
    - station_name (fixed 32 bytes)
    - station description (fixed 64 bytes)
    - temperature (float)
    - humidity (float)
    - luminosity (float)
    
    Returns: all the weather data in the correct order
    """
    # Unpack the encoded message
    station_name, station_description, temperature, humidity, luminosity = struct.unpack('32s64sfff', input_encoded_message)
    
    # Decode and strip null bytes
    station_name = station_name.decode('utf-8').strip('\x00')
    
    # Decode and strip null bytes
    station_description = station_description.decode('utf-8').strip('\x00')

    # Return the decoded message
    return station_name, station_description, temperature, humidity, luminosity

##################

def udp_initialize_and_start_udp_server(input_application, input_database):
    """
    Allows to perform the following actions:
    - Configure and initialize the UDP server,
    - Receive all the data coming from the weather stations
    - Acknowledge message received from the UDP client
    - Parse and decode the incoming messages
    - Store the weather data inside the database
    
    Returns: N/A
    """
    
    try:
    
        # Create an UDP socket
        udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        
        # Bind the socket to the provided IP address and UDP port
        udp_server_socket.bind((Config.deploy_ip_address, Config.udp_server_port_number))
        
        print(f"UDP server up and listening on {Config.deploy_ip_address}:{Config.udp_server_port_number}!")
    
        # Listen for incoming datagrams
        while(True):
        
            # Receive incoming messages
            udp_bytes_address_pair = udp_server_socket.recvfrom(Config.udp_buffer_size)
            
            # Retrieve the messages and the IP address from the UDP client
            udp_message = udp_bytes_address_pair[0]
            udp_client_ip_address = udp_bytes_address_pair[1]
            
            # Acknowledge message received from the UDP client
            udp_server_socket.sendto(Config.udp_ack_to_client_bytes, udp_client_ip_address)
            
            # Decode the received message:
            current_station_name, current_station_description, current_temperature, current_humidity, current_luminosity = udp_decode_weather_data(udp_message)
            
            # Print the parsed data
            print(f"Station Name: {current_station_name}")
            print(f"Station Description: {current_station_description}")
            print(f"Temperature: {current_temperature} °C")
            print(f"Humidity: {current_humidity} %")
            print(f"Luminosity: {current_luminosity} lux")
            
            current_weather_station = sql_db_retrieve_weather_station(input_application, input_database, current_station_name)
            if current_weather_station.station_name == 'ERROR':
                # The weather station is not present inside the database and shall be added
                
                # Create new weather station
                new_weather_station = WeatherStation(station_name = current_station_name,
                                                    station_description = current_station_description)
                if sql_db_add_weather_station_into_db(input_application, input_database, new_weather_station) == 0:
                    print("The following weather station has been successfully added into the database: " + current_station_name)
                else:
                    print("An error occurs during the adding of the following weather station: " + current_station_name)
                
                # Set the current station to the newly added weather station
                current_weather_station = new_weather_station
            else:
                print("The weather station is already present inside the database, add the related weather data...")
            
            # Create one instance of Weather Data with the received information
            received_weather_data = WeatherData(temperature = current_temperature, humidity = current_humidity, luminosity = current_luminosity, station_id = current_weather_station.get_station_id())
            
            # Add the received weather data inside the database
            if sql_db_add_weather_data_for_one_ws(input_application, input_database, current_weather_station, received_weather_data) == 0:
                print("The weather data has been successfully added inside the database!")
            else:
                print("An error occurs during the adding of the weather data inside the database...")
                
            # Display all the weather data for one given weather station
            # DEBUG - sql_db_display_weather_data_for_one_ws(input_application, input_database, current_weather_station.station_name)
            
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the socket
        udp_server_socket.close()

##################

# ==================================================
# Classes
# ==================================================
    