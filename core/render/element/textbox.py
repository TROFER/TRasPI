import PIL.ImageDraw
from ...vector import Vector
from .text import Text
from .rectangle import Rectangle

__all__ = ["TextBox"]


class TextBox(Text):

    def __init__(self, anchor, *args, line_col=0, fill=None, width=1, **kwargs):
        self.rect = Rectangle(Vector(0, 0), Vector(0, 0),
                              line_col, fill, width)
        super().__init__(anchor, *args, **kwargs)

    def render(self, image: "PIL.ImageDraw.ImageDraw"):
        self.rect.render(image)
        super().render(image)

    def copy(self):
        return (*super().copy(), *self.rect.copy())

    def _calc_pos(self):
        super()._calc_pos()
        fs = self._font_size()
        self.rect.pos1 = self.pos - Vector(2, 0)
        self.rect.pos2 = self.pos + fs
