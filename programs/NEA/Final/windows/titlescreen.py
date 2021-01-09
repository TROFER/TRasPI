import core
from app import App
from control import Keyboard
from core import Vector
from core.render.element import Image, Text, TextBox
from elements import ImageLoop


class Main(core.render.Window):

    def __init__(self):
        super().__init__()
        self.background = ImageLoop(Vector(0, 0), App.asset.ts_background)
        self.title = Image(Vector(64, 5), App.asset.ts_title)
        self.button0 = TextBox(Vector(64, 25), "Play Game", colour=0, line_col=1, fill=0)
        self.button1 = TextBox(Vector(64, 40), "Scoreboard", colour=0, line_col=1, fill=0)
        self.button2 = TextBox(Vector(64, 55), "Extra", colour=0, line_col=1, fill=0)
        self.cursor = Image(Vector(64, 10), App.asset.ts_cursor)
        self.elements = [self.title,self.button0, self.button1, self.button2]
        self.keyboard = Keyboard(self, ["w", "s", "enter"], [self.up, self.down, self.select])
        self.index = 0
        App.interval(self.background.increment)

    def render(self):
        core.interface.render(self.background)
        for element in self.elements:
            core.interface.render(element)

    def up(self):
        Map = [self.button0, self.button1, self.button2]
        if self.index != 0: 
            self.index -= 1
            self.cursor.pos = Vector(
                Map[self.index].pos[0] - 7, Map[self.index].pos[0] - 2)

    def down(self):
        Map = [self.button0, self.button1, self.button2]
        if self.index != 2:
            self.index += 1
            self.cursor.pos = Vector(
                Map[self.index].pos[0] - 7, Map[self.index].pos[0] - 2)

    async def select(self):
        pass

class Handle(core.input.Handler):

    window = Main

    class press:
        async def up(null, window):
            window.up()
    
        async def down(null, window):
            window.down()

        async def centre(null, window):
            window.select()
            