from core.interface import Interface
from core.hw.power import Power
from core.render.element import Text
from core.render.element import TextBox

class Main(Window):

    def __init__(self):
        self.index = 0
        self.map {
            Power.halt,
            Power.restart,
            self.finish}
        self.elements [
            Text(Vector(3, 5), "Power Options", justify='L'),
            Text(Vector(127, 5), time.strftime("%I:%M%p"), justify='R'),
        ]
