import itertools

from core.input.event import Handler
from core.interface import Interface
from core.render import Window
from core.render.element import Image
from core.render.element import Rectangle
from core.sys.attributes import SysConstant
from core.vector import Vector
from home import app


class Loader:

    def index(self, path="programs/"):
        apps = []
        for program in os.scandir(SysConstant.path + path):
            if program.is_dir():
                with os.scandir(SysConstant.path + program) as app:
                    if "main.py" in app:
                        if "app.icon" in app:
                            icon = Image(
                                f"{SysConstant.path}{program}/app.icon")
                        else:
                            icon = Image(
                                f"{SysConstant.path}core/resource/image/code.icon")
                        apps.append(
                            App(app, f"{SysConstant.path}programs/{app}", icon))
        return apps

    def run(self, target):
        pass


class AppDrawer(Window, Loader):

    POSITIONS = [(27, 21), (54, 21), (84, 21),
                 (27, 42), (54, 42), (84, 42)]
    ICON_SCALE = 15

    def __init__(self):
        self.index, self.pos = 0, 0
        self.pages = self.group(6, super().index())
        self.icons = [Image(Vector(self.POSITIONS[i]), app.icon)
                      for i, app in enumerate(page) for page in self.pages]
        self.elements = [
            Rectangle(Vector(0, 0))
        ]

    def group(self, groupsize, iterable, fillvalue=None):
        args = [iter(iterable)] * groupsize
        pages = list(itertools.zip_longest(*args, fillvalue=fillvalue))
        for page in pages:
            while None in page:
                page.remove(None)
        return pages

    def render(self):
        for icon in self.icons[self.index]:
            Interface.render(icon)
        for element in self.elements:
            Interface.render(element)

    def refresh(self):
        self.elements[0].pos1 = Vector(*self.POSITIONS[self.pos])
        self.elements[0].pos2 = Vector(
            *self.POSITIONS[self.pos]) + self.ICON_SCALE


class Handle(Handler):

    window = AppDrawer

    class press:
        async def left(null, window):
            if window.pos > 0:
                window.pos -= 1

        async def right(null, window):
            if window.pos < len(window.pages[window.pos])-1:
                window.pos += 1

        async def up(null, window):
            if window.index > 0:
                window.index -= 1

        async def down(null, window):
            if window.index < len(window.pages)-1:
                window.index += 1

        async def centre(null, window):
            window.run()

        async def back(null, window):
            window.finish()


class AppList(Loader):
    pass


# main = AppDrawer()
main = "fekoff"
