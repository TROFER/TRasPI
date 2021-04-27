import core
from generation.common import align
import time
from PIL import Image as PIL


class Sprite:

    def __init__(self, sprite, pos: tuple, step: float = 0, show: bool = True):
        self.sprite = sprite
        self.x, self.y = pos
        self.step = step
        self.show = show
        self.rotation = "Forward"
        self._timer = None

        # Alignment
        self.y_offset = align(self.sprite, "Y", "B")
        self.x_offset = align(self.sprite, "X", "C")

    def render(self, frame):
        if self._timer is not None:
            if self._timer <= time.time():
                self.show = False
                self._timer = None
        if self.show:
            construct = PIL.new("RGBA", (256, 64))
            construct.alpha_composite(self.sprite, dest=(
                self.x + 128 + self.x_offset, self.y + self.y_offset))
            construct = construct.crop((128, 0, 256, 64))
            frame.alpha_composite(construct)
        return frame

    def set_position(self, position):
        self.x = position

    def increment(self):
        self.x += self.step

    def decrement(self):
        self.x -= self.step

    def flip_backward(self):
        if self.rotation != "Backward":
            self.sprite = self.sprite.transpose(PIL.FLIP_LEFT_RIGHT)
            self.rotation = "Backward"

    def flip_forward(self):
        if self.rotation != "Forward":
            self.sprite = self.sprite.transpose(PIL.FLIP_LEFT_RIGHT)
            self.rotation = "Forward"
    
    def peak(self, secconds):
        self.show = True
        self._timer = time.time() + secconds
