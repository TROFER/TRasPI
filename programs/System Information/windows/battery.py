import core
from app import App
from core import Vector, hw
from core.render.element import Line, Text
from hardware import Hardware, constrain
from remote import main as Remote


class Main(core.render.Window):

    def __init__(self):
        super().__init__()
        self.elements = [
            Text(Vector(3, 5), "Battery - Sys Info", justify='L'),
            Line(Vector(0,  10), Vector(128, 10)),
            Text(Vector(3, 16), "", justify="L"),  # State
            Text(Vector(3, 24), "", justify="L"),  # Charge Level
            Text(Vector(3, 32), "", justify="L"),  # Tempreture
            Text(Vector(3, 41), "", justify="L"),  # Voltage
            Line(Vector(0, 46), Vector(128, 46)),
            Text(Vector(3, 52), "Charge Level", justify="L"),
            Line(Vector(3, 58), Vector(128, 58), width=2)]
        App.interval(self.refresh)
    
    async def show(self):
        hw.Backlight.gradient(App.const.colour, hsv=False)

    def render(self):
        for element in self.elements:
            core.Interface.render(element)

    def refresh(self):
        self.elements[2].text = f"Status: {'Charging' if hw.Battery.status() else 'Decharging'}"
        self.elements[3].text = f"Charge Level: {hw.Battery.percentage()}%"
        self.elements[4].text = f"Temperature: {hw.Battery.temperature()}°C"
        self.elements[5].text = f"Voltage: {round(hw.Battery.voltage() / 1000, 3)}v"
        self.elements[8].pos2 = Vector(
            constrain(hw.Battery.percentage(), 0, 100, 3, 125), 58)


class Handle(core.input.Handler):

    window = Main

    class press:
        async def right(null, window: Main):
            window.finish(1)

        async def left(null, window: Main):
            window.finish(-1)

        async def down(null, window: Main):
            window.finish()
