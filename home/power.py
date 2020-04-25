import time

from core import Vector, asset
from core.asset import Template
from core.hw.power import Power
from core.input import Handler
from core.interface import Interface
from core.render import Window, element
from home.app import App


class Main(Window):

    template = Template("window")
    POWER_HALT = asset.Image("power-halt")
    POWER_RESTART = asset.Image("power-restart")

    def __init__(self):
        self.index = 2 # Default to cancel
        self.map = {Power.halt, Power.restart, self.finish}
        self.elements = [
            element.Text(Vector(3, 5), "Power Options", justify='L'),
            element.Text(Vector(127, 5), time.strftime(
                "%I:%M%p"), justify='R'),
            element.Image(Vector(32, 15), self.POWER_HALT),
            element.Image(Vector(94, 15), self.POWER_RESTART),
            element.TextBox(Vector(32, 40), "Turn Off", line_col=1),
            element.TextBox(Vector(94, 40), "Restart", line_col=1),
            element.TextBox(Vector(100, 57), "Cancel", line_col=0)]
        App.interval(self.refresh)

    def render(self):
        for element in self.elements:
            Interface.render(element)

    def refresh(self):
        print(self.index)
        self.elements[1].text = time.strftime("%I:%M%p")


class Handle(Handler):

    window = Main

    class press:
        async def left(null, window):
            print("if")
            if window.index > 0:
                print("left")
                window.elements[window.index + 3].line_col = 1
                window.index -= 1
                window.elements[window.index + 3].line_col = 0
                print("done")

        async def right(null, window):
            print("if")
            if window.pos < 2:
                print("right")
                window.elements[window.index + 3].line_col = 1
                window.pos += 1
                window.elements[window.index + 3].line_col = 0
                print("done")

        async def centre(null, window):
            print("starting")
            print(window.index)
            window.map[window.index]()
            print(window.index)


main = Main()
