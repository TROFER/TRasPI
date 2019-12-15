from core.render.window import Element, Vector
from core.render.renderer import Render
from core.render.font import Font
from core.sys import PATH

from PIL import ImageFont

__all__ = ["Text"]

Font("std", PATH+"core/asset/font/bitocra-full.bdf")

class Text(Element):

    def __init__(self, pos: Vector, text="Default Text", font="std", size=11, colour=1, justify='C'):
        super().__init__(pos)
        self._text, self._size, self.colour, self.justify, self._font = str(text), size, colour, justify, Font(font, size)
        self._calc_justify()

    def render(self):
        self.Render.draw.text(self.position, self._text, self.colour, self._font.font)

    def font(self, name=None) -> Font:
        if name is not None:
            self._font = Font(name, self._size)
        return self.font

    def text(self, text=None):
        if text is not None:
            self._text = str(text)
            self._calc_justify()
        return self._text

    def size(self, size=None):
        if name is not None:
            self._size = size
            self._calc_justify()
        return self._size

    def _calc_justify(self):
        fs = Vector(*self._font.font_size(self._text))
        if self.justify == "L":
            self.position = (self.pos[0], self.pos[1] - fs[1] // 2)
        elif self.justify == "R":
            self.position = (self.pos[0] - fs[0], self.pos[1] - fs[1] // 2)
        else:
            self.justify = "C"
            self.position = self.pos - fs // 2

class TextContainer(Text):

    def __init__(self, pos: Vector, default="Text", *args, **kwargs):
        self._value = default
        super().__init__(pos, str(self._value), *args, **kwargs)

    def value(self, value=None):
        if value is not None:
            self._value = value
            self.text(str(self._value))
        return self._value

class Rectangle(Element):

    def __init__(self, pos: Vector, width: int, height: int):
        super().__init__(pos)
        self.width, self.height = width, height

    def render(self):
        self.Render.draw.rect()
