import core
from construct import Room
import keyboard
from element import Backlight, Paralax, ParalaxLayer
from core import Vector
from app import App
from PIL import Image


class Viewer(core.render.Window):

    def __init__(self):
        self.generate()
        self.input = Keyboard(self)
        super().__init__()

    def render(self):
        core.Interface.render(self.paralax)
        core.Interface.render(self.backlight)

    def generate(self):
        self.room = Room()
        layers = [
            ParalaxLayer(self.room.base, 0.1),
            ParalaxLayer(self.room.background, 0.25),
            ParalaxLayer(self.room.foreground, 1)]
        self.paralax = Paralax(layers)
        colours = [self.room.base.copy().convert("RGB").getpixel((x, 64))
                   for x in range(0, self.room.base.width - 1)]
        self.backlight = Backlight(colours)


class Keyboard:

    def __init__(self, parent):
        self.parent = parent
        keyboard.add_hotkey("a", self.a)
        keyboard.add_hotkey("d", self.d)

    def a(self):
        self.parent.paralax.decrement()
        self.parent.backlight.x = int(self.parent.paralax.layers[0].x)

    def d(self):
        self.parent.paralax.increment()
        self.parent.backlight.x = int(self.parent.paralax.layers[0].x)


class Handle(core.input.Handler):

    window = Viewer

    class press:
        async def down(null, window):
            window.finish()


App.window = Viewer
main = App
