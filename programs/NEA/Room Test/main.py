import core
from construct import Room
from core.hw.key import Key
from element import Backlight, Paralax, ParalaxLayer
from core import Vector
from app import App
from PIL import Image


class Viewer(core.render.Window):

    Repeat_rate = 75

    def __init__(self):
        Key.repeat(self.Repeat_rate)
        self.generate()
        super().__init__()

    def render(self):
        core.Interface.render(self.paralax)
        core.Interface.render(self.backlight)

    def generate(self):
        self.room = Room()
        layers = [
            ParalaxLayer(self.room.base, 3),
            ParalaxLayer(self.room.background, 5),
            ParalaxLayer(self.room.foreground, 7)]
        self.paralax = Paralax(layers)
        colours = [self.room.base.copy().convert("RGB").getpixel((x, 64))
                   for x in range(0, self.room.base.width - 1)]
        self.backlight = Backlight(colours)


class Handle(core.input.Handler):

    window = Viewer

    class press:
        async def down(null, window):
            window.finish()

    class held:
        async def left(null, window):
            window.paralax.decrement(core.application.app().deltatime())
            window.backlight.x = window.paralax.x

        async def right(null, window):
            window.paralax.increment(core.application.app().deltatime())
            window.backlight.x = window.paralax.x


App.window = Viewer
main = App
