#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Program Name: Weather Station Data Logger
    Description:  This Python program allows to test the sending
                  of data to the UDP server.
    
    Author:       JB LAFFOSSE
    Date:         2025-01-21
    Version:      1.0.0
    License:      None
"""

# ==================================================
# Imports
# ==================================================

# Only for test purpose in order to generate random numbers:
import random

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

# Only for test purpose: Declare the minimum and maximum to generate random temperature
min_temperature = 15.0
max_temperature = 25.0

# Only for test purpose: Declare the minimum and maximum to generate random humidity
min_humidity = 50.0
max_humidity = 90.0

# Only for test purpose: Declare the minimum and maximum to generate random luminosity
min_luminosity = 0.0
max_luminosity = 100.0

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
    print("Check the following points:\
    \n- The UDP client is well configured,\
    \n- The UDP client sends properly all the messages,\
    \n- The UDP client receives the acknowledgment.")
    print("Expected Result:")
    print("Message correctly sent to the UDP server!")
    print("Message from Server: OK")
    print("Obtained Result:")
    
    # Generate fake weather data
    test_weather_data = test_create_weather_data(1)
    
    # Encode the weather data
    encoded_message = udp_encode_weather_data("Bathroom", "Inside weather station", test_weather_data.temperature, test_weather_data.humidity, test_weather_data.luminosity)
    
    # Create the datagram socket
    udp_server_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    
    # Send a message to the UDP server
    udp_server_socket.sendto(encoded_message, (Config.deploy_ip_address, Config.udp_server_port_number))
    
    print("Message correctly sent to the UDP server!") 
    
    # Wait for the acknowledgment from the UDP server
    udp_message_from_server = udp_server_socket.recvfrom(Config.udp_buffer_size)
    
    print("Message from Server: {}".format(udp_message_from_server[0]))
    
