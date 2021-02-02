import core
from app import App
from core import Vector
from core.hw import Backlight
from core.render.element import Line, Text
from hardware import Hardware
from remote import main as Remote


class Main(core.render.Window):

    def __init__(self):
        super().__init__()
        self.elements = [
            Text(Vector(3, 5), "Network - Sys Info", justify='L'),
            Line(Vector(0,  10), Vector(128, 10)),
            Text(Vector(3, 16), "Local / Public IP", justify="L"),
            Text(Vector(3, 24), "Loading...", justify="L"),
            Text(Vector(3, 32), "Loading...", justify="L"),
            Line(Vector(0,  37), Vector(128, 37)),
            Text(Vector(3, 43), "Testing...", justify="L"),
            Text(Vector(3, 51), f"SSH PW: {Hardware.Network.ssh_login()}", justify="L")]
        App.interval(self.refresh, 5)

    async def show(self):
        Backlight.gradient(App.const.colour, hsv=False)

    def render(self):
        for element in self.elements:
            core.Interface.render(element)

    def refresh(self):
        self.elements[3].text = f"Loc: {Hardware.Network.local_addr()}"
        self.elements[4].text = f"Pub: {Hardware.Network.public_addr()}"
        self.elements[6].text = f"INet Access: {Hardware.Network.internet_test()}"


class Handle(core.input.Handler):

    window = Main

    class press:
        async def right(null, window: Main):
            window.finish(1)

        async def left(null, window: Main):
            window.finish(-1)

        async def down(null, window: Main):
            window.finish()
