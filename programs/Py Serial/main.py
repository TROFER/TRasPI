import serial
import json
import os
import core

@core.render.Window.focus
def write_code(element, window):
    try:
        port = window.serial # Grabs attributes from SerialMenu
        port.write(element.data.encode()) #NEEDS TO BE CONVERTED TO BINARY
        yield core.std.Info(str(port.read()))
    except ValueError:
        yield core.std.Error("Bad Write Data")
    except SerialException:
        yield core.std.Error("Device Error")

class SerialMenu(core.std.Menu):

    def __init__(self):

        self.serial = None

        with open(f"{core.sys.PATH}programs/Py Serial/codes.json", "r") as file:
            self.data = json.load(file)

        elements = []

        for key, value in self.data.items():
            elements.append(core.std.Menu.Element(
                core.element.Text(core.Vector(0, 0), key, justify="L"),
                data = value,
                select = write_code))
        super().__init__(*elements, title="Serial Commands")

    @core.render.Window.focus
    def show(self):
        super().show()
        core.hardware.Backlight.fill(225, 225, 225)
        # This function is run when the window is first loaded
        try:
            for port in ["/dev/ttyUSB0", "/dev/ttyAMA0"]:
                self.serial = serial.Serial(port, baudrate=9600, stopbits=1, timeout=10)
                break
        except IOError:
            yield core.std.Error("Port Error")
            self.finish()

main = SerialMenu()
