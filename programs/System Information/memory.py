import core
from app import App
from core import Vector
from core.render.element import Line, Text
from hardware import Hardware, constrain

class Main(core.render.Window):

    def __init__(self):
        super().__init__()
        self.elements = [
            Text(Vector(3, 5), "Mem - System Info..", justify='L'),
            Line(Vector(0,  10), Vector(128, 10)),
            Text(Vector(3, 16), "", justify="L"),
            Text(Vector(3, 23), "", justify="L"),
            Text(Vector(3, 30), "", justify="L"),
            Line(Vector(0,  35), Vector(128, 35)),
            Text(Vector(3, 42), "Memory Usage", justify="L"),
            Line(Vector(3, 47), Vector(128, 47), width=2)]
        App.interval(self.refresh)

    def render(self):
        for element in self.elements:
            Interface.render(element)

    def refresh(self):
        self.elements[2].text = f"Mem Load: {Hardware.Memory.load()}%"
        self.elements[3].text = f"Swap Size: {Hardware.Memory.vmem()}Mb"
        self.elements[4].text = f"Mem Total {Hardware.Memory.total()}Mb"
        self.elements[7].pos2 = Vector(constrain(Hardware.Memory.load(), 1, 128, 0, 100), 36)


class Handle(core.input.Handler):

    window = Main

    class press:
        async def right(null, window: Main):
            window.finish(1)

        async def left(null, window: Main):
            window.finish(-1)
