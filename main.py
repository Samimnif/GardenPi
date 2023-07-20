"""
author: Sami Mnif

main.py is the main script where it uses all other modules to control the 
sensors and motor
"""
import RPi.GPIO as GPIO
import time
from soil_moisture import *
from pump import *
from temperature import *
from camera import *
from screen import *
from movementSens import *
from remote import *
from send import *
import schedule
import logging

wateringD = 15
data = {'temp': 0, 'hum': 0, 'lastw': '', 'soil': 0,
        'delay': wateringD, 'movement': False}


def watering() -> None:
    """
    watering function utilizes the water pump, display, camera and the rf transmitter.
    """
    wateringD = getWaterD()
    initializeS()  # initializes the screen to be able to display message
    displayS('\n\nWatering in process\nDuration: ' + str(wateringD))
    # pumping water with delay (in seconds) stored in wateringD
    pump_on(wateringD)
    displayS('\n\nWatering in process\nDuration: ' +
             str(wateringD) + '\n    Done !')
    info()  # displaying info about this project on screen
    data['lastw'] = time.strftime('%d/%m @ %H:%M')
    data['temp'] = get_temp()[0]
    data['hum'] = get_temp()[1]
    data['soil'] = getSoil_status(14)
    send(str(data))  # sending data over rf transmitter
    # taking picture with camera
    takePicture(str(time.strftime('D %d-%m@%H:%M')))


if __name__ == '__main__':
    try:
        schedule.every().day.at("08:00").do(watering)  # create a scheduled action
        # starting with testing the project components to make sure verything works at startup
        initializeS()
        displayS('Testing Componenets\n')
        time.sleep(1)
        displayS('Testing Componenets\nTemperature Sensor: ' +
                 str(get_temp()[0]) + 'C,' + str(get_temp()[1]))
        time.sleep(1)
        displayS('Testing Componenets\nTemperature Sensor: ' +
                 str(get_temp()[0]) + 'C,' + str(get_temp()[1]) + '\nPump test:')
        pump_on(5)
        displayS('Testing Componenets\nTemperature Sensor: ' +
                 str(get_temp()[0]) + 'C,' + str(get_temp()[1]) + '\nPump test: Done')
        time.sleep(1)
        displayS('Testing Componenets\nTemperature Sensor: ' + str(get_temp()
                                                                   [0]) + 'C,' + str(get_temp()[1]) + '\nPump test: Done\nSoil Test:')
        time.sleep(0.5)
        displayS('Testing Componenets\nTemperature Sensor: ' + str(get_temp()[0]) + 'C,' + str(
            get_temp()[1]) + '\nPump test: Done\nSoil Test:' + str(getSoil_status(14)))
        time.sleep(2)
        displayS('Testing Componenets\nP2\nMovement Test:')
        time.sleep(1)
        displayS('Testing Componenets\nP2\nMovement Test:' + str(msensor(21)))
        time.sleep(2)
        statusShow(str(get_temp()[0]), str(
            getSoil_status(14)), time.strftime('%d @%H:%M'))
        # end of testing

        while True:
            schedule.run_pending()  # checking if it is time to run the action of watering
            print('Start remote check')
            remoteCheck()  # checks for remote control signals
            print('soil test')
            if getSoil_status(14) == 0:  # checks if the soil is dry
                watering()  # waters it if dry
                statusShow(str(data['temp']) + 'C, ' + str(data['hum']), str(
                    data['soil']), str(data['lastw']))  # dislaying garden status
            print('movement')
            if msensor(21) == True:  # checking the motin sensor for any movement
                # take a picture for future reference
                takePicture(str(time.strftime('%d-%m@%H:%M')))
                info()  # displaying info about the garden project on the screen
                data['movement'] = True
                send(str(data))  # sends data through rf transmitter
                data['movement'] = False
            print('temp')
            if get_temp()[0] >= 40:  # checking the temperature of the area
                data['temp'] = get_temp()[0]
                data['hum'] = get_temp()[1]
                # will send data information through rf transmitter
                send(str(data))
    except Exception as Argument:
        # catching errors and saving them in a log.txt for future reference
        f = open("log.txt", "a")
        f.write(time.strftime('%H:%M : ') + str(Argument) + '\n')
        f.close()
