"""
author: Sami Mnif

this module controls the temperature sensor to get reading about the
temperature and the humidity in the air.
"""
#!/usr/bin/python
# pin 04
import sys
import Adafruit_DHT


def get_temp() -> list:
    """
    gets the reading from the temperature sensor and returns the temperature and 
    the humidity percentage in form of a list [temperature, humidity]
    """
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    return [temperature, humidity]
