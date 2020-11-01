from ...vector import Vector
from .text import Text
from ...interface import Interface

class Marquee(Text):

    def __init__(self, anchor: Vector, text: str="Text", width: int=None, speed: float=1, small=True, flag=True, **kwargs):
        super().__init__(anchor, text, **kwargs)
        self.width = abs(int(width)) if width else len(self.text)
        self.speed = abs(speed) if speed else 1
        self.flag = bool(flag)
        self.small = True
        self.__index = 0
        self.__generate_subtext()
        self.__time_buffer = 0

    def __generate_subtext(self):
        self.__subtext = self.text[self.__index:min(self.__index + self.width, len(self.text))]
        self.__subtext += self.text[:min(self.__index, self.width - len(self.__subtext))]
        self.__subtext += " " * (self.width - len(self.__subtext))

    def render(self, image: "PIL.ImageDraw.ImageDraw"):
        text = self.text
        self.text = self.__subtext
        super().render(image)
        self.text = text

    def copy(self):
        if self.flag and not (self.small and len(self.text.strip()) <= self.width):
            self.__time_buffer += Interface.application().deltatime()
            while self.__time_buffer > self.speed:
                self.__time_buffer -= self.speed
                self.__index = (self.__index + 1) % len(self.text)
        return (self.__index, self.width, *super().copy())

    def volatile(self):
        self.__generate_subtext()

        text = self.text
        self.text = self.__subtext
        super().volatile()
        self.text = text

    def reset(self, *args):
        self.__index = 0
    def pause(self, *args):
        self.flag = False
    def play(self, *args):
        self.flag = True