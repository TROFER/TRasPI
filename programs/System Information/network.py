import core
from app import App
from core import Vector
from core.render.element import Line, Text
from hardware import Hardware

class Main(core.render.Window):

    def __init__(self):
        super().__init__()
        self.elements = [
            Text(Vector(3, 5), "Network - System In..", justify='L'),
            Line(Vector(0,  10), Vector(128, 10)),
            Text(Vector(3, 16), "Loading...", justify="L"),
            Text(Vector(3, 24), "Loading...", justify="L"),
            Text(Vector(3, 32), "Testing...", justify="L"),
            Text(Vector(3, 40), f"SSH PW: {Hardware.Network.ssh_login()}", justify="L")]
        App.interval(self.refresh, 5)

    def render(self):
        for element in self.elements:
            core.Interface.render(element)

    def refresh(self):
        self.elements[2].text = f"IP 0: {Hardware.Network.local_addr()}"
        self.elements[3].text = f"IP 1: {Hardware.Network.public_addr()}"
        self.elements[4].text = f"Net Test: {Hardware.Network.internet_test()}"

class Handle(core.input.Handler):

    window = Main

    class press:
        async def right(null, window: Main):
            window.finish(1)

        async def left(null, window: Main):
            window.finish(-1)
