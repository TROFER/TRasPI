from core.render.window import Element, Vector
from core.render.renderer import Render

__all__ = ["Text"]

class Text(Element):

    def __init__(self, pos: Vector, text):
        super().__init__(pos)
        self.text = text

    def render(self):
        self.Render.draw.text()
