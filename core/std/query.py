from ..render.window import Window
from ..interface import Interface
from ..input.event import Handler
from ..render.element import Text
from ..render.element import TextBox
from ..vector import Vector

__all__ = ["Query"]

class Query(Window):

    #template = core.asset.Template("std::query", path="query.template")

    def __init__(self, message, title="Query", cancel=False):
        super().__init__()
        self.elements = [
            Text(Vector(5, 5), title, justify='L'),
            Text(Vector(64, 32), message, justify='C'),
            TextBox(Vector(32 if cancel else 31, 54), "Yes"),
            TextBox(Vector(61 if cancel else 93, 54), "No")]
        if cancel:
            self.elements.append(TextBox(Vector(96, 54), "Cancel"))

        self.__cancel = cancel

    def render(self):
        for element in self.elements:
            Interface.render(element)

class Handle(Handler):

    window = Query

    class press:
        async def left(null, window: Query):
            window.finish(True)
        async def right(null, window: Query):
            window.finish(False)
        async def centre(null, window: Query):
            if window.__cancel:
                window.finish(None)
