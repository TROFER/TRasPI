import core
from core.asset.image import Image as AssetImage
import time
from PIL import Image


class ImageLoop(core.render.Primative):

    def __init__(self, pos: core.Vector, image: AssetImage):
        super().__init__()
        self.pos = pos
        self.stitch(image)
        self.x, self.y = 0, 0

    def render(self, draw):
        frame = self.image.copy().crop((self.x, self.y, self.x + 128, self.y + 64))
        draw.im.paste(frame.im, (*self.pos, 128, 64))

    def increment(self):
        if self.x != 140 and self.y != 84:
            self.x += 1
            self.y += 1
        else:
            self.x = 0
            self.y = 0

    def stitch(self, image):
        self.image = Image.new("1", (280, 168))
        for x in range(0, 280, 140):
            for y in range(0, 168, 84):
                self.image.paste(image.image, (x, y))

    def copy(self):
        return self.x, self.y
