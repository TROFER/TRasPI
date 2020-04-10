import PIL.ImageDraw
from core.render.primative import Primative


class Text(Primative):

    def __init__(self, anchor, text="Default Text", font="std", size=11, colour=0, justify='C'):  # ASSET SYSTEM
        self.text, self.size, self.colour, self.justify, self.font = str(
            text), size, colour, justify
        self.anchor = anchor
        self.pos = self._offset(self.anchor)

    def render(self, image: PIL.ImageDraw.ImageDraw):
        image.text(self.pos, self.text, self.colour, self.font)
    
    def copy(self):
        return self.anchor, self.text, self.size, self.colour, self.justify, self.font
    
    def volatile(self):
        self.pos = self._offset(self.anchor)

    def _offset(self, value: Vector):
        fs = self._fontsize()
        if self.justify == "L":
            return Vector(value[0], value[1] - fs[1] // 2)
        elif self.justify == "R":
            return Vector(value[0] - fs[0], value[1] - fs[1] // 2)
        else:
            self.justify = "C"
            return value - fs // 2

    def _fontsize(self):
        return ImageDraw.textsize(self.text, font=self.font)


class Rectangle(Primative):

    def __init__(self, pos1, pos2, outline=0, fill=None, width=1):
        self.outline, self.fill, self.width = outline, fill, width
        self.pos1, self.pos2 = pos1, pos2

    def copy(self):
        return self.pos1, self.pos2, self.outline, self.fill, self.width

    def render(self):
        ImageDraw.rectangle([*pos1, *pos2], self.fill, self.outline, self.fill)
    

