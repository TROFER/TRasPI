from core.render.window import Window
from core.interface import Interface
from core.input.event import Handler
from core.render.element import Text
from core.vector import Vector

class Query(Window):

    #template = core.asset.Template("std::query", path="query.template")

    def __init__(self, message, title="Query", cancel=False):
        self.elements = [
            Text(Vector(5,5), title, justify='L'),
            Text(Vector(38, 27), message[:14], justify='L'),
            
        ]
