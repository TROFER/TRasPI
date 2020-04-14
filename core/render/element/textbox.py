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
    
    def volatile(self):
        self._calc_pos()
        self.rect.pos1, self.rect.pos2 = *self._offset()

    def _offset(self):
        fs = self._font_size()
        return (self.pos[0] - 2, self.pos[1]), Vector(self.pos[0] + fs[0], self.pos[1] + fs[1]))
