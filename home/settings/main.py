import core
from core.vector import Vector
from core.std import menu, 
from core.std import Query, Numpad
from .app import App

class Settings(menu.Menu):

    def __init__(self, settings):
        self.items = []
        for _setting in settings:
            elements = [Text(Vector(0, 0), _setting["name"], justify='L')]
            if isinstance(_setting, list):
                elements.append(Text(Vector(128, 0), ">", justify="R")))
                self.items.append(menu.MenuElement(*elements, data=_setting["settings"], func=self.NewMenu))
            else:
                self.items.append(menu.MenuElement(*elements, data="Value, min max ect ect", func=self.EditValue)) # Add func=numpad or true false ect. 
        super().__init__(*self.items, title="Settings")
    
    async def NewMenu(self, item):
        await Settings(item)

    async def EditValue(self, item):
        if settting.type == bool:
            res = await Query()

App.window = Main
main = App