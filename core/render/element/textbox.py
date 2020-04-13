import PIL.ImageDraw
from core.vector import Vector
from core.render.element.text import Text
from core.render.element.rectangle import Rectangle

__all__ = ["TextBox"]

class TextBox(Text):

    def __init__(self, anchor, *args, line_col=0, fill=None, width=1, **kwargs):
        super().__init__(anchor, *args, **kwargs)
        self.rect = Rectangle(*self._offset(), line_col, fill, width)

    def render(self, image: "PIL.ImageDraw.ImageDraw"):
        super().render(image)
        self.rect.render(image)

    def copy(self):
        return (*super().copy(), *self.rect.copy())

    def _offset(self):
        fs = super()._font_size()
        return (self.pos.__add__(Vector(-2, 0)), Vector(self.pos[0] + fs[0], self.pos[1] + fs[1]))
