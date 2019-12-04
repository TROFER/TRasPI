from core.render.window import Element, Vector
from core.render.renderer import Render

import core.render.template
import PIL

__all__ = ["Text"]

class Text(Element):

    def __init__(self, pos: Vector, text):
        super().__init__(pos)
        self.text = text
        self.data = {}
        self.size = 10
        self.colour = 0
        self.font = PIL.ImageFont.truetype(core.render.template.std_font, self.size)
        self.font_size = self.font.getsize(self.text)

    def render(self):
        self.Render.draw.text(self.pos, self.text, self.colour, self.font)

class Rectangle(Element):

    def __init__(self, pos: Vector, width: int, height: int):
        super().__init__(pos)
        self.width, self.height = width, height

    def render(self):
        self.Render.draw.rect()
