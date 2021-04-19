import core
from app import App
from core import Vector
from core.render.element import Image, TextBox
from elements import ImageMotion

from game import keyboard
from windows.game.main import Game


class Main(core.render.Window):

    template = core.asset.Template(core.render.Window.template.copy())

    def __init__(self):
        super().__init__()
        self.elements = [
            TextBox(Vector(64, 25), "Play Game",
                    colour=0, fill=255, line_col=0),
            TextBox(Vector(64, 40), "Scoreboard",
                    colour=255, fill=0, line_col=255),
            TextBox(Vector(64, 55), "Extra", colour=255, fill=0, line_col=255),
            Image(Vector(64, 3), App.asset.ts_title)]
        self.imagemotion = ImageMotion(App.asset.ts_template)
        self.index = 0
        self.map = [Game]
        self._flag = False
        App.interval(self.imagemotion.move)
        App.interval(self.check_flag, 0.1)

    async def show(self):
        # Bind Hotkeys
        keyboard.Hotkey("w", self.up)
        keyboard.Hotkey("s", self.down)
        keyboard.Hotkey("e", self.select)
        # Set Backlight
        core.hw.Backlight.fill((33, 94, 100), force=True) 

    def render(self):
        self.template.image = self.imagemotion.copy()
        core.interface.application().render.template()
        for element in self.elements:
            core.interface.render(element)

    def up(self):
        if self.index != 0:
            self.dehover()
            self.index -= 1
            self.hover()

    def down(self):
        if self.index != 2:
            self.dehover()
            self.index += 1
            self.hover()

    def hover(self):
        self.elements[self.index].colour = 0
        self.elements[self.index].rect.fill = 255
        self.elements[self.index].rect.outline = 0

    def dehover(self):
        self.elements[self.index].colour = 255
        self.elements[self.index].rect.fill = 0
        self.elements[self.index].rect.outline = 255

    async def check_flag(self):
        if self._flag:
            await self.map[self.index]()
            self._flag = False

    def select(self):
        self._flag = True
    
    
