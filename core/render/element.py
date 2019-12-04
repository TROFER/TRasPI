from core.render.window import Element, Vector
from core.render.renderer import Render

__all__ = ["Text"]

class Text(Element):

    def __init__(self, pos: Vector, text):
        super().__init__(pos)
        self.text = text

    def render(self):
        self.Render.draw.text()

class Rectangle(Element):

    def __init__(self, pos: Vector, width: int, height: int):
        super().__init__(pos)
        self.width, self.height = width, height

    def render(self):
        self.Render.draw.rect()