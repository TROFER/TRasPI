# /main.py

import core
from core.hw import Backlight
from core.render.element import Image

from app import App
from windows import titlescreen


class Main(core.render.Window):

    def __init__(self):
        super().__init__()
        App.interval(self.check_render, 2)
        self.flag = False
        self.titles = [
            Image(core.Vector(0, 0), App.asset.ts_keyboard, just_w="L")]
        self.index = 0

    def render(self):
        core.interface.render(self.titles[self.index])
        if self.index == len(self.titles) - 1:
            self.flag = True
    
    async def show(self):
        Backlight.fill((57, 99, 100), force=True)

    async def check_render(self):
        if self.flag:
            await titlescreen.Main()
            self.finish()
        else:
            self.index += 1


App.window = Main
main = App