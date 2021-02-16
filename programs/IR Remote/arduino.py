import json
import os
import serial
import time
from core.hw.key import Key

from app import App


class Arduino:

    TIMEOUT = 2

    def __init__(self):
        self.arduino = serial.Serial(
            port=App.const.Port, baudrate=App.const.Baudrate, timeout=App.const.Timeout)
        time.sleep(0.3)

    def receiveIR(self):
        self.arduino.reset_input_buffer()
        self.arduino.write(bytes("<0>", "UTF-8"))
        for i in range(self.TIMEOUT):
            res = self.arduino.readline().rstrip().decode("UTF-8")
            if len(res) > 0:
                Key.flash(speed=0.1)
                values = ""
                for char in res.split("=")[1]:
                    if char.isnumeric() or char == ",":
                        values += char
                self.arduino.reset_input_buffer()
                return values.split(",")
            time.sleep(1)
        raise IOError

    def sendIR(self, values):
        self.arduino.write(bytes(f"<{len(values)}>", "UTF-8"))
        for value in values:
            self.arduino.write(bytes(f"<{value}>", "UTF-8"))

try:
    Arduino = Arduino()
except serial.SerialException:
    Arduino = FileNotFoundError