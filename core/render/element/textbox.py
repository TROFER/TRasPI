import PIL.ImageDraw
from core.vector import Vector
from core.render.element.text import Text
from core.render.element.rectangle import Rectangle

__all__ = ["TextBox"]

class TextBox(Text):  # ASK TOM

    def __init__(self, anchor, *args, line_col=0, fill=None, width=1, **kwargs):
        self.rect = Rectangle(anchor-Vector(2, 0), Vector(1, 1), line_col, fill, width)
        super().__init__(anchor, *args, **kwargs)

    def render(self, image: "PIL.ImageDraw.ImageDraw"):
        super().render(image)
        self.rect.render(image)

    def copy(self):
        return self.anchor, self.line_col, self.fill, self.width

    def _calc_pos(self):
        super()._calc_pos()
        self.rect.pos = self.pos - Vector(2, 0)
        self.rect.pos_2 = self.font_size() + Vector(2, 0)
