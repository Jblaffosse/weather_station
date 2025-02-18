#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Program Name: Weather Station Data Logger
    Description:  
    
    This Python program allows to retrieve and
    send to the UDP server the following data:
    - Temperature (Celsius) - coming from AHT20
    - Humidity (%) - coming from AHT20
    - Luminosity (Lux) - coming from TSL2591
    
    For more information concerning the AHTx0 library,
    please see the following websites:
    https://docs.circuitpython.org/projects/ahtx0/en/latest/
    https://learn.adafruit.com/adafruit-aht20/python-circuitpython
    
    For more information concerning the TSL2591 library,
    please see the following websites:
    https://docs.circuitpython.org/projects/tsl2591/en/latest/
    https://learn.adafruit.com/adafruit-tsl2591/python-circuitpython
    
    Author:       JB LAFFOSSE
    Date:         2025-02-18
    Version:      1.0.0
    License:      None
"""

# ==================================================
# Imports
# ==================================================

# For sleep() function
import time

# For the sensor connection
import board

# Import libraries used for both sensors
import adafruit_tsl2591
import adafruit_ahtx0

# For the UDP server
import socket
from app.data_transmission_utils import *

# For the UDP messages
import struct

# Import configuration parameters
from app.config import Config

# Import database model for the weather station
from app.models import WeatherStation, WeatherData

# ==================================================
# Constants
# ==================================================

# Flag to control the main loop
main_loop = True

# Data acquisition period (in seconds)
data_acquisition_period = 60

# Declare the name of the weather station
weather_station_name = "Bedroom"

# Declare the description for the weather station
weather_station_description = "Master bedroom of the appartment"

print("# Initializing {} ...".format(weather_station_name))

print("# Open I2C port...")
# Declare I2C port
i2c_port = board.I2C()
print("# I2C port successfully open!")

print("# Initialize TSL2591 Sensor...")
# Declare TSL2591 Sensor
light_sensor = adafruit_tsl2591.TSL2591(i2c_port)
print("# TSL2591 Sensor successfully initialized!")

# Define the gain for the TSL2591 Sensor
light_sensor.gain = adafruit_tsl2591.GAIN_MED
# Here all potential values for the gain: 
#       - GAIN_LOW - 1x
#       - GAIN_MED - 25x (the default)
#       - GAIN_HIGH - 428x
#       - GAIN_MAX - 9876x

# Define the integration time for the TSL2591 Sensor
light_sensor.integration_time = adafruit_tsl2591.INTEGRATIONTIME_100MS
# Here all potential values for the integration time: 
#       - INTEGRATIONTIME_100MS- 100ms (the default)
#       - INTEGRATIONTIME_200MS- 200ms
#       - INTEGRATIONTIME_300MS- 300ms
#       - INTEGRATIONTIME_400MS- 400ms
#       - INTEGRATIONTIME_500MS- 500ms
#       - INTEGRATIONTIME_600MS- 600ms

print("# Initialize AHT20 Sensor...")
# Declare AHT20 Sensor
temp_hum_sensor = adafruit_ahtx0.AHTx0(i2c_port)
print("# AHT20 Sensor successfully initialized!")

# ==================================================
# Functions
# ==================================================

def read_light_level():
    """
    Reads the light level from the TSL2591 sensor.
    
    Returns:
        float: Light level in lux
    """
    return light_sensor.lux

def read_temperature_humidity():
    """
    Reads temperature and humidity from the AHT20 sensor.
    
    Returns:
        tuple: Temperature in Celsius, Humidity in percentage
    """
    humidity = temp_hum_sensor.relative_humidity
    temperature = temp_hum_sensor.temperature
    return temperature, humidity

# ==================================================
# Main Program Entry
# ==================================================

print("# {} successfully initialized!".format(weather_station_name))

if __name__ == "__main__":
    
    # Execute an infinite loop to retrieve temperature, humidity and luminosity
    try:
        while main_loop:
            # Retrieve the temperature and humidity provided by the AHT20 sensor
            current_temperature, current_humidity = read_temperature_humidity()
            
            # Retrieve the light level provided by the TSL2591 sensor
            current_light_level = read_light_level()
        
            # Encode the weather data
            encoded_message = udp_encode_weather_data(weather_station_name,
                                                weather_station_description,
                                                current_temperature,
                                                current_humidity,
                                                current_light_level)
            
            # Create the datagram socket
            udp_client_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            
            # Send a message to the UDP server
            udp_client_socket.sendto(encoded_message, (Config.deploy_ip_address, Config.udp_server_port_number))
            
            print("# Message correctly sent to the UDP server!") 
            
            # Wait for the acknowledgment from the UDP server
            udp_message_from_server = udp_client_socket.recvfrom(Config.udp_buffer_size)
            
            print("# Message from Server: {}".format(udp_message_from_server[0]))
            
            # Wait for 2 seconds
            time.sleep(data_acquisition_period)
        
    except KeyboardInterrupt:
        print("# Program interrupted by user. Exiting...")
    except Exception as e:
        print(f"# An error occurred: {e}")
    finally:
        print("# Cleaning up resources...")
        # Close the socket and exit properly the program
        udp_client_socket.close()
        print("# Ressources successfully cleaned, exit program...")
        exit(0)
