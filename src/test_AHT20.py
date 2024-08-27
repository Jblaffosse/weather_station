#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Program Name: Weather Station Data Logger
    Description:  This Python program allows to test the AHT20 and verify that
                  the temperature and humidity sensor is correctly connected.
                  
                  For more information concerning the AHTx0 library,
                  please see the following websites:
                  https://docs.circuitpython.org/projects/ahtx0/en/latest/
                  https://learn.adafruit.com/adafruit-aht20/python-circuitpython
    
    Author:       JB LAFFOSSE
    Date:         2024-09-02
    Version:      1.0.0
    License:      None
"""

# ==================================================
# Imports
# ==================================================

import time
import board
# Only imported for test purpose
import keyboard
# TODO verify that the library is correctly imported
import adafruit_ahtx0

# ==================================================
# Constants
# ==================================================

# Declare I2C port
i2c_port = board.I2C()

# Declare AHT20 Sensor
temp_hum_sensor = adafruit_ahtx0.AHTx0(i2c_port)

# ==================================================
# Functions
# ==================================================

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

if __name__ == "__main__":
    print("Press spacebar if you want to exit the loop...")
    
    # Loop until the spacebar is pressed
    while True:
        # Retrieve the temperature and humidity provided by the AHT20 sensor
        current_temperature, current_humidity = read_temperature_humidity()
        
        # Display properly the current temperature and humidity
        print("\nTemperature: %0.1f C" % current_temperature)
        print("Humidity: %0.1f %%" % current_humidity)
    
        # Wait for 2 seconds
        time.sleep(2)
        
        # Verify if the spacebar is pressed
        if keyboard.is_pressed('space'):
            print("Spacebar pressed. Exiting program.")
            break
