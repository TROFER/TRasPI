import serial
import json
import core

class SerialWindow(core.render.Window):

    def __init__(self):
        self.command = None
        with open("codes.json", 'r') as codes:
            self.codes = json.load(codes)
        while self.comand != "Return":
            self.command = super().__init__(**self.codes)
        self.finish()

main = SerialWindow()
