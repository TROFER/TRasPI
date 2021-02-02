import json

import core
from app import App
from core import Vector
from core.hw import Backlight
from core.render.element import Line, Text
from hardware import constrain


class Main(core.render.Window):

    def __init__(self, client):
        super().__init__()
        self.client = client
        self.elements = [Line(Vector(0, 10), Vector(128, 10)),
                          Text(Vector(3, 5),
                               f"{client.SERVER_ADDR} - RAM", justify='L'),
                          Text(Vector(3, 16), "", justify="L"),
                          Text(Vector(3, 24), "", justify="L"),
                          Text(Vector(3, 32), "", justify="L"),
                          Line(Vector(0,  37), Vector(128, 37)),
                          Text(Vector(3, 43), "RAM Load", justify="L"),
                          Line(Vector(3, 48), Vector(125, 48), width=2)]
        self.refresh()
        App.interval(self.refresh, 1.5)
    
    async def show(self):
        Backlight.gradient(App.const.colour, hsv=False)

    def refresh(self):
        self.current = json.loads(self.client.buffer)
        self.elements[2].text = f"RAM Load: {self.current['Memory']['load']}%"
        self.elements[3].text = f"RAM Used: {self.current['Memory']['used']}GB"
        self.elements[4].text = f"RAM Free: {self.current['Memory']['free']}GB"
        self.elements[7].pos2 = Vector(
            constrain(float(self.current["Memory"]["load"]), 1, 100, 3, 125), 48)

    def render(self):
        for element in self.elements:
            core.Interface.render(element)


class Handle(core.input.Handler):

    window = Main

    class press:
        async def right(null, window: Main):
            window.finish(1)

        async def left(null, window: Main):
            window.finish(-1)

        async def down(null, window: Main):
            window.finish()
