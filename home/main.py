import time

import core
from core.hw.backlight import Backlight
from core.input.event import Handler
from core.interface import Interface
from core.render import Window
from core.render.element import Rectangle, Text, TextBox
from core.render.window import Window
from core.sys.attributes import SysConfig
from core.vector import Vector
from home import loader, panels


class App(core.type.Application):
    pass


class MainWindow(Window):

    # template = core.asset.Template("std::window", path="window.template")

    def __init__(self):
        super().__init__()
        self.index = [0, 0]
        self.elements = [
            Text(Vector(3, 5), f"{SysConfig.name}", justify='L'),
            Text(Vector(127, 5), time.strftime("%I:%M%p"), justify='R'),
            Text(Vector(0, 0), ">", justify='R'),
            TextBox(Vector(127, 17), "Run Program", justify='R'),
            TextBox(Vector(127, 30), "Settings", justify='R'),
            TextBox(Vector(127, 43), "Power Ctrl", justify='R')
        ]
        self.panels = panels.panels
        self.map = {0: loader.main}
        App.interval(self.refresh)

    async def show(self):
        Backlight.fill(SysConfig.colour)
        self.refresh()

    def render(self):
        for element in self.elements:
            Interface.render(element)
        self.panels[self.index[1]].render()

    def refresh(self):
        self.elements[1].text = time.strftime("%I:%M%p")
        self.elements[2].anchor = Vector(self.elements[self.index[0] + 3].pos[0] - 2,
                                         self.elements[self.index[0] + 3].pos[1] + 4)
        self.panels[self.index[1]].refresh()


class Handle(Handler):

    window = MainWindow

    class press:
        async def down(null, window):
            if window.index[0] < 2:
                window.index[0] += 1
                window.refresh()

        async def up(null, window):
            if window.index[0] > 0:
                window.index[0] -= 1
                window.refresh()

        async def centre(null, window):
            await(window.map[window.index[0]])
            window.refresh()

        async def left(null, window):
            if window.index[1] > 0:
                window.index[1] -= 1
                window.refresh()

        async def right(null, window):
            if window.index[1] < 2:
                window.index[1] += 1
                window.refresh()


App.window = MainWindow()
main = App
