import core

__all__ = ["Numpad"]

class Numpad(core.render.Window):

    template = f"{core.sys.PATH}core/resource/template/numpad.template"

    def __init__(self, min, max, default=None, title="Numpad"):
        if default is None:
            default = min
        self.min, self.max, self.default = min, max, default
        self.selected_number = core.render.element.TextContainer(core.Vector(64, 32), default)
        self.step = core.render.element.TextContainer(core.Vector(125, 48), 1, justify='R', func=lambda v: "+"+str(v))
        self.step_l = core.render.element.TextContainer(core.Vector(3, 48), self.step, justify='L', func=lambda v: "-"+str(v))
        self.title = core.render.element.Text(core.Vector(64, 16), title, size=11)#Font: 8

    def render(self):
        self.selected_number.render()
        self.step.render(), self.step_l.render()
        self.title.render()

    def add(self):
        if not self.selected_number.value() + self.step.value() > self.max:
            self.selected_number.value(self.selected_number.value() + self.step.value())
        else:
            self.selected_number.value(self.max)

    def subtract(self):
        if not self.selected_number.value() - self.step.value() < self.min:
            self.selected_number.value(self.selected_number.value() - self.step.value())
        else:
            self.selected_number.value(self.min)

    def units_up(self):
        if not self.step.value() * 10 > self.max:
            self.step.value(self.step.value() * 10)

    def units_down(self):
        if not self.step.value() // 10 < 1:
            self.step.value(self.step.value() // 10)

class Handle(core.render.Handler):

    key = core.render.Button.UP
    window = Numpad

    def press(self):
        self.window.units_up()

class Handle(core.render.Handler):

    key = core.render.Button.DOWN
    window = Numpad

    def press(self):
        self.window.units_down()

class Handle(core.render.Handler):

    key = core.render.Button.LEFT
    window = Numpad

    def press(self):
        self.window.subtract()

class Handle(core.render.Handler):

    key = core.render.Button.RIGHT
    window = Numpad

    def press(self):
        self.window.add()

class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = Numpad

    def press(self):
        self.window.finish(self.window.selected_number.value())
