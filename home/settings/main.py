import core
from core.vector import Vector
from core.render.element import Text, Line
from core.std import Query, Numpad
from .app import App

class Main(core.render.Window):

    def __init__(self):
        self.index = 0
        self.cursor = Text(Vector(3, 10), "<", justify='R')
        self.elements = [
            Text(Vector(64, 5), "Settings",),
            Line(Vector(0, 6), Vector(128, 6)),
            Line(Vector(0, 20), Vector(128, 20)),
            Line(Vector(0, 30), Vector(128, 30)),
            Text(Vector(3, 10), "Account", justify='L'),
            Text(Vector(3, 20), "Display", justify='L'),
            Text(Vector(3, 30), "Personalisation", justify='L'),
            Line(Vector(0, 35), Vector(128, 35))]
    
    def render(self):
        for element in self.elements:
            core.interface.render(element)
        core.interface.render(self.cursor)
    
    def refresh(self):
        self.cursor.pos = self.elements[3+self.index].pos

class Handle(core.input.Handler):

    window = WindowPower

    class press:
        async def down(null, window: WindowPower):
            if window.index < 2:
                window.index +=1
                window.refresh()

        async def up(null, window: WindowPower):
            if window.index != 0:
                window.index -=1
                window.refresh()

        async def centre(null, window: WindowPower):
            async open()


App.window = Main
main = App