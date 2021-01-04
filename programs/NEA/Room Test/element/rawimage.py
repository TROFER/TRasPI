import core
from core import Vector
from PIL import Image
from core.render import Primative

class RawImage(Primative):

    def __init__(self, pos: Vector, image: Image):
        super().__init__()
        self.image = image.convert("1")
        self.pos = pos
    
    def render(self, image: "PIL.ImageDraw.ImageDraw"):
        image.bitmap(tuple(self.pos), self.image)


    def copy(self):
        return self.image, self.pos