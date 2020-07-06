import core
from app import App
from core import Vector, Interface
from core.render.element import Line, Text
from hardware import Hardware, constrain

class Graph:

    BUFFER_SIZE = 10

    def __init__(self):
        self.buffer = [0 for i in range(self.BUFFER_SIZE)]

    def plot(self, data):
        self.buffer.append(data)
        del self.buffer[-1]

    def trend(self):
        if self.buffer[0] > self.buffer[-1]:
            return True
        elif self.buffer[0] < self.buffer[-1]:
            return False
        else:
            None


class Main(core.render.Window, Graph):

    def __init__(self):
        super().__init__()
        self.elements = [
            Text(Vector(3, 5), "CPU - System Information", justify='L'),
            Text(Vector(3, 15), "", justify="L"),
            Text(Vector(3, 22), "", justify="L"),
            Text(Vector(3, 29), "", justify="L"),
            Text(Vector(3, 40), "CPU Load", justify="L"),
            Line(Vector(0, 53), Vector(128, 53), width=2),
            Text(Vector(3, 55), "CPU Speed", justify="L"),
            Line(Vector(0, 62), Vector(128, 62), width=2)]
        App.interval(self.refresh)

    def render(self):
        for element in self.elements:
            Interface.render(element)

    def refresh(self):
        for elm, text in zip(self.elements[1:4], (f"CPU Load: {Hardware.CPU.load()}%", f"CPU Temp: {Hardware.CPU.temperature()}°C", f"CPU Speed: {Hardware.CPU.cur_speed()}Mhz")):
            elm.text = text
        self.elements[5].pos2 = Vector(constrain(Hardware.CPU.load(), 1, 128, 0, 100), 36)
        self.elements[7].pos2 = Vector(
            constrain(Hardware.CPU.cur_speed(), 1, 128, 0, Hardware.CPU.max_speed()), 46)


class Handle(core.input.Handler):

    window = Main

    class press:
        async def right(null, window: Main):
            window.finish(1)

        async def left(null, window: Main):
            window.finish(-1)

        async def centre(null, window: Main):
            window.finish()