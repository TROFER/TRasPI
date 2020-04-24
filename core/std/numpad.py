from core.render.window import Window
from core.asset import Template
from core.interface import Interface
from core.input.event import Handler
from core.render.element import Text
from core.vector import Vector


class Numpad(Window):

    template = Template("window.template")

    def __init__(self, min, max, default=None, title="Numpad"):
        if default is None:
            default = min
        self.min, self.max, self.number, self.step = min, max, default, 1
        self.elements = [
            Text(Vector(64, 16), title[0:18]),
            Text(Vector(64, 32), self.number),  # Selected Number
            Text(Vector(3, 48), f"-{self.step}"),  # Step Left
            Text(Vector(125, 48), f"+{self.step}", justify='R')  # Step Right
        ]

        def render(self):
            for element in self.elements:
                Interface.render(element)

        def refresh(self):
            self.elements[1].text = self.number
            self.elements[2].text = f"-{self.step}"
            self.elements[3].text = f"+{self.step}"


class Handle(Handler):

    window = Numpad

    class press:
        async def up(window):
            if not window.step * 10 > window.max:
                window.step *= 10
                window.refresh()

        async def down(window):
            if not window.step // 10 < 1:
                window.step //= 10
                window.refresh()

        async def left(window):
            if window.number - window.step >= window.min:
                window.number -= window.step
                window.refresh()

        async def right(window):
            if window.number + window.step <= window.max:
                window.number += window.step
                window.refresh()

        async def centre(window):
            window.finish(window.number)
