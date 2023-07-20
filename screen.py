"""
author: Sami Mnif

this module is to control the e-paper screen.
the code is based on teh manufactures library 'waveshare'.
The functions in this file is to help display some needed messages.
"""
#!/usr/bin/python
# -*- coding:utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
import traceback
import time
from waveshare_epd import epd2in13_V3
import logging
import sys
import os
picdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(
    os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)


def statusShow(temperature, soil, lastWater):
    """
    shows the status of the garden by displaying the parameters
    """

    epd = epd2in13_V3.EPD()
    epd.init()
    epd.Clear(0xFF)

    # Drawing on the image
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 20)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

    logging.info("1.Drawing on the image...")
    image = Image.new('1', (epd.height, epd.width),
                      255)  # 255: clear the frame
    draw = ImageDraw.Draw(image)

    draw.rectangle([(0, 0), (150, 29)], outline=0)

    draw.text((1, 1), time.strftime('%d %a %H:%M'), font=font24, fill=0)
    draw.text((1, 30), 'Temperature: ' +
              str(temperature), font=font15, fill=0)
    draw.text((2, 50), 'Soil Status:' + str(soil), font=font15, fill=0)
    draw.text((2, 70), 'Last Time Watered:\n' +
              str(lastWater), font=font15, fill=0)
    epd.display(epd.getbuffer(image))
    time.sleep(2)
    epd.sleep()


def info():
    """
    displays the information about the project
    includes a qr code to my website
    """

    epd = epd2in13_V3.EPD()
    epd.init()
    epd.Clear(0xFF)

    # Drawing on the image
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 16)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

    logging.info("1.Drawing on the image...")
    image = Image.new('1', (epd.height, epd.width),
                      255)  # 255: clear the fram>
    draw = ImageDraw.Draw(image)

    draw.text((1, 1), "Hi fellow gardner! My name is Sami \nand I am a student engineer.\nThis is my garden project\nScan the QR Code for more info!", font=font15, fill=0)
    # epd.display(epd.getbuffer(image))
    # image1 = Image.new('1', (epd.height, epd.width), 255)  # 255: clear the fr>
    bmp = Image.open(os.path.join(picdir, 'qr.bmp'))
    image.paste(bmp, (90, 75))
    epd.display(epd.getbuffer(image))

    epd.sleep()


def initializeS() -> None:
    """
    code to initialize the screen and clearing the contents
    """
    epd = epd2in13_V3.EPD()
    epd.init()
    epd.Clear(0xFF)


def clear() -> None:
    """
    clearing the contents
    """
    epd = epd2in13_V3.EPD()
    epd.Clear(0xFF)
    epd.sleep()


def displayS(message: str) -> None:
    """
    displaying the message in the parameter
    """
    epd = epd2in13_V3.EPD()
    font15 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 17)
    font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)

    logging.info("1.Drawing on the image...")
    image = Image.new('1', (epd.height, epd.width),
                      255)  # 255: clear the fram>
    draw = ImageDraw.Draw(image)
    draw.text((1, 1), str(message), font=font15, fill=0)
    epd.displayPartial(epd.getbuffer(image))


# testing
if __name__ == "__main__":
    statusShow(10, 1, time.strftime('%d @ %H:%M'))
    time.sleep(2)
    info()
    initializeS()
    displayS('Hello')
    time.sleep(0.5)
    displayS('Hello My name is ')
    time.sleep(0.5)
    displayS('Hello My name is Sami')
    time.sleep(3)
    clear()
