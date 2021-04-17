import core
import time

from .app import App
from . import panels

class Home(core.render.Window):

    def __init__(self):
        super().__init__()
        self.status = core.element.Text(core.Vector(127, 5), f"{core.hw.Battery.percentage()}% {time.strftime(App.const.time)}", justify='R')

        self.panel = 0
        self.panels = [panels.WorldClock(), panels.HWInfo(), panels.Weather()]

        self.index = 0
        self.cursor = core.element.Text(core.Vector(0, 0), ">", justify='R')
        self.app_map = [
            core.sys.load.app("home", "loader", default=True),
            core.sys.load.app("home", "settings", default=True), # Settings - Placeholder
            core.sys.load.app("home", "power", default=True),
            core.sys.load.app("home", "manager", default=True),
        ]

        self.buttons = [
            core.element.TextBox(core.Vector(127, 18), "Run Program", justify='R'),
            core.element.TextBox(core.Vector(127, 31), "Settings", justify='R'),
            core.element.TextBox(core.Vector(127, 44), "Power Ctrl", justify='R'),
            core.element.TextBox(core.Vector(127, 57), "Task Mngr", justify='R'),
        ]

        self.elements = {
            core.element.Text(core.Vector(3, 5), f"{core.sys.var.name}", justify='L'),
            core.element.Line(core.Vector(0, 10), core.Vector(128, 10)),
        }

        App.interval(self.refresh)

    def render(self):
        for element in (*self.elements, self.status, self.cursor, *self.buttons):
            core.Interface.render(element)
        self.panels[self.panel].render()

    def move_cursor(self):
        self.cursor.anchor = self.buttons[self.index].pos + core.Vector(-2, 4)

    def refresh(self):
        self.status.text = f"{core.hw.Battery.percentage()}% {time.strftime(App.const.time)}"
        self.panels[self.panel].refresh()

    async def show(self):
        core.hw.Backlight.fill(core.sys.var.colour)
        core.hw.Key.all()
        self.move_cursor()
        self.refresh()

class Handle(core.input.Handler):

    window = Home

    class press:
        async def down(null, window: Home):
            if window.index < len(window.app_map)-1:
                window.index += 1
                window.move_cursor()

        async def up(null, window: Home):
            if window.index > 0:
                window.index -= 1
                window.move_cursor()

        async def centre(null, window: Home):
            core.Interface.program(window.app_map[window.index])

        async def left(null, window: Home):
            window.panel = (window.panel - 1) % len(window.panels)
            window.refresh()

        async def right(null, window: Home):
            window.panel = (window.panel + 1) % len(window.panels)
            window.refresh()

App.window = Home
main = App