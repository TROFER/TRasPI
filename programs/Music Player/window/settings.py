import core
from ..app import App
from ..main import Main
from core.std import Numpad, Query
from core.render.element import Text, Rectangle, Line


class Main(core.render.Window):

    def __init__(self):
        self.index = 0
        self.elements = [
            Text(Vector(64, 3), "Music Player - Settings"),
            Line(Vector(0, 7), Vector(128, 7)),
            Rectangle(Vector(0, 10), Vector(128, 18),
                      outline=0, str="Sleep Timer"),
            Rectangle(Vector(0, 18), Vector(128, 26), outline=1, str="Repeat")
            Rectangle(Vector(0, 36), Vector(128, 44), outline=1, str="Rescan Library")]

        def render(self):
            for element in self.elements:
                core.interface.render(element)


class Handle(core.input.Handler):

    window = Settings

    class press:
        async def up(null, window: Main):
            if window.index == 2:
                window.index = 0

        async def down(null, window: Main):
            if window.index == 0:
                window.index = 2

        async def centre(null, window: Main):
            if window.index == 0:
                App.player.sleeptimer = await Numpad(min=, max=180, default=30, title="Set Sleep Timer")
            elif window.index == 1:
                res = await Query("Repeat Track", title="Repeat", cancel=True)
                if res is not None:
                    App.player.repeat = res
            else:
                Main.rescan()
