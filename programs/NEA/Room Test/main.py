import core
from construct import Room
from core.hw.key import Key
from element import Paralax, ParalaxLayer
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

    def generate(self):
        self.room = Room()
        layers = [
            ParalaxLayer(self.room.base, 3),
            ParalaxLayer(self.room.background, 5),
            ParalaxLayer(self.room.foreground, 7)]
        self.paralax = Paralax(layers)


class Handle(core.input.Handler):

    window = Viewer

    class press:
        async def down(null, window):
            window.finish()

    class held:
        async def left(null, window):
            window.paralax.decrement(core.application.app().deltatime())

        async def right(null, window):
            window.paralax.increment(core.application.app().deltatime())


App.window = Viewer
main = App
