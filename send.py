"""
author: Sami Mnif

this modeul uses the rf transmitter module to tranbsmit data through 433MHz radio
waves.
"""
import sys
import tty
import termios
import threading
import time
from rpi_rf import RFDevice

tx = RFDevice(22)
tx.enable_tx()


def send(text: str) -> None:
    """
    uses the rf module to send string text data by converting each
    character to their Unicode number representation.
    """
    for i in text:
        tx.tx_code(ord(i))
        print(i)
