from core.render.window import Window
from core.interface import Interface
from core.input.event import Handler
from core.render.element import Text
from core.render.element import TextBox
from core.render.element import Rectangle
from core.vector import Vector
from core.sys.attributes import SysConfig
import core
import time
from home import panels

class App(core.type.Application):
    pass

class MainWindow(Window):

    # template = core.asset.Template("std::window", path="window.template")

    def __init__(self):
        super().__init__()
        # Apply colour scheme
        self.index = [0, 0]
        self.elements = [
            Text(Vector(3, 5), f"{SysConfig.system_name}", justify='L'),
            Text(Vector(126, 5), time.strftime("%I:%M%p"), justify='R'),
            Text(Vector(self.elements[3+self.index][0].pos[0] - 2,
                        self.elements[3+self.index][0].pos[1]), ">", justify='R'),
            TextBox(Vector(127, 18), "Run Program", justify='R'),
            TextBox(Vector(127, 30), "System Settings", justify='R'),
            TextBox(Vector(127, 42), "Power Options", justify='R')
        ]
        self.panels = panels.panels

    def render(self):
        for element in self.elements:
            Interface.render(element)
        self.panels[self.index[1]].render()

    def refresh(self):
        self.elements[1].text = time.strftime("%I:%M%p")
        self.elements[2].anchor = Vector(self.elements[3+self.index][0].pos[0] - 2, self.elements[3+self.index][0].pos[1])

class Handle(Handler):

    window = MainWindow

    class press:

        async def up(window):
            if window.index[0] < 2:
                window.index[0] += 1
                window.refresh()
        
        async def down(window):
            if window.index[0] > 0:
                window.index[0] -=1
                window.refresh()
        
        async def centre(window):
            pass
            
        async def left(window):
            if window.index[1] > 0:
                window.index[1] -=1
        
        async def right(window):
            if window.index[1] < 2:
                window.index[1] += 1

App.window = MainWindow()
main = App