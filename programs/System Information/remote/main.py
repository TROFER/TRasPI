import json

import core
from app import App
from core import Vector
from core.hw import Backlight
from core.render.element import Text
from core.std.menu import Menu, MenuElement

from remote.client import Client
from remote.windows import cpu, gpu, ram, vram


class Main(Menu):

    def __init__(self):
        items = []

        '''for server in App.const.servers:
            MenuElement(Text(Vector(0, 0), server, justify="L"), data=server, func=self.select)'''

        items.append(MenuElement(Text(Vector(0, 0), App.const.server_address, justify='L'),
                                 data=App.const.server_address, func=self.select))
        super().__init__(*items, title="Remote Servers", end=False)

    async def select(self, data):
        await Carousel(data)
    
    async def show(self):
        await super().show()
        Backlight.gradient(App.const.colour, hsv=False)


class Handle(core.input.Handler, Menu):

    window = Main

    class press:
        async def right(null, window):
            window.finish(1)

        async def left(null, window):
            window.finish(-1)

        async def down(null, window):
            window.finish()


class Carousel(core.render.Window):

    def __init__(self, server_address):
        super().__init__()
        self._flag = True
        self.index = 0
        self.client = Client(server_address)
        self.client.request()
        self.map = [cpu.Main(self.client), ram.Main(
            self.client), gpu.Main(self.client), vram.Main(self.client)]
        App.interval(self.client.request, App.const.refresh_period)

    async def show(self):
        Backlight.gradient(App.const.colour, hsv=False)
        if self._flag:
            self._flag = False
            while True:
                res = await self.map[self.index]
                if res is None:
                    self.client.close()
                    self.finish()
                    break
                else:
                    self.index = (self.index + res) % len(self.map)
            self._flag = True
