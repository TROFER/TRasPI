import core
from app import App
from core import Vector
from core.render.element import Line, Text
from core.hw.battery import Battery
from hardware import Hardware, constrain

class Main(core.render.Window):

    def __init__(self):
        super().__init__()
        self.elements = [
            Text(Vector(3, 5), "Battery - Sys Info", justify='L'),
            Line(Vector(0,  10), Vector(128, 10)),
            Text(Vector(3, 16), "", justify="L"), #State
            Text(Vector(3, 24), "", justify="L"), #Charge Level
            Text(Vector(3, 32), "", justify="L"), #Tempreture
            Text(Vector(3, 41), "", justify="L"), #Voltage 
            Line(Vector(0, 46), Vector(128, 46)),
            Text(Vector(3, 52), "Charge Level", justify="L"),
            Line(Vector(3, 58), Vector(128, 58), width=2)]
        App.interval(self.refresh)

    def render(self):
        for element in self.elements:
            core.Interface.render(element)

    def refresh(self):
        self.elements[2].text = f"Status: {'Charging' if Battery.status() else 'Decharging'}"
        self.elements[3].text = f"Charge Level: {Battery.percentage()}%"
        self.elements[4].text = f"Temperature: {Battery.temperature()}°C"
        self.elements[5].text = f"Voltage: {round(Battery.voltage() / 1000, 3)}v"
        self.elements[8].pos2 = Vector(constrain(Battery.percentage(), 0, 100, 3, 125), 58)


class Handle(core.input.Handler):

    window = Main

    class press:
        async def right(null, window: Main):
            window.finish(1)

        async def left(null, window: Main):
            window.finish(-1)

        async def centre(null, window: Main):
            window.finish()