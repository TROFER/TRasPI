from core.render.window import Window
from core.interface import Interface
from core.input.event import Handler
from core.render.element import Text
from core.vector import Vector


class Info(Window):

    # template = core.asset.Template("std::info", path="info.template")

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
    # template = core.asset.Template("std::warning", path="warning.template")
    pass


class Error(Info):
    # template = core.asset.Template("std::error", path="error.template")
    pass
