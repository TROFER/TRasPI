import core

__all__ = ["PowerMenu"]

core.asset.Template("std::power", path="powermenu.template")
core.asset.Image("std::powericon", path="power.icon")
core.asset.Image("std::restarticon", path="restart.icon")

class PowerMenu(core.render.Window):

    template = core.asset.Template("std::power")

    def __init__(self):
        self.index = 2
        self.functions = {0: core.hardware.Power.halt, 1: core.hardware.Power.restart, 2: self.finish}
        # Elements
        self.title = core.element.Text(core.Vector(3, 5), "Power Options", justify="L")
        self.powericon = core.element.Image(core.Vector(20, 20), core.asset.Image("std::powericon"))
        self.restarticon = core.element.Image(core.Vector(40, 20), core.asset.Image("std::restarticon"))
        self.options = [core.element.TextBox(core.Vector(20, 30), "Turn Off", rect_colour=1),
        core.element.TextBox(core.Vector(40, 30), "Restart", rect_colour=1),
        core.render.element.TextBox(core.Vector(110, 50), "Cancel", rect_colour=0)]

    def render(self):
        for option in self.options:
            option.render()
        self.powericon.render(), self.restarticon.render()
        self.title.render()

    def up(self):
        if self.index + 1 < 2:
            self.options[self.index].rect.colour = 1
            self.index += 1
            self.options[self.index].rect.colour = 0

    def down(self):
        if self.index > 0:
            self.options[self.index].rect.colour = 1
            self.index -=1
            self.options[self.index].rect.colour = 0

    def select(self):
        func = self.functions[self.index]
        func()

class Handle(core.render.Handler):

    key = core.render.Button.RIGHT
    window = PowerMenu

    def press(self):
        self.window.up()

class Handle(core.render.Handler):

    key = core.render.Button.LEFT
    window = PowerMenu

    def press(self):
        self.window.up()
