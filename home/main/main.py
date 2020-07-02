import core
import time

from .app import App
from . import panels

class WindowHome(core.render.Window):

    def __init__(self):
        super().__init__()
        self.time = core.element.Text(core.Vector(127, 5), time.strftime(App.const.time), justify='R')

        self.panel = 0
        self.panels = [panels.WorldClock(), panels.HWInfo(), panels.Weather()]

        self.index = 0
        self.cursor = core.element.Text(core.Vector(0, 0), ">", justify='R')
        self.app_map = [
            core.sys.load.app("home", "loader"),
            core.sys.load.app("home", "power"), # Settings - Placeholder
            core.sys.load.app("home", "power"),
        ]

        self.buttons = [
            core.element.TextBox(core.Vector(127, 18), "Run Program", justify='R'),
            core.element.TextBox(core.Vector(127, 31), "Settings", justify='R'),
            core.element.TextBox(core.Vector(127, 44), "Power Ctrl", justify='R'),
        ]

        self.elements = {
            core.element.Text(core.Vector(3, 5), f"{core.sys.var.name}", justify='L'),
            core.element.Line(core.Vector(0, 10), core.Vector(128, 10)),
        }

        App.interval(self.refresh)

    def render(self):
        for element in (*self.elements, self.time, self.cursor, *self.buttons):
            core.Interface.render(element)
        self.panels[self.panel].render()

    def move_cursor(self):
        self.cursor.anchor = self.buttons[self.index].pos + core.Vector(-2, 4)

    def refresh(self):
        self.time.text = time.strftime(App.const.time)
        self.panels[self.panel].refresh()

    async def show(self):
        core.hw.Backlight.fill(core.sys.var.colour)
        self.move_cursor()
        self.refresh()

class Handle(core.input.Handler):

    window = WindowHome

    class press:
        async def down(null, window: WindowHome):
            if window.index < len(window.app_map)-1:
                window.index += 1
                window.move_cursor()

        async def up(null, window: WindowHome):
            if window.index > 0:
                window.index -= 1
                window.move_cursor()

        async def centre(null, window: WindowHome):
            core.Interface.program(window.app_map[window.index])

        async def left(null, window: WindowHome):
            window.panel = (window.panel - 1) % len(window.panels)
            window.refresh()

        async def right(null, window: WindowHome):
            window.panel = (window.panel + 1) % len(window.panels)
            window.refresh()

App.window = WindowHome
main = App