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
        fs = self._font_size()
        if self.justify == "L":
            self.position = (self.pos[0], self.pos[1] - fs[1] // 2)
        elif self.justify == "R":
            self.position = (self.pos[0] - fs[0], self.pos[1] - fs[1] // 2)
        else:
            self.justify = "C"
            self.position = self.pos - fs // 2

    def _font_size(self):
        return self._font.font_size(self._text)

class TextContainer(Text):

    _hook = {}

    def __init__(self, pos: Vector, default="Text", *args, func=str, **kwargs):
        if isinstance(default, self.__class__):
            self._hook[default].append(self)
            self._hook[self] = self._hook[default]
            default = default._value
        else:
            self._hook[self] = [self]
        self._value = default
        self._func = func
        super().__init__(pos, str(func(self._value)), *args, **kwargs)

    def value(self, value=None):
        if value is not None:
            for element in self._hook[self]:
                element._set_value(value)
        return self._value

    def _set_value(self, value):
        self._value = value
        self.text(str(func(self._value)))

class TextBox(Text):

    def __init__(self, pos: Vector, *args, **kwargs):
        self.rect = Rectangle(pos, Vector(1, 1))
        super().__init__(pos, *args, **kwargs)
        self.rect.colour = self.colour

    def _calc_justify(self):
        super()._calc_justify()
        self.rect.pos = self.position
        self.rect.pos_2(self._font_size())
        self.rect

class Rectangle(Element):

    def __init__(self, pos1, pos2, colour=1, fill=None, width=1, rel=True):
        super().__init__(pos1)
        self.colour, self.fill = colour, fill
        self.width = width
        if not rel:
            self.pos_2 = self._calc_pos
        self.pos_2(pos2)

    def _calc_pos(self, vec: Vector):
        self.pos2 = vec - self.pos
        self._abs_2 = vec

    def pos_2(self, vec: Vector):
        self.pos2 = vec
        self._abs_2 = self.pos + vec

    def render(self):
        self.Render.draw.rectangle([self.pos, self._abs_2], self.fill, self.colour, self.width)
