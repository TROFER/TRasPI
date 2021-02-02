import core
from app import App
from core import Interface, Vector
from core.hw import Backlight
from core.render.element import Line, Text
from hardware import Hardware, constrain
from remote import main as Remote


class Graph:

    BUFFER_SIZE = 30

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
            Text(Vector(3, 5), "CPU - Sys Info", justify='L'),
            Line(Vector(0,  10), Vector(128, 10)),
            Text(Vector(3, 16), "", justify="L"),
            Text(Vector(3, 24), "", justify="L"),
            Text(Vector(3, 32), "", justify="L"),
            Line(Vector(0,  37), Vector(128, 37)),
            Text(Vector(3, 43), "CPU Load", justify="L"),
            Line(Vector(3, 48), Vector(128, 48), width=2),
            Text(Vector(3, 57), "CPU Speed", justify="L"),
            Line(Vector(3, 62), Vector(128, 61), width=2)]
        self.graph = Graph()
        App.interval(self.refresh)
    
    async def show(self):
        Backlight.gradient(App.const.colour, hsv=False)

    def render(self):
        for element in self.elements:
            Interface.render(element)

    def refresh(self):
        for elm, text in zip(self.elements[1:4], (f"CPU Load: {Hardware.CPU.load()}%", f"CPU Temp: {Hardware.CPU.temperature()}°C", f"CPU Speed: {Hardware.CPU.cur_speed()}Mhz")):
            elm.text = text
        self.elements[2].text = f"CPU Load: {Hardware.CPU.load()}%"
        self.elements[3].text = "CPU Temp: {}°C {}".format(
            Hardware.CPU.temperature(), '/\\' if self.graph.trend() else '\\/')
        self.elements[4].text = f"CPU Speed: {Hardware.CPU.cur_speed() // 1000}Mhz"
        self.elements[7].pos2 = Vector(
            constrain(Hardware.CPU.load(), 0, 100, 3, 125), 48)
        self.elements[9].pos2 = Vector(
            constrain(Hardware.CPU.cur_speed(), 1, Hardware.CPU.max_speed(), 3, 125), 62)
        self.graph.plot(Hardware.CPU.temperature())


class Handle(core.input.Handler):

    window = Main

    class press:
        async def right(null, window: Main):
            window.finish(1)

        async def left(null, window: Main):
            window.finish(-1)

        async def down(null, window: Main):
            window.finish()
