import core
import time
from core import Vector

class Marquee(core.element.Text):

    def __init__(self, pos: Vector, text: str, width):
        self.pos, self.width = pos, width
        self.index = 0
        self.flag = True
        self._array = [' ' for i in range(self.width)]
        self._text = f"{_text}{' '*width}"
        super().__init__(self.pos, "".join(self._array))
    
    def text(self, text):
        self._array = [' ' for i in range(self.width)]
        self.index = 0
        self._text = f"{_text}{' '*width}"
        super().text = "".join(self._array)

    def update(self):
        if self.flag:
            self._array.pop(0)
            self._array.append(self._text[self.index])
            if self.index == len(self._text) - 1:
                self.index = 0
            else:
                self.index += 1
            super().text = "".join(self._array)
    