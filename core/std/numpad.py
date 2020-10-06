from ..render.window import Window
from ..asset import Template
from ..interface import Interface
from ..input.event import Handler
from ..render.element import Text
from ..vector import Vector

__all__ = ["Numpad"]

class Numpad(Window):

    template = Template("window")

    def __init__(self, min, max, default=None, title="Numpad"):
        super().__init__()
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
        async def up(null, window: Numpad):
            if not window.step * 10 > window.max:
                window.step *= 10
                window.refresh()

        async def down(null, window: Numpad):
            if not window.step // 10 < 1:
                window.step //= 10
                window.refresh()

        async def left(null, window: Numpad):
            if window.number - window.step >= window.min:
                window.number -= window.step
                window.refresh()

        async def right(null, window: Numpad):
            if window.number + window.step <= window.max:
                window.number += window.step
                window.refresh()

        async def centre(null, window: Numpad):
            window.finish(window.number)
