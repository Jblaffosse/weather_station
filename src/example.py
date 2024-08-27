#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    Program Name: Weather Station Data Logger
    Description:  This Python program reads data from temperature, humidity, 
                  and light sensors connected to a Raspberry Pi and serves 
                  the data on a web interface.
    
    Author:       JB LAFFOSSE
    Date:         2024-09-02
    Version:      1.0.0
    License:      None
"""

# ==================================================
# Imports
# ==================================================

import time
import Adafruit_DHT
import board
import busio
import adafruit_tsl2561
from flask import Flask, render_template

# ==================================================
# Constants
# ==================================================

# DHT22 Sensor
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4  # GPIO pin connected to the DHT22 data pin

# TSL2561 Light Sensor
i2c = busio.I2C(board.SCL, board.SDA)
light_sensor = adafruit_tsl2561.TSL2561(i2c)

# Flask Web Server Configuration
app = Flask(__name__)

# ==================================================
# Functions
# ==================================================

def read_temperature_humidity():
    """
    Reads temperature and humidity from the DHT22 sensor.
    
    Returns:
        tuple: Temperature in Celsius, Humidity in percentage
    """
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    return temperature, humidity

def read_light_level():
    """
    Reads the light level from the TSL2561 sensor.
    
    Returns:
        float: Light level in lux
    """
    return light_sensor.lux

@app.route('/')
def index():
    """
    Flask route to render the main web page with sensor data.
    
    Returns:
        str: Rendered HTML page
    """
    temperature, humidity = read_temperature_humidity()
    light_level = read_light_level()
    return render_template('index.html', temp=temperature, humidity=humidity, light=light_level)

# ==================================================
# Main Program Entry
# ==================================================

if __name__ == "__main__":
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Cleaning up resources...")
        # Add any cleanup code here if necessary
