import core
from core.std import menu
from ..types import Genre, Album, Track, Playlist
from core import Vector
from ..app import App
import player

class Main(menu.Menu):

    def __init__(self, data):
        if data is None:
            data = App.var.library
        elements = []
        if isinstance(data, list) or isinstance(data, Genre):
            for container in data:
                elements.append(menu.MenuElement(
                    *[Text(Vector(0, 0), container.name[:19], justify='L'), Text(Vector(128, 0), len(container.items), justify='R')],
                    data = container.items,
                    select = self.select))
            super().__init__(*elements, title=f"Music Player - {container.name}", end=False)

        elif isinstance(data, Album):
            for track in data:
                elements.append(menu.MenuElement(
                    *[Text(Vector(0, 0), track.name, justify='L')],
                    data = track,
                    select = self.select))
            super().__init__(*elements, title=f"Music Player - {data.name}", end=False)


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
