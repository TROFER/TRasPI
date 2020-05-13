import core
from home.app import App
from core import Vector
from core import Interface
from core.render.element import Line, Text

def constrain(n, start1, stop1, start2, stop2):
    return int(((n - start1) / (stop1 - start1)) * (stop2 - start2) + start2)

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
        self.elements = [
            Text(Vector(3, 5), "CPU - System Information", justify='L'),
            Text(Vector(3, 15), ""),
            Text(Vector(3, 20), ""),
            Text(Vector(3, 25), ""),
            Text(Vector(3, 30), "CPU Load"),
            Line(Vector(0, 36), Vector(128, 36), width=2),
            Text(Vector(3, 40), "CPU Speed"),
            Line(Vector(0, 46), Vector(128, 46), width=2)]
        App.interval(self.refresh)
    
    def render(self):
        for element in self.elements:
            Interface.render(element)
            

    def refresh(self):
        self.elements[1:4].text = f"CPU Load: {CPU.load()}%", f"CPU Temp: {CPU.tempreture()}°C", f"CPU Speed: {CPU.cur_speed()}Mhz"
        self.elements[5].pos2 = Vector(constrain(CPU.load, 1, 128, 0, 100), 36)
        self.elements[7].pos2 = Vector(constrain(CPU.Speed, 1, 128, 0, CPU.max_speed()), 46)

class Handle(core.input.event.Handle):

    window=Main

    class press:
        async def right(null, window):
            window.finish(1)

        async def left(null, window):
            window.finish(-1)
