import time

import core
from app import App
from core import Vector
from core.render.element import Image, Rectangle, Text
from elements import ImageMotion

from game import keyboard, library


class Results(core.render.Window):

    template = core.asset.Template(core.render.Window.template.copy())

    def __init__(self, game):
        super().__init__()
        self.game = game
        self.input_buffer = []
        self._flag = False

        # Calculate Final Score
        if game.scoring["surface_exit"]:
            game.scoring["score"] *= game.scoring["depth_multiplier"]
            game.scoring["score"] = int(game.scoring["score"])
            message = "You escaped!"
        else:
            message = "Ending: Lost"

        # Elements
        self.imagemotion = ImageMotion(App.asset.ts_template)
        self.title = Image(Vector(64, 3), App.asset.rs_gameover)
        self.message = Text(Vector(64, 25), message)
        self.score = Text(
            Vector(64, 38), f"Score: {self.game.scoring['score']}")

        self.elements = [Rectangle(Vector(15, 15), Vector(113, 64), fill=255, zindex=-1),
                         self.title, self.message, self.score]

        App.interval(self.imagemotion.move)
        App.interval(self.check_flag, 0.1)

    async def show(self):
        # Reset
        keyboard.clear_all()
        self._flag = False

        # Bind Hotkeys
        keyboard.all_alpha(self.keypress)
        keyboard.Hotkey("enter", self.enter)

        # Set Backlight
        core.hw.Backlight.fill((57, 99, 100), force=True)
        core.hw.Key.all(False)

    def render(self):
        self.template.image = self.imagemotion.copy()
        core.interface.application().render.template()
        for element in self.elements:
            core.interface.render(element)
        name = Text(Vector(64, 55), f"Name: {''.join(self.input_buffer)}")
        core.interface.render(name)

    def keypress(self, key):
        if key == "del":
            if len(self.input_buffer) != 0:
                self.input_buffer.pop(-1)
        elif len(self.input_buffer) < 9:
            self.input_buffer.append(key)

    def enter(self):
        if self.input_buffer:
            self._flag = True

    def check_flag(self):
        if self._flag:
            self._flag = False
            library.lib.databases["scores"].c.execute("INSERT INTO score (date, player, score) VALUES (?, ?, ?)",
            [time.time(), "".join(self.input_buffer), self.game.scoring["score"]])
            library.lib.databases["scores"].db.commit()
            self.finish()
