import core
from construct import Room
import keyboard
import random
from element import Backlight, Paralax, ParalaxLayer
from core import Vector
from app import App
from PIL import Image


class Viewer(core.render.Window):

    toggle = {"L": False, "R": False}

    def __init__(self):
        self.level = [Room() for i in range(3)]
        self.generate()
        self.input = Keyboard(self)
        App.interval(self.refresh, 0.5)
        super().__init__()

    def render(self):
        core.Interface.render(self.paralax)
        core.Interface.render(self.backlight)
    
    def refresh(self):
        if self.toggle["L"]:
            self.paralax.decrement()
            self.backlight.x = int(self.paralax.layers[0].x)
        if self.toggle["R"]:
            self.paralax.increment()
            self.backlight.x = int(self.paralax.layers[0].x)
    
    def generate(self):
        self.room = random.choice(self.level)
        self.level.remove(self.room)
        layers = [
            ParalaxLayer(self.room.base, 0.75),
            ParalaxLayer(self.room.background, 2),
            ParalaxLayer(self.room.fixings, 3),
            ParalaxLayer(self.room.foreground, 5)]
        self.paralax = Paralax(layers)
        colours = [self.room.base.copy().convert("RGB").getpixel((x, 64))
                   for x in range(0, self.room.base.width - 1)]
        self.backlight = Backlight(colours)


class Keyboard:

    def __init__(self, parent):
        self.parent = parent
        keyboard.add_hotkey("a", self.enable, args=("L"))
        keyboard.on_release_key("a", self.disable_left)
        keyboard.add_hotkey("d", self.enable, args=("R"))
        keyboard.on_release_key("d", self.disable_right)
    
    def enable(self, direction: str):
        self.parent.toggle[direction] = True
    
    def disable_left(self, *args):
        self.parent.toggle["L"] = False
    
    def disable_right(self, *args):
        self.parent.toggle["R"] = False

class Handle(core.input.Handler):

    window = Viewer

    class press:
        async def down(null, window):
            window.finish()


App.window = Viewer
main = App
