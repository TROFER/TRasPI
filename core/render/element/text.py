import PIL.ImageFont # font asset
from core.vector import Vector
from core.render.primative import Primative

__all__ = ["Text"]

_FONT = PIL.ImageFont.load_default() # font asset

class Text(Primative):

    def __init__(self, anchor: Vector, text: str="Default Text", font: str="std", size: int=11, colour: int=0, justify: str='C'): # font asset
        super().__init__()
        self.anchor = anchor
        self.text, self.size, self.colour, self.justify, self.font = str(text), size, colour, justify, font
        self._calc_pos()

    def render(self, image: "PIL.ImageDraw.ImageDraw"):
        image.text(self.pos, self.text, self.colour, _FONT) # font asset

    def copy(self):
        return self.anchor, self.text, self.size, self.colour, self.justify, self.font

    def volatile(self):
        self.text = str(self.text)
        self._calc_pos()

    def _calc_pos(self) -> Vector:
        fs = Vector(*_FONT.getsize(self.text)) # font asset
        if self.justify == "L":
            self.pos = Vector(self.anchor[0], self.anchor[1] - fs[1] // 2)
        elif self.justify == "R":
            self.pos = Vector(self.anchor[0] - fs[0], self.anchor[1] - fs[1] // 2)
        else:
            self.justify = "C"
            self.pos = self.anchor - fs // 2

