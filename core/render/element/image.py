from core.vector import Vector
from core.render.primative import Primative
from core.asset.image import Image as AssetImage

__all__ = ["Image"]

class Image(Primative):

    def __init__(self, anchor: Vector, image: AssetImage, just_w: str='C', just_h: str=None):
        super().__init__()
        self.image, self.just_w, self.just_h = image, just_w, just_h
        self.anchor = anchor
        self._calc_pos()

    def render(self, image: "PIL.ImageDraw.ImageDraw"):
        pos = [*self.pos, *self.pos+self.image.size()]
        image.im.paste(self.image.image, tuple(pos))

    def copy(self):
        return self.pos, self.just_w, self.just_h

    def _calc_pos(self):
        size = self.image.size()

        if self.just_w == 'R':
            off_w = self.anchor[0] - size[0]
        elif self.just_w == 'L':
            off_w = self.anchor[0]
        else:
            off_w = self.anchor[0] - (size[0] // 2)

        if self.just_h == 'B':
            off_h = self.anchor[1] + size[1]
        elif self.just_h == 'T':
            off_h = self.anchor[1]
        else:
            off_h = self.anchor[1] + (size[1] // 2)

        self.pos = Vector(off_w, off_h)

