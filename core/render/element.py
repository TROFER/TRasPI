from core.render.window import Element, Vector
from core.render.renderer import Render
from core.asset.font import Font
from core.asset.image import Image

__all__ = ["Text"]

class Text(Element):

    def __init__(self, pos: Vector, text="Default Text", font="std", size=11, colour=0, justify='C'):
        super().__init__(pos)
        self._text, self._size, self.colour, self.justify, self._font = str(text), size, colour, justify, Font(font, size)
        self.pos = pos

    def render(self):
        self.Render.draw.text(self.pos_abs, self._text, self.colour, self._font.font)

    def font(self, name=None) -> Font:
        if name is not None:
            self._font = Font(name, self._size)
        return self.font

    def text(self, text=None):
        if text is not None:
            self._text = str(text)
            self.pos = self.pos
        return self._text

    def size(self, size=None):
        if name is not None:
            self._size = size
            self.pos = self.pos
        return self._size

    def _offset(self, value: Vector):
        fs = self.font_size()
        if self.justify == "L":
            return Vector(value[0], value[1] - fs[1] // 2)
        elif self.justify == "R":
            return Vector(value[0] - fs[0], value[1] - fs[1] // 2)
        else:
            self.justify = "C"
            return value - fs // 2

    def font_size(self):
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
        super().__init__(pos, str(self._func(self._value)), *args, **kwargs)

    def value(self, value=None):
        if value is not None:
            for element in self._hook[self]:
                element._set_value(value)
        return self._value

    def _set_value(self, value):
        self._value = value
        self.text(str(self._func(self._value)))

class TextBox(Text):

    def __init__(self, pos: Vector, *args, rect_colour=0, fill=None, width=1, **kwargs):
        self.rect = Rectangle(pos-Vector(2, 0), Vector(1, 1), rect_colour, fill, width)
        super().__init__(pos, *args, **kwargs)

    def _offset(self, value: Vector):
        value = super()._offset(value)
        self.rect.pos = value
        self.rect.pos_2 = self.font_size()
        return value

    def render(self):
        super().render()
        self.rect.render()

class Rectangle(Element):

    def __init__(self, pos1, pos2, colour=0, fill=None, width=1, rel=True):
        super().__init__(pos1)
        self.colour, self.fill = colour, fill
        self.width = width
        self.rel = rel
        self.pos_2 = pos2

    @property
    def pos_2(self):
        return self._pos_2

    @pos_2.setter
    def pos_2(self, value: Vector):
        if self.rel:
            self._pos_2 = vec
            self._abs_2 = self.pos + vec
        else:
            self._pos_2 = value - self.pos
            self._abs_2 = value

    def render(self):
        self.Render.draw.rectangle([*self.pos_abs, *self._abs_2], self.fill, self.colour, self.width)

class Image(Element):

    def __init__(self, pos: Vector, image: Image, justify=True):
        super().__init__(pos)
        self.image = image
        self.justify = justify
        self.pos = pos

    def _offset(self, value: Vector):
        if self.justify:
            return value - Vector(*self.image.image.size) // 2
        return value

    def render(self):
        self.Render.image.paste(self.image.image, tuple(self.pos_abs))
