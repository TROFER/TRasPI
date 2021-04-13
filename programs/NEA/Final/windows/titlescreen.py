import core
from app import App
import keyboard
from core import Vector
from core.render.element import Image, Rectangle, TextBox
from elements import ImageMotion


class Main(core.render.Window):

    template = core.asset.Template(core.render.Window.template.copy())

    def __init__(self):
        self.elements = [
            TextBox(Vector(64, 25), "Play Game", colour=255, fill=0, line_col=255),
            TextBox(Vector(64, 40), "Scoreboard", colour=255, fill=0, line_col=255),
            TextBox(Vector(64, 55), "Extra", colour=255, fill=0, line_col=255),
            Image(Vector(64, 10), App.asset.ts_cursor),
            Image(Vector(64, 5), App.asset.ts_title)]
        keyboard.add_hotkey("E", self.select)
        keyboard.add_hotkey("W", self.up)
        keyboard.add_hotkey("S", self.down)
        self.imagemotion = ImageMotion(App.asset.ts_template)
        self.index = 0
        App.interval(self.imagemotion.move)
        super().__init__()
        
    def render(self):
        self.template.image = self.imagemotion.copy()
        core.interface.application().render.template()
        for element in self.elements:
            core.interface.render(element)

    def up(self):
        if self.index != 0:
            self.index -= 1
            self.elements[3].pos = Vector(
                self.elements[self.index].pos[0] - 7,
                self.elements[self.index].pos[0] - 2)

    def down(self):
        if self.index != 2:
            self.index += 1
            self.elements[3].pos = Vector(
                self.elements[self.index].pos[0] - 7,
                self.elements[self.index].pos[0] - 2)

    async def select(self):
        pass
