"""
author: Sami Mnif

This module will control the water pump.
"""
import RPi.GPIO as GPIO
import time


def init_output(pin):
    """
    init_output will setup the pin in 'pin' number for use
    """
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    GPIO.output(pin, GPIO.HIGH)


def pump_on(delay):
    """
    pump_on will setup the pin 5 for use and then turn on the pump for 
    'delay' number seconds
    """
    init_output(5)
    GPIO.output(5, GPIO.LOW)
    GPIO.output(5, GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(5, GPIO.LOW)

