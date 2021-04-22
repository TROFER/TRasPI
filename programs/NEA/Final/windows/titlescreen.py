import core
from app import App
from core import Vector
from core.render.element import Image, TextBox
from elements import ImageMotion

from game import keyboard
from windows.game import game
from windows import character, scoreboard


class Main(core.render.Window):

    template = core.asset.Template(core.render.Window.template.copy())

    def __init__(self):
        super().__init__()

        # Elements 
        self.imagemotion = ImageMotion(App.asset.ts_template)
        self.elements = [
            TextBox(Vector(64, 25), "Play Game",
                    colour=0, fill=255, line_col=0),
            TextBox(Vector(64, 40), "Change Skin",
                    colour=255, fill=0, line_col=255),
            TextBox(Vector(64, 55), "Scoreboard", colour=255, fill=0, line_col=255),
            Image(Vector(64, 3), App.asset.ts_title)]

        self.index = 0
        self.map = [game.Game, character.Main, scoreboard.Main]
        self._flag = False

        App.interval(self.imagemotion.move)
        App.interval(self.check_flag, 0.1)

    async def show(self):
        # Reset
        self._flag = False
        keyboard.clear_all()

        # Bind Hotkeys
        keyboard.Hotkey("w", self.up)
        keyboard.Hotkey("s", self.down)
        keyboard.Hotkey("e", self.select)

        # Set Backlight
        core.hw.Backlight.fill((33, 94, 100), force=True)
        core.hw.Key.all(False)

    def render(self):
        self.template.image = self.imagemotion.copy()
        core.interface.application().render.template()
        for element in self.elements:
            core.interface.render(element)

    def select(self):
        self._flag = True

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
    
    
