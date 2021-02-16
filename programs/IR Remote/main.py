import core
from core import Vector
from core.render.element import Text, Line, TextBox
from windows import send, receive, manage
from core.std.popup import Error
from app import App

class Main(core.render.Window):

    def __init__(self):
        self.index = 0
        self.map = [send.Main, receive.Main, manage.Main]
        self.elements = [
            Text(Vector(3, 10), "IR Controller", justify='L'),
            Line(Vector(0, 14), Vector(128, 14)),
            TextBox(Vector(64, 25), "Open Remote", line_col=0),
            TextBox(Vector(64, 37), "Create Remote", line_col=1),
            TextBox(Vector(64, 49), "Manage Remotes", line_col=1)]

    def render(self):
        for element in self.elements:
            core.interface.render(element)

class Handle(core.input.Handler):

    window = Main

    class press:
        async def down(null, window):
            if window.index != 2:
                window.elements[2 + window.index].rect.outline = 1
                window.index += 1
                window.elements[2 + window.index].rect.outline = 0

        async def up(null, window):
            if window.index != 0:
                window.elements[2 + window.index].rect.outline = 1
                window.index -= 1
                window.elements[2 + window.index].rect.outline = 0
        
        async def centre(null, window):
            await window.map[window.index]()

App.window = Main
main = App
