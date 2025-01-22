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

# ==================================================
# Classes
# ==================================================
    