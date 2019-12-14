from core.render.window import Element, Vector
from core.render.renderer import Render

import core.render.template
from PIL import ImageFont

__all__ = ["Text"]

class Text(Element):

    def __init__(self, pos: Vector, text="Default Text", size=10, colour=1, justify='C'):
        super().__init__(pos)
        self.text, self.size, self.colour, self.justify = text, size, colour, justify
        set_font(size), get_font_size(), _calc_justify()

    def get_font_size(self):
        self.font_size = self.font.getsize(self.text)

    def set_text(self, text):
        self.text = text
        get_font_size(), _calc_justify()

    def set_font(self, size):
        self.font = ImageFont.truetype(core.render.template.std_font, size)

    def render(self):
        self.Render.draw.text(self.position, self.text, self.colour, self.font)

    def _calc_justify(self):
        if self.justify == "C":
            self.position = (self.pos[0] - (self.font_size[0] // 2), self.pos[1] - (self.font_size[1] // 2))
        elif self.justify == "L":
            self.position = (self.pos[0], self.pos[1] - (self.font_size[1] // 2))
        elif self.justify == "R":
            self.position = (self.pos[0] - self.font_size[0], self.pos[1] - (self.font_size[1] // 2))
        else:
            self.justify = "C"
            self.position = (self.pos[0] - (self.font_size[0] // 2), self.pos[1] - (self.font_size[1] // 2))

class Rectangle(Element):

    def __init__(self, pos: Vector, width: int, height: int):
        super().__init__(pos)
        self.width, self.height = width, height

    def render(self):
        self.Render.draw.rect()
