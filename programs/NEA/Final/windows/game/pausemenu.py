# /windows/game/pausemenu.py

import core
from app import App
from core import Vector
from core.render.element import Image, TextBox
from elements import ImageMotion
from game import keyboard


class Main(core.render.Window):

    template = core.asset.Template(core.render.Window.template.copy())

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.index = 0
        self._flag = False

        # Elements
        self.imagemotion = ImageMotion(App.asset.ts_template)

        self.title = Image(Vector(64, 3), App.asset.pm_paused)
        self.score = TextBox(Vector(64, 25),
                             f"Score: {self.game.scoring['score']} x{self.game.scoring['depth_multiplier']}",
                             colour=0, fill=255, line_col=0)
        self.resume = TextBox(Vector(64, 40), "Resume Game",
                             colour=0, fill=255, line_col=0)
        self.quit = TextBox(Vector(64, 55), "Exit Game",
                             colour=255, fill=0, line_col=255)

        self.elements = [self.title, self.score, self.resume, self.quit]

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
        core.hw.Backlight.fill((57, 99, 100), force=True)
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
        if self.index != 1:
            self.dehover()
            self.index += 1
            self.hover()

    def hover(self):
        self.elements[self.index + 2].colour = 0
        self.elements[self.index + 2].rect.fill = 255
        self.elements[self.index + 2].rect.outline = 0

    def dehover(self):
        self.elements[self.index + 2].colour = 255
        self.elements[self.index + 2].rect.fill = 0
        self.elements[self.index + 2].rect.outline = 255

    def check_flag(self):
        if self._flag:
            if self.index == 0:
                self.finish()
            else:
                self.finish("quit")