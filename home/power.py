from core.interface import Interface
from core.hw.power import Power
from core.render import element
from core import asset

class Main(Window):

    POWER_HALT = asset.Image("power-halt.image")
    POWER_RESTART = asset.Image("power-restart.image")

    def __init__(self):
        self.index = 0
        self.map {
            Power.halt,
            Power.restart,
            self.finish}
        self.elements [
            element.Text(Vector(3, 5), "Power Options", justify='L'),
            element.Text(Vector(127, 5), time.strftime("%I:%M%p"), justify='R'),
            element.Image()

        ]
