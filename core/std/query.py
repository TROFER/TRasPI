from core.render.window import Window
from core.interface import Interface
from core.input.event import Handler
from core.render.element import Text
from core.render.element import TextBox
from core.vector import Vector


class Query(Window):

    #template = core.asset.Template("std::query", path="query.template")

    def __init__(self, message, title="Query", cancel=False):
        self.elements = [
            Text(Vector(5, 5), title, justify='L'),
            Text(Vector(38, 27), message[:14], justify='L'),
            TextBox(Vector(32 if cancel else 31, 54), "Yes"),
            TextBox(Vector(61 if cancel else 93, 54), "No")]
        if cancel:
            self.elements.append(TextBox(Vector(96, 54), "Cancel"))

    def render(self):
        for element in self.elements:
            Interface.render(element)


class Handle(Handler):

    window = Query

    class press:
        async def left(window):
            window.finish(True)

        async def right(window):
            window.finish(False)

        async def back(window):
            window.finish(None)
