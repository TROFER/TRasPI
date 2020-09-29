import core
from core.vector import Vector
import time
from core.render.element import Text, Line
from .app import App

TIME_FORMAT = "%I:%M%p"

class Main(core.render.Window):

    self.TREE = {
        "Accounts": {
            "System Name": "name"
        },
        "Display": {
            "Brightness": "brightness",
            "Night Mode": "nightmode_enable"
        },
        "Personalisation": {
            "System Colour": "colour",
            "Time Format" : "timeformat"
        }
    }

    def __init__(self):
        super().__init__()
        self.index = 0
        self.elements = [Text(Vector(64, 3), "Settings"),
        Line(Vector(0, 5), Vector(128, 5)),
        Text(Vector(3, 10), ""),
        Line(Vector(0, 10), Vector(128, 10)),
        Text(Vector(3, 20), ""),
        Line(Vector(0, 20), Vector(128, 20)),
        Text(Vector(3, 30), ""),
        Line(Vector(0, 30), Vector(128, 30)),
        Text(Vector(3, 40), ""),
        Line(Vector(0, 40), Vector(128, 40))]
        
        #setattr(core.sys.var, "name", "value") use this to edit and set attributes
    
    def render(self):
        for element in self.elements:
            core.Interface.render(element)
    
    def show(self):
        pass

    def render(self):
        pass


class Handle(core.input.Handler):

    window = WindowPower

    class press:
        async def right(null, window: WindowPower):
            if window.index < len()

        async def left(null, window: WindowPower):
            if window.index > 0:
                window.index -= 1

        async def centre(null, window: WindowPower):
            window.func_map[window.index]()


App.window = Main
main = App