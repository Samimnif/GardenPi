"""
author: Sami Mnif

This module is to control the IR receiver and setup actions for specific buttons on the remote
"""
import RPi.GPIO as GPIO
from datetime import datetime
import time
from screen import *
from pump import *
from camera import *
import json
import logging

jsonF = "data.json"

# Static program vars
pin = 26  # Input pin of sensor (GPIO.BOARD) 37
Buttons = [0x300ffa25d, 0x300ff629d, 0x300ffe21d, 0x300ff22dd, 0x300ff02fd, 0x300ffc23d, 0x300ffe01f, 0x300ffa857, 0x300ff906f,
           0x300ff9867, 0x300ff6897, 0x300ffb04f, 0x300ff38c7, 0x300ff18e7, 0x300ff4ab5, 0x300ff10ef, 0x300ff5aa5]  # HEX code list
ButtonsNames = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "*", "#",
                "ok", "up", "down", "left", "right"]  # String list in same order as HEX list

# Sets up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN)

# Gets binary value


def getWaterD():
    file = open(jsonF, "r")
    json_obj = json.load(file)
    print(json_obj)
    file.close()
    return json_obj['w']


def changeWaterD(newNum):
    try:
        with open(jsonF, "r+") as file:
            displayS('opening json file')
            data = json.load(file)
            dictation = {"w": newNum}
            data.update(dictation)
            displayS('updated')
            file.seek(0)
            displayS('finalizing')
            json.dump(data, file, indent=4)
            displayS('done')
    except Exception as Argument:
        displayS(str(Argument))


def getBinary():
    # Internal vars
    num1s = 0  # Number of consecutive 1s read
    binary = 1  # The binary value
    command = []  # The list to store pulse times in
    previousValue = 0  # The last value
    value = GPIO.input(pin)  # The current value
    count = 0

    # Waits for the sensor to pull pin low
    while value:
        # sleep(0.0001) # This sleep decreases CPU utilization immensely
        value = GPIO.input(pin)
        count += 1
        if count > 100000:
            break

    # Records start time
    startTime = datetime.now()

    while True:
        # If change detected in value
        if previousValue != value:
            now = datetime.now()
            pulseTime = now - startTime  # Calculate the time of pulse
            startTime = now  # Reset start time
            # Store recorded data
            command.append((previousValue, pulseTime.microseconds))

        # Updates consecutive 1s variable
        if value:
            num1s += 1
        else:
            num1s = 0

        # Breaks program when the amount of 1s surpasses 10000
        if num1s > 10000:
            break

        # Re-reads pin
        previousValue = value
        value = GPIO.input(pin)

    # Converts times to binary
    for (typ, tme) in command:
        if typ == 1:  # If looking at rest period
            if tme > 1000:  # If pulse greater than 1000us
                binary = binary * 10 + 1  # Must be 1
            else:
                binary *= 10  # Must be 0

    if len(str(binary)) > 34:  # Sometimes, there is some stray characters
        binary = int(str(binary)[:34])

    return binary

# Convert value to hex


def convertHex(binaryValue):
    tmpB2 = int(str(binaryValue), 2)  # Temporarely propper base 2
    return hex(tmpB2)


def messageF(delay: str) -> str:
    """
    a function that returns the full message with the delay parameter
    """
    return 'Options| *:Save+Quit,\n#:change delay, OK:pump,\nDown: clear Delay, Up: show delay\nEntered delay:' + delay + '\nReceiving Remote Signals\n'


def remoteCheck() -> None:
    """
    remoteCheck function checks for remote signals.
    If the remote mode is started (by pressing '*' button), then you can run
    different actions like changing the duration of the usual water pump
    or pumping water for a specific time without changing the current duration settings
    or can take picture by a push of button('right' button)
    """
    count = 0
    message = 'Options\n*:Save, \#:Change, OK:pump\nReceiving Remote Signals\n'
    delay = ''
    start = False
    end = False
    while True:
        print(str(count) + ' remote')
        # Runs subs to get incoming hex value
        inData = convertHex(getBinary())
        print(inData)
        for button in range(len(Buttons)):
            if hex(Buttons[10]) == inData and start == False:  # Checks if '*' is pressed
                print('into remote')
                delay = ''
                message = 'Options| *:Save+Quit,\n#:change delay, OK:pump,\nDown: clear Delay, Up: show delay\nEntered delay:' + \
                    delay + '\nReceiving Remote Signals\n'
                start = True
                message += ButtonsNames[10]
                initializeS()
                displayS(message)
                break
            # if '*' is pressed while the remote mode is on
            elif hex(Buttons[10]) == inData and start == True:
                start = False
                message = '\nEnd of Remote'
                displayS(message)
                time.sleep(2)
                info()
                print('done remote')
                end = True
                break
            # checks if 'OK' is pressed
            elif hex(Buttons[12]) == inData and start == True and delay != '':
                message = '\nEnd of Remote\nPumping water for:' + delay + 's'
                print('pump on' + message)
                displayS(message)
                pump_on(int(delay))
                clear()
                info()
                start = False
                end = True
                break
            # checks for number buttons input
            elif hex(Buttons[button]) == inData and start == True:
                if button >= 0 and button <= 9:
                    delay += ButtonsNames[button]
                message = messageF(delay) + ButtonsNames[button]
                displayS(message)
                break
            # checks for if '#' is pressed
            elif hex(Buttons[11]) == inData and start == True and delay != '':
                changeWaterD(int(delay))
                displayS('Changed delay time\nto ' + str(getWaterD()
                                                         ) + '\nPress * to end ,or\nEnter numbers.')
                break
            # checks if 'up' is pressed
            elif hex(Buttons[13]) == inData and start == True:
                displayS('Current General Delay:\n' + str(getWaterD()
                                                          ) + '\nPress * to end ,or\nEnter numbers.')
                break
            # checks if 'down' is pressed
            elif hex(Buttons[14]) == inData and start == True:
                delay = ''
                displayS('Current delay cleared\nEnter numbers')
                break
            # checks if 'right' is pressed
            elif hex(Buttons[16]) == inData and start == True:
                displayS('\nTaking a picture!\nSmile :)')
                takePicture(str(time.strftime('M %d-%m@%H:%M')))
                displayS('\nPicture Saved!')
                break
        if start == False:  # counting number of trys if the remote mode isn't started
            count += 1
        if count >= 5 and start == False or end == True:  # stops the check after 5 trys
            print('break')
            break


# testing
if __name__ == '__main__':
    remoteCheck()
