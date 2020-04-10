import PIL.ImageDraw
import PIl.ImageFont
import core.Vector
from core.render.primative import Primative


class Text(Primative):

    def __init__(self, anchor, text="Default Text", font="std", size=11, colour=0, justify='C'):  # ASSET SYSTEM
        super().__init__()
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
        return ImageFont.getsize(self.text, font=self.font)


class TextBox(Text): # ASK TOM

    def __init__(self, anchor, *args, line_col=0, fill=None, width=1, **kwargs):
        self.rect = Rectangle(pos-Vector(2, 0), Vector(1, 1), line_col, fill, width)
        super().__init__(anchor, *args, *kwargs)

        def render(self):
            super().render()
            ImageDraw.rectangle(*self.rect)

        def copy(self):
            return self.anchor, self.line_col, self.fill, self.width

        def _offset(self, value: Vector):
            value = super()._offset(value)
            self.rect.pos = value - Vector(2, 0)
            self.rect.pos_2 = self.font_size() + Vector(2, 0)
            return value

class Image(Primative):

    def __init__(self, anchor, just_w='C', just_h=None):
        super().__init__()
        self.image, self.just_w, self.just_h = image, just_w, just_h
        self.anchor = anchor
        self.pos = self._offset()

    def render(self):
        # ASK TOM

    def copy(self):
        return self.pos, self.just_w, self.just_h

    def _offset(self):
        img_w, img_h = self.image_size()
        pos = []
        if self.just_w == 'R':
            pos[0] = self.anchor[0] - img_w
        elif self.just_w == 'L':
            pos[0] = self.anchor[0]
        else:
            pos[0] = self.anchor[0] - (img_w // 2)

        if self.just_h == 'B':
            pos[1] = self.anchor[1] + img_h
        elif self.just_h == 'T':
            pos[1] = self.anchor[1]
        else:
            pos[1] = self.anchor[1] + (img_h // 2)
        return pos

    def image_size(self):
        return  # IMAGE SIZE


class Rectangle(Primative):

    def __init__(self, pos1, pos2, outline=0, fill=None, width=1):
        super().__init__()
        self.outline, self.fill, self.width = outline, fill, width
        self.pos1, self.pos2 = pos1, pos2

    def copy(self):
        return self.pos1, self.pos2, self.outline, self.fill, self.width

    def render(self):
        ImageDraw.rectangle([*self.pos1, *self.pos2],
                            self.fill, self.outline, self.fill)


class Line(Primative):

    def __init__(self, pos1, pos2, colour=0, width=1, joint=None):
        super().__init__()
        self.colour, self.width, self.joint = colour, width, joint
        self.pos1, self.pos2 = pos1, pos2

    def copy(self):
        return self.pos1, self.pos2, self.colour, self.width

    def render(self):
        ImageDraw.line([*self.pos1, *self.pos2],
                       self.colour, self.width, self.joint)
