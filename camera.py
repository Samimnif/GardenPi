"""
author: Sami Mnif

camera.py is a module that controlls the camera.
It access the camera using the picamera library.
Then it saves it in pi folder.
"""
from picamera import PiCamera
from time import sleep


def takePicture(i: str) -> None:
    """
    takePicture function takes a file name 'i' and saves the picture
    taken by the camera in /home/pi directory with the 'i' name.

    >>> takePicture('newImage')
    # uses the camera module to take picture and saves it as newImage.jpg
    """
    camera = PiCamera()
    camera.start_preview()
    sleep(3)
    camera.capture('/home/pi/' + str(i) + '.jpg')
    camera.stop_preview()
    camera.close()


# Testing
if __name__ == '__main__':
    takePicture('test')
