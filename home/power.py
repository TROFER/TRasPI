import core
from core.hardware.power import Power

__all__ = ["PowerMenu"]

core.asset.Template("std::power", path="power.template")
core.asset.Image("std::powericon", path="power.icon")
core.asset.Image("std::restarticon", path="restart.icon")

class PowerMenu(core.render.Window):

    template = core.asset.Template("std::power")

    def __init__(self):
        self.index = 2
        self.functions = {0: Power.halt, 1: Power.restart, 2: self.finish}
        R, G, B = colorsys.hsv_to_rgb(core.sys.Config(
            "std::system")["system_colour"]["value"] / 100, 1, 1)
        core.hardware.Backlight.fill(int(R * 255), int(G * 255), int(B * 255))
        # Elements
        self.title = core.element.Text(core.Vector(3, 4), "Power Options", justify="L")
        self.powericon = core.element.Image(core.Vector(32, 25), core.asset.Image("std::powericon"))
        self.restarticon = core.element.Image(core.Vector(94, 25), core.asset.Image("std::restarticon"))
        self.options = [core.element.TextBox(core.Vector(32, 40), "Turn Off", rect_colour=1),
        core.element.TextBox(core.Vector(94, 40), "Restart", rect_colour=1),
        core.element.TextBox(core.Vector(100, 57), "Cancel", rect_colour=0)]

    def render(self):
        for option in self.options:
            option.render()
        self.powericon.render(), self.restarticon.render()
        self.title.render()

    def up(self):
        if self.index + 1 < 3:
            self.options[self.index].rect.colour = 1
            self.index += 1
            self.options[self.index].rect.colour = 0

    def down(self):
        if self.index > 0:
            self.options[self.index].rect.colour = 1
            self.index -=1
            self.options[self.index].rect.colour = 0

    def select(self):
        self.functions[self.index]()

class Handle(core.render.Handler):

    key = core.render.Button.RIGHT
    window = PowerMenu

    def press(self):
        self.window.up()

class Handle(core.render.Handler):

    key = core.render.Button.LEFT
    window = PowerMenu

    def press(self):
        self.window.down()

class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = PowerMenu

    def press(self):
        self.window.select()
