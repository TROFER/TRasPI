import core
from time import strftime
from core.render.element import Line, Text

class Player(core.render.Window):
    
    def __init__(self):
        super().__init__()
        self.elements = [
            Text(Vector(64, 5), strftime("%I:%M %p")),
            Line(Vector(0, 6), Vector(128, 6))
        ]