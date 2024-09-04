#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Program Name: Weather Station Data Logger
    Description:  This Python program allows to test the TSL2591 and verify
                  that the light sensor is correctly connected.
                  
                  For more information concerning the TSL2591 library,
                  please see the following websites:
                  https://docs.circuitpython.org/projects/tsl2591/en/latest/
                  https://learn.adafruit.com/adafruit-tsl2591/python-circuitpython
    
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
import adafruit_tsl2591

# ==================================================
# Constants
# ==================================================

# Declare I2C port
i2c_port = board.I2C()

# Declare TSL2591 Sensor
light_sensor = adafruit_tsl2591.TSL2591(i2c_port)

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

# ==================================================
# Main Program Entry
# ==================================================

if __name__ == "__main__":
    print("Press spacebar if you want to exit the loop...")
    
    # Loop until the spacebar is pressed
    while True:
        # Retrieve the light level provided by the TSL2591 sensor
        current_light_level = read_light_level()
        
        # Display properly the current light level
        print('Light: {0}lux'.format(current_light_level))
    
        # Wait for 2 seconds
        time.sleep(2)
        
        # Verify if the spacebar is pressed
        if keyboard.is_pressed('space'):
            print("Spacebar pressed. Exiting program.")
            break
