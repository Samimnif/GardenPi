"""
author: Sami Mnif

this module uses the soil moisture sensor to be able to get the soil
status (dry or wet)
"""
import RPi.GPIO as GPIO


def getSoil_status(pin: int) -> int:
    """
    initializes the pin and reads the data from the sensor.
    If the soil is wet then returns 1, if it is dry then retruns 0
    """
    GPIO.setup(pin, GPIO.IN)
    return GPIO.input(pin)
