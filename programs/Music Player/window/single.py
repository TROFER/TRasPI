import core
from core.std import menu
from core import Vector
from app import App
from window import player
from core.render.element import Text

class Main(menu.Menu):

    def __init__(self, data=None):
        if data is None:
            data = App.var.library
        elements = []
        if isinstance(data, list) or isinstance(data, Genre):
            for container in data:
                elements.append(menu.MenuElement(
                    *[Text(Vector(0, 0), f"{container.name[:16]}[{len(container.items)}]", justify='L')],
                    data = container.items,
                    func = self.select))
            super().__init__(*elements, title=f"Library - MP", end=False)

        elif isinstance(data, Album):
            for track in data:
                elements.append(menu.MenuElement(
                    *[Text(Vector(0, 0), track.name, justify='L')],
                    func = track,
                    select = self.select))
            super().__init__(*elements, title=f"{data.name} - MP", end=False)


    async def select(self, element, window):
        if isinstance(element.data, Track):
            await player.Main(Playlist(element.name, [element]))
        else:
            await Main(element.data)

class Handle(core.input.Handler):

    window = Main

    class press:
        async def right(null, window: Main):
            window.finish(1)

        async def left(null, window: Main):
            pass
            window.finish(-1)
