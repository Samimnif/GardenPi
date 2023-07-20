"""
author: Sami Mnif

this module is to control the motion sensor.
"""
import RPi.GPIO as GPIO
import time


def msensor(sensor: int) -> bool:
    """
    msensor will use the motion sensor connected on pin 'sensor'.
    the output will be either True (if it detects movement) or False.
    """
    GPIO.setup(sensor, GPIO.IN)
    if GPIO.input(sensor):
        return True
    return False

