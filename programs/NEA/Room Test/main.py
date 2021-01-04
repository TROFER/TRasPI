import core
from construct import Room
from core.hw.key import Key
from element import RawImage
from core import Vector
from app import App
from PIL import Image


class Viewer(core.render.Window):

    Sensitivity = 150

    def __init__(self):
        Key.repeat(self.Sensitivity)
        self.generate()
        self.layers = {
            "base": 0,
            "background": 0,
            "foreground": 0}
        self.velocities = {
            "base": 1,
            "background": 2,
            "foreground": 3}
        super().__init__()

    def render(self):
        template = Image.new("RGBA", (128, 64), color=0)
        template.alpha_composite(self.background, (self.layers["base"], 0))
        template.alpha_composite(self.background, (self.layers["background"], 0))
        template.alpha_composite(self.foreground, (self.layers["foreground"], 0))
        core.Interface.render(RawImage(Vector(self.layers["base"], 0), template))

    def generate(self):
        self.room = Room()
        self.base = self.room.base
        self.background = self.room.background
        self.foreground = self.room.foreground


class Handle(core.input.Handler):

    window = Viewer

    class press:
        async def down(null, window):
            window.finish()

    class held:
        async def left(null, window):
            for layer in window.layers:
                #if window.layers[layer] != window.room.x:
                window.layers[layer] += window.velocities[layer]

        async def right(null, window):
            for layer in window.layers:
                #if window.layers[layer] != 0:
                window.layers[layer] -= window.velocities[layer]


App.window = Viewer
main = App
