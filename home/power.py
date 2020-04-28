import time

from core import Vector, asset
from core.asset import Template
from core.hw.power import Power
from core.input import Handler
from core.interface import Interface
from core.render import Window, element
from home.app import App


class Main(Window):

    POWER_HALT = asset.Image("power-halt")
    POWER_RESTART = asset.Image("power-restart")

    def __init__(self):
        super().__init__()
        self.index = 2  # Default to cancel
        self.map = [Power.halt, Power.restart, self.finish]
        self.elements = [
            element.Text(Vector(3, 5), "Power Ctrl", justify='L'),
            element.Text(Vector(127, 5), time.strftime(
                "%I:%M%p"), justify='R'),
            element.Line(Vector(0, 10), Vector(128, 10)),
            element.Image(Vector(32, 22), self.POWER_HALT),
            element.Image(Vector(94, 22), self.POWER_RESTART),
            element.TextBox(Vector(32, 40), "Turn Off", line_col=1),
            element.TextBox(Vector(94, 40), "Restart", line_col=1),
            element.TextBox(Vector(94, 56), "Cancel", line_col=0)]
        App.interval(self.refresh)

    def render(self):
        for element in self.elements:
            Interface.render(element)

    def refresh(self):
        self.elements[1].text = time.strftime("%I:%M%p")


class Handle(Handler):

    window = Main

    class press:
        async def left(null, window):
            if window.index > 0:
                window.elements[window.index + 5].rect.outline = 1
                window.index -= 1
                window.elements[window.index + 5].rect.outline = 0

        async def right(null, window):
            if window.index < 2:
                window.elements[window.index + 5].rect.outline = 1
                window.index += 1
                window.elements[window.index + 5].rect.outline = 0

        async def centre(null, window):
            window.map[window.index]()


main = Main()
