import core
from home.app import App
from util import Hardware, constrain
from core import Vector
from core import Interface
from core.render.element import Line, Text


class Graph:

    BUFFER_SIZE = 10

    def __init__(self):
        self.buffer = [0]

    def plot(self, data):
        if self.buffer[0] != 0:
            self.buffer.append(data)
        else:
            self.buffer[0] = data
        if len(self.buffer) > self.BUFFER_SIZE:
            del self.buffer[0]

    def trend(self):
        if self.buffer[0] < self.buffer[-1]:
            return True
        elif self.buffer[0] > self.buffer[-1]:
            return False
        else:
            None


class Main(core.render.Window, Graph):

    def __init__(self):
        super().__init__()
        self.elements = [
            Text(Vector(3, 5), "CPU - Sys Information", justify='L'),
            Line(Vector(0, 9), Vector(128, 9)),
            Text(Vector(3, 15), "", justify='L'),
            Text(Vector(3, 25), "", justify='L'),
            Text(Vector(3, 34), "", justify='L'),
            Line(Vector(0, 39), Vector(128, 39)),
            Text(Vector(3, 45), "CPU Load"),
            Line(Vector(0, 50), Vector(128, 50), width=2),
            Text(Vector(3, 57), "CPU Speed"),
            Line(Vector(0, 62), Vector(128, 62), width=2)]
        self.graph = Graph()
        App.interval(self.refresh)

    def render(self):
        for element in self.elements:
            Interface.render(element)

    def refresh(self):
        self.elements[2].text = f"CPU Load: {Hardware.CPU.load()}%"
        self.elements[3].text = "CPU Temp: {}°C {}".format(Hardware.CPU.temperature(), '/\\' if self.graph.trend() else '\\/')
        self.elements[4].text = f"CPU Speed: {Hardware.CPU.cur_speed() // 1000}Mhz"
        self.elements[7].pos2 = Vector(
            constrain(Hardware.CPU.load(), 0, 100, 0, 128), 50)
        self.elements[9].pos2 = Vector(
            constrain(Hardware.CPU.cur_speed(), 1, Hardware.CPU.max_speed(), 0, 128), 62)
        self.graph.plot(Hardware.CPU.temperature())

class Handle(core.input.Handler):

    window = Main

    class press:
        async def right(null, window):
            window.finish(1)

        async def left(null, window):
            window.finish(-1)
