import core
from core.std.menu import Menu, MenuElement
from core.render.element import Text
from core import Vector
from app import App


class Options(Menu):

    def __init__(self, parent):
        self.parent = parent
        elements = [
            MenuElement(Text(Vector(0, 0), "Change Location",
                             justify='L'), func=self.setLocation),
            MenuElement(Text(Vector(0, 0), "Refresh", justify='L'), func=self.refresh)]
        super().__init__(*elements, title="App Settings")

    async def setLocation(self, *kwargs):
        await Location(self.parent)
        self.finish()

    def refresh(self, *kwargs):
        self.parent.request()
        self.finish()


class Location(Menu):

    def __init__(self, parent):
        self.parent = parent
        elements = []
        for loc in App.var.alternative_locations:
            MenuElement(Text(Vector(0, 0), loc, justify='L'),
                        func=self.set, data=loc)
        super().__init__(*elements, title="Locations")

    def set(self, location):
        self.parent.LOCATION = location
        self.parent.request()
        self.finish()
