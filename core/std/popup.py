from ..render.window import Window
from ..interface import Interface
from ..input.event import Handler
from ..render.element import Text
from ..vector import Vector
from ..asset import Template

__all__ = ["Info", "Warning", "Error"]

class Info(Window):

    template = Template("info")

    def __init__(self, message):
        self.message = Text((38, 27), message[:20], justify='L')

    def render(self):
        Interface.render(self.message)


class Handle(Handler):

    window = Info

    class press:
        async def centre(null, window: Info):
            window.finish()


class Warning(Info):
    template = Template("warning")


class Error(Info):
    template = Template("error")
