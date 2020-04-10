import PIL.ImageDraw
import PIL.ImageFont
from core.vector import Vector
from core.render.primative import Primative

__all__ = ["Text"]

_FONT = PIL.ImageFont.load_default()

class Text(Primative):

    def __init__(self, anchor: Vector, text="Default Text", font="std", size=11, colour=0, justify='C'):  # ASSET SYSTEM
        super().__init__()
        self.anchor = anchor
        self.text, self.size, self.colour, self.justify, self.font = str(text), size, colour, justify, font
        self.pos = self._offset(self.anchor)

    def render(self, image: PIL.ImageDraw.ImageDraw):
        image.text(self.pos, self.text, self.colour, _FONT) # font asset

    def copy(self):
        return self.anchor, self.text, self.size, self.colour, self.justify, self.font

    def volatile(self):
        self.text = str(self.text)
        self.pos = self._offset(self.anchor)

    def _offset(self, value: Vector):
        fs = self._fontsize()
        if self.justify == "L":
            return Vector(value[0], value[1] - fs[1] // 2)
        elif self.justify == "R":
            return Vector(value[0] - fs[0], value[1] - fs[1] // 2)
        else:
            self.justify = "C"
            print(value, fs)
            return value - fs // 2

    def _fontsize(self):
        return Vector(*_FONT.getsize(self.text)) # font asset
