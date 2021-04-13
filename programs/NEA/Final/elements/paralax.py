import core
from core import Vector
from PIL import Image


class Paralax(core.render.Primative):

    def __init__(self, layers: list):
        super().__init__()
        self.layers = layers

    def render(self, draw):
        frame = Image.new("RGBA", (128, 64), color=(255, 255, 255))
        for layer in self.layers:
            image = layer.image.copy()
            flag = False
            if layer.x < 0:
                image = image.crop((0 - int(layer.x), 0, *layer.image.size))
                flag = True
            frame.alpha_composite(
                image, dest=(0 if flag else int(layer.x), 0))
        draw.im.paste(frame.convert("1").im, (0, 0, *frame.size))

    def increment(self):
        """Shifts scene right"""
        if self.layers[-1].x + self.layers[-1].speed > 128 - self.layers[-1].image.width:
            for layer in self.layers:
                layer.x -= layer.speed

    def decrement(self):
        """Shifts scene left"""
        if self.layers[-1].x - self.layers[-1].speed < 0:
            for layer in self.layers:
                layer.x += layer.speed

    def copy(self):
        return [l.x for l in self.layers]
    
    def position(self):
        """Returns top layer offset"""
        return self.layers[-1].x

class ParalaxLayer:

    def __init__(self, image: Image, speed: int = 1):
        self.image = image
        self.speed = speed
        self.x = 0
