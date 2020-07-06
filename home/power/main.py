import core
import time
TIME_FORMAT = "%I:%M%p"

class App(core.type.Application):
    name = "Power Controls"

    class asset(core.asset.Pool):
        halt = core.asset.Image("halt")
        restart = core.asset.Image("restart")

class WindowPower(core.render.Window):

    def __init__(self):
        super().__init__()
        self.index = 2
        self.time = core.element.Text(core.Vector(127, 5), time.strftime(TIME_FORMAT), justify="R")

        self.func_map = [core.hw.Power.halt, core.hw.Power.restart, self.finish]
        self.buttons = [
            core.element.TextBox(core.Vector(32, 40), "Turn Off", line_col=1),
            core.element.TextBox(core.Vector(94, 40), "Restart", line_col=1),
            core.element.TextBox(core.Vector(94, 56), "Cancel", line_col=0),
        ]

        self.elements = {
            core.element.Text(core.Vector(3, 5), "Power Ctrl", justify="L"),
            self.time,
            core.element.Line(core.Vector(0, 10), core.Vector(128, 10)),
            core.element.Image(core.Vector(32, 22), App.asset.halt),
            core.element.Image(core.Vector(94, 22), App.asset.restart),
            *self.buttons,
        }

        App.interval(self.refresh)

    def render(self):
        for element in self.elements:
            core.Interface.render(element)

    def refresh(self):
        self.time.text = time.strftime(TIME_FORMAT)

class Handle(core.input.Handler):

    window = WindowPower

    class press:
        async def right(null, window: WindowPower):
            if window.index < len(window.func_map)-1:
                window.buttons[window.index].rect.outline = 1
                window.index += 1
                window.buttons[window.index].rect.outline = 0

        async def left(null, window: WindowPower):
            if window.index > 0:
                window.buttons[window.index].rect.outline = 1
                window.index -= 1
                window.buttons[window.index].rect.outline = 0

        async def centre(null, window: WindowPower):
            window.func_map[window.index]()

App.window = WindowPower
main = App