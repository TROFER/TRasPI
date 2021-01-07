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
        if self.layers[0].x - 0 < self.layers[0].image.width:
            for layer in self.layers:
                layer.x -= layer.velocity


    def decrement(self):
        if self.layers[0].x < self.layers[0].image.width:
            for layer in self.layers:
                layer.x += layer.velocity

    def copy(self):
        return [l.x for l in self.layers]


class ParalaxLayer:

    def __init__(self, image: Image, velocity: int):
        self.image = image
        self.velocity = velocity
        self.x = 0