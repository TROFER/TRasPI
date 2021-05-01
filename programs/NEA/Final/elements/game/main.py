# /elements/game/main.py

import core
from PIL import Image as PIL


class MainLoop(core.render.Primative):

    def __init__(self, elements: list):
        self.frame = PIL.new("RGBA", (128, 64))
        self.elements = elements
        self.counter = True
        super().__init__()

    def render(self, draw):
        self.counter = not self.counter
        self.frame = PIL.new("RGBA", (128, 64))
        try:
            for layer in self.elements:
                self.frame = layer.render(self.frame)
        except BaseException as e:
            print(f"Render Error in: {layer} Reason: {e}")
        draw.im.paste(self.frame.convert("1").im, (0, 0, *self.frame.size))

    def copy(self):
        return (self.frame.copy(), self.counter)