import time

import core
from core import Vector
from core.render.element import Image, Line, Text, TextBox

from app import App
from windows import pool, ticker


class Main(core.render.Window):

    def __init__(self):
        super().__init__()
        self.index = 0
        self.map = [ticker.Main, pool.Main]
        self.elements = [
            Line(Vector(0, 10), Vector(128, 10)),
            Text(Vector(1, 5), "Crypto Tra...", justify="L"),
            Text(Vector(127, 5), time.strftime("%I:%M%p"), justify="R"),
            Image(Vector(32, 18), App.asset.ticker_logo),
            Image(Vector(96, 18), App.asset.pool_logo),
            TextBox(Vector(32, 50), "Prices"),
            TextBox(Vector(96, 50), "Pool Stats", line_col=255)]
        App.interval(self.refresh)
    
    async def show(self):
        core.hw.Backlight.fill([64, 100, 100])

    def render(self):
        for element in self.elements:
            core.Interface.render(element)

    def refresh(self):
        self.elements[2].text = time.strftime("%I:%M%p")


class Handle(core.input.Handler):

    window = Main

    class press:
        async def left(null, window):
            if window.index != 0:
                window.elements[5 + window.index].rect.outline = 255
                window.index -= 1
                window.elements[5 + window.index].rect.outline = 0

        async def right(null, window):
            if window.index != 1:
                window.elements[5 + window.index].rect.outline = 255
                window.index += 1
                window.elements[5 + window.index].rect.outline = 0

        async def centre(null, window):
            await window.map[window.index]()


App.window = Main
main = App
