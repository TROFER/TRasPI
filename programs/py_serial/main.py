import serial
import json
import os
import core

@core.render.Window.focus
def write_code(element, window):
    try:
        port = window.serial # Grabs attributes from serialmenu
        port.write(element.data.encode()) #NEEDS TO BE CONVERTED TO BINARY
    except Exception as e:
        raise # REMOVE THIS WHEN YOU KNOW WHAT TYPE OF ERROR YOU GET, thanks <3
        yield core.std.Error(str(e))
    #send(code)

class SerialMenu(core.std.Menu):

    def __init__(self):

        self.serial = None

        with open(f"{core.sys.PATH}programs/py_serial/codes.json", "r") as file:
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
                self.serial = serial.Serial(port, baudrate=9600, stopbits=1)
                break
        except IOError:
            yield core.std.Error("Port Error")
            self.finish()


'''
class SerialWindow(core.render.Window):

    core.hardware.Backlight.fill(225, 225, 225)

    def send(code)
        self.port
        serial.write(code)


    @core.render.Window.focus
    def __init__(self):
        # I think the problem with the core.std.Error is cause this is happening in the __init__ and thats returning nothing and so the window gets really messed up
        # The way to fix this probelm is to override the self.show() func and do this stuff there cause that wouldn't mess with the creation of the object
        # I orginialy started this in the same way as torch works where a menu is called at the begining, however I could not open the menu, as I would like it to run a function and  pass the related serial code as an argument and just tried to run some code instead
        # So you want to make a menu using the core.std.Menu but don't know how to get it to run a func when you click on the item in the menu?
        # Yes, I would like to pass the hex code and its name which is in the json data

        # I can show you how to subclass the core.std.Menu and set one up?
        # Ok do you want to use discord because its easylol
        # Might be eaiser than typing .... xd
        # I will have to try build a gui then, the idea is that I can use a USB to serial converter to send various codes to an old projector
        print("Checking for open ports") #Im not sure how raspbery / linux handles serial stuff so im trying to open all ports
        try: # If you have any idea let me know lol
            self.ports = os.listdir("/dev")
            for port in self.ports:
                if "tty" not in port:
                    self.ports.remove(port)
        except Exception as error:
            print(error)
            yield core.std.Error(str(error))
        print(f"{self.ports} are open")
        for port in self.ports:
            try:
                self.serial = serial.Serial(port, 9600)
                print(self.serial.portstr)
                self.command = ("BE EF 03 06 00 2A D3 01 00 00 60 00 00").replace(" ", "")
                self.serial.write(self.command.encode())
                self.serial.close()
            except Exception as error:
                print(error)
                yield core.std.Error(str(error))
        print("All ports Checked")
        self.finish()
'''
main = SerialMenu()
