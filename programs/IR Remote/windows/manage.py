import os

from app import App
from core import Vector
from core.render.element import Text
from core.std.menu import Menu, MenuElement
from core.std.query import Query


class Main(Menu):

    def __init__(self):
        elements = []
        for item in os.scandir(App.const.Path):
            if item.is_file() and "json" in item.name:
                elements.append(MenuElement(Text(Vector(0, 0), item.name[:-5], justify='L'), data=(item.name[:-5], item.path), func=self.select))
        super().__init__(*elements, title="Manage Remote...")
    
    async def select(self, remote):
        await Manage(remote)

class Manage(Menu):
    
    def __init__(self, remote):
        elements = [
            MenuElement(Text(Vector(0, 0), "Delete Remote", justify='L'), data=remote, func=self.select)]
        super().__init__(*elements, title=f"Remote: {remote[0]}...")
    
    async def select(self, remote):
        if await Query(f"Delete {remote[0]}?", title="Delete"):
            os.remove(remote[1])
        else:
            self.finish()
