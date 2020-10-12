from ...vector import Vector
from ..primative import Primative
from .text import Text

class Marquee(Text):

    def __init__(self, pos: Vector, text: str, width: int):
        self.width = width
        self.speed = speed
        self.index = 0
        self.flag = True
        self._array = [' ' for i in range(self.width)]
        self.text = f"{text}{' ' * self.width}"
        super().__init__(self.pos, "".join(self._array))

    def update(self):
        if self.flag(self):
            self._array.pop(0)
            self._array.append(self.text[self.index])
            if self.index == len(self.text) - 1:
                self.index = 0
            else:
                self.index += 1
            super().text = "".join(self._array)