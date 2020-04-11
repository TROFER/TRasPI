from core.vector import Vector
from core.render.primative import Primative

__all__ = ["Line"]

class Line(Primative):

    def __init__(self, pos1: Vector, pos2: Vector, colour: int=0, width: int=1, joint=None):
        super().__init__()
        self.colour, self.width, self.joint = colour, width, joint
        self.pos1, self.pos2 = pos1, pos2

    def copy(self):
        return self.pos1, self.pos2, self.colour, self.width

    def render(self, image: "PIL.ImageDraw.ImageDraw"):
        image.line([*self.pos1, *self.pos2], self.colour, self.width, self.joint)
