import core
import time
from core import Vector
from app import App

class Marquee(core.element.Text):

    def __init__(self, pos: Vector, text: str, width, speed: int=1):
        self.pos, self.width = pos, width
        self.speed = speed
        self.index = 0
        self.flag = True
        self._array = [' ' for i in range(self.width)]
        self.text = f"{text}{' '*width}"
        super().__init__(self.pos, "".join(self._array))
        App.interval(self.update, self.speed)

    def update(self):
        if self.flag:
            self._array.pop(0)
            self._array.append(self.text[self.index])
            if self.index == len(self.text) - 1:
                self.index = 0
            else:
                self.index += 1
            super().text = "".join(self._array)
    