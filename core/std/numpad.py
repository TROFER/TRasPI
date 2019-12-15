import core

__all__ = ["Numpad"]

class Numpad(core.render.Window):

    def __init__(self, min, max, default=None):
        if default is None:
            default = min
        self.min, self.max, self.default = min, max, default
        self.step = 1
        self.selected_number = core.render.element.TextContainer(core.Vector(64, 32), default)
        self.left_step = core.render.element.Text(core.Vector(3, 32), f"-{self.step}", justify='L')
        self.right_step = core.render.element.Text(core.Vector(125, 32), f"+{self.step}", justify='R')

    def render(self):
        self.selected_number.render()
        self.left_step.render(), self.right_step.render()

    def add(self):
        if not self.selected_number.value() + self.step > self.max:
            self.selected_number.value(self.selected_number.value() + self.step)
        else:
            self.selected_number.value(self.max)

    def subtract(self):
        if not self.selected_number.value() - self.step < self.min:
            self.selected_number.value(self.selected_number.value() - self.step)
        else:
            self.selected_number.value(self.min)

    def units_up(self):
        if not self.step * 10 > self.max:
            self.step *= 10
            self.left_step.text(f"-{self.step}")
            self.right_step.text(f"+{self.step}")

    def units_down(self):
        if not self.step // 10 < 1:
            self.step //= 10
            self.left_step.text(f"-{self.step}")
            self.right_step.text(f"+{self.step}")

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
