import core
from home.app import App
from core import Vector
from core.render.element import Line, Text


class Main(core.render.Window):

    def __init__(self):
        super().__init__()
        self.elements = [
            Text(Vector(3, 5), "Memory - System Information", justify='L'),
            Text(Vector(3, 15), ""),
            Text(Vector(3, 20), ""),
            Text(Vector(3, 25), ""),
            Text(Vector(3, 30), "Mem Load"),
            Line(Vector(0, 36), Vector(128, 36), width=2)]
        App.interval(self.refresh)

    def render(self):
        for element in self.elements:
            Interface.render(element)

    def refresh(self):
        self.elements[1:4].text = f"Mem Load: {Mem.load()}%", f"VMem: {Mem.vmem()}Mb", f"Total Mem{Mem.total()}Mb"
        self.elements[5].pos2 = Vector(constrain(Hardware.Memory.load, 1, 128, 0, 100), 36)


class Handle(core.input.Handler):

    window = Main

    class press:
        async def right(null, window):
            window.finish(1)

        async def left(null, window):
            window.finish(-1)
