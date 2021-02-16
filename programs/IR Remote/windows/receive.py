import json
import os

import core
from app import App
from arduino import Arduino
from core import Vector
from core.render.element import Image, Text
from core.std.menu import Menu, MenuElement
from core.std.popup import Error


class Main(core.render.Window):

    def __init__(self):
        super().__init__()
        self._flag = True
        self.buttons = []

    async def show(self):
        if self._flag:
            self._flag = False
            while True:
                res = await Configurator(self.buttons)
                if res[1] == -1:
                    break
                elif res[1] == 0:
                    self.save()
                    break
                else:
                    self.buttons = res[0]
            self._flag = True
            self.finish()

    def save(self):
        i = 0
        while True:
            try:
                with open(f"{App.const.Path}untitled_remote({i}).json", 'r') as file:
                    i += 1
            except FileNotFoundError:
                break
        with open(f"{App.const.Path}untitled_remote({i}).json", "w") as file:
            json.dump(self.buttons, file)


class Configurator(Menu):

    def __init__(self, buttons):
        self.buttons = buttons
        self.receving = False
        elements = []
        for button in self.buttons:
            elements.append(MenuElement(
                Text(Vector(0, 0), button["name"], justify='L')))
        elements += [
            MenuElement(Text(Vector(0, 0), "Add Control",
                             justify='L'), func=self.addControl),
            MenuElement(Text(Vector(0, 0), "Save & Exit",
                             justify='L'), func=self.saveAndExit),
            MenuElement(Text(Vector(0, 0), "Exit Without Saving", justify='L'), func=self.exit)]
        super().__init__(*elements, title="Create Remote...", end=False)

    async def addControl(self, data):
        if Arduino != FileNotFoundError:
            res = await ReceiveScreen()
            if isinstance(res, dict):
                self.buttons.append(res)
                self.finish((self.buttons, 1))
            else:
                await Error("Read Timeout")
        else:
            await Error("Serial Err")

    async def saveAndExit(self, data):
        if len(self.buttons) > 0:
            self.finish((self.buttons, 0))
        else:
            self.finish((self.buttons, -1))

    async def exit(self, data):
        self.finish((self.buttons, -1))


class ReceiveScreen(core.render.Window):

    def __init__(self):
        super().__init__()
        self._flag = False
        self.image = Image(Vector(0, 0), App.asset.ReceiveScreen, just_w='L')
        self.future = App.interval(self.awaitRender)

    def render(self):
        core.interface.render(self.image)
        self._flag = True

    def awaitRender(self):
        if self._flag:
            self.future.cancel()
            try:
                self.finish(
                    {"name": "Untitled", "timings": Arduino.receiveIR()})
            except IOError:
                self.finish("timeout")
