from core.render.window import Window
from core.interface import Interface
from core.input.event import Handler
from core.render.element import Text
from core.vector import Vector
from core.asset import Template


class Info(Window):

    template = Template("info")

    def __init__(self, message):
        self.message = Text((38, 27), message[:20], justify='L')

    def render(self):
        Interface.render(self.message)


class Handle(Handler):

    window = Info

    class press:
        async def centre(window):
            window.finish()


class Warning(Info):
    template = Template("warning")


class Error(Info):
    template = Template("error")
