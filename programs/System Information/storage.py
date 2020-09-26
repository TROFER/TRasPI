import core
from app import App
from core import Vector
from core.render.element import Line, Text
from hardware import Hardware, constrain

class Main(core.render.Window):

    def __init__(self):
        super().__init__()
        self.elements = [
            Text(Vector(3, 5), "Storage - Sys Info", justify='L'),
            Line(Vector(0,  10), Vector(128, 10)),
            Text(Vector(3, 16), "", justify="L"),
            Text(Vector(3, 24), "", justify="L"),
            Text(Vector(3, 32), "", justify="L"),
            Line(Vector(0,  37), Vector(128, 37)),
            Text(Vector(3, 43), "Disk Usage", justify="L"),
            Line(Vector(3, 49), Vector(128, 49), width=2)]
        App.interval(self.refresh)

    def render(self):
        for element in self.elements:
            core.Interface.render(element)

    def refresh(self):
        self.elements[2].text = f"Used: {Hardware.Storage.used()}GB ({Hardware.Storage.used_percent()}%)"
        self.elements[3].text = f"Free: {Hardware.Storage.free()}GB"
        self.elements[4].text = f"Total: {Hardware.Storage.total()}GB"
        self.elements[7].pos2 = Vector(constrain(Hardware.Storage.used_percent(), 0, 100, 3, 125), 49)


class Handle(core.input.Handler):

    window = Main

    class press:
        async def right(null, window: Main):
            window.finish(1)

        async def left(null, window: Main):
            window.finish(-1)
