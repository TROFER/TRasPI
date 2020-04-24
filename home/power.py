from core.interface import Interface
from core.render import Window
from core.input import Handler
from core.hw.power import Power
from core.render import element
from core import asset
from core import Vector

class Main(Window):

    POWER_HALT = asset.Image("power-halt.image")
    POWER_RESTART = asset.Image("power-restart.image")

    def __init__(self):
        self.index = 0
        self.map = {Power.halt, Power.restart, self.finish}
        self.elements = [
            element.Text(Vector(3, 5), "Power Options", justify='L'),
            element.Text(Vector(127, 5), time.strftime("%I:%M%p"), justify='R'),
            element.Image(Vector(32, 25), self.POWER_HALT),
            element.Image(Vector(94, 25), self.POWER_RESTART),
            element.TextBox(Vector(32, 40), "Turn Off", line_col=1),
            element.TextBox(Vector(94, 40), "Restart", line_col=1),
            element.TextBox(Vector(100, 57), "Cancel", line_col=0)]
        App.interval(self.refresh)

    def render(self):
        for element in self.elements:
            Interface.render(element)
    
    def refresh(self):
        self.elements[1].text = time.strftime("%I:%M%p")


class Handle(Handler):

    window = Main

    class press:
        async def left(null, window):
            if window.index > 0:
                window.elements[window.index + 3].line_col = 1
                window.index -= 1
                window.elements[window.index + 3].line_col = 0

        async def right(null, window):
            if window.pos < 2:
                window.elements[window.index + 3].line_col = 1
                window.pos += 1
                window.elements[window.index + 3].line_col = 0

        async def centre(null, window):
            window.map[window.index]()

main = Main()
