import json
import os

import core
from app import App
from arduino import Arduino
from core import Vector
from core.hw.key import Key
from core.render.element import Text
from core.std.menu import Menu, MenuElement
from core.std.popup import Error


class Main(Menu):

    def __init__(self):
        elements = []
        for item in os.scandir(App.const.Path):
            if item.is_file() and "json" in item.name:
                with open(item.path, 'r') as remote:
                    elements.append(MenuElement(Text(Vector(0, 0), item.name[:-5], justify='L'), data=(
                        item.name[:-5], json.load(remote)), func=self.select))
        super().__init__(*elements, title="Open Remote...")

    async def select(self, data):
        await RemoteVeiwer(data)

class RemoteVeiwer(Menu):

    def __init__(self, remote):
        elements = []
        for button in remote[1]:
            elements.append(MenuElement(Text(Vector(
                0, 0), button["name"], justify="L"), data=button["timings"], func=self.select))
        super().__init__(*elements, title=remote[0])

    async def select(self, data):
        if Arduino != FileNotFoundError:
            Arduino.sendIR(data)
            Key.flash(speed=0.1)
        else:
            await Error("Serial Err")
