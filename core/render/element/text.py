from core.vector import Vector
from core.render.primative import Primative
from core.asset.font import Font
from core.asset.std import AssetPool as std

__all__ = ["Text"]

class Text(Primative):

    def __init__(self, anchor: Vector, text: str="Default Text", font: Font=std.font, colour: int=0, justify: str='C'):
        super().__init__()
        self.anchor = anchor
        self.text, self.colour, self.justify, self.font = str(text), colour, justify, font
        self._calc_pos()

    def render(self, image: "PIL.ImageDraw.ImageDraw"):
        image.text(self.pos, self.text, self.colour, self.font.font)

    def copy(self):
        return self.anchor, self.text, self.colour, self.justify, self.font

    def volatile(self):
        self.text = str(self.text)
        self._calc_pos()

    def _calc_pos(self) -> Vector:
        fs = self._font_size()
        self.justify = self.justify.upper()
        if self.justify == "L":
            self.pos = Vector(self.anchor[0], self.anchor[1] - fs[1] // 2)
        elif self.justify == "R":
            self.pos = Vector(self.anchor[0] - fs[0], self.anchor[1] - fs[1] // 2)
        else:
            self.justify = "C"
            self.pos = self.anchor - fs // 2

    def _font_size(self):
        return Vector(*self.font.text_pixel_size(self.text))

