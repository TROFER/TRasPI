import itertools
import os

from core import asset
from core.hw.backlight import Backlight
from core.input.event import Handler
from core.interface import Interface
from core.render import Window
from core.render.element import Image, Rectangle
from core.sys.attributes import SysConfig, SysConstant
from core.vector import Vector
from home import folder, program


class Loader:

    APP_DEFAULT = asset.Image("app-default")
    FOLDER_DEFAULT = asset.Image("folder-default")

    def index(self, path):
        apps = [] 
        for package in os.scandir(SysConstant.path + path):
            if package.is_dir:
                contents = [item.name for item in list(os.scandir(SysConstant + path + package))]
                if "main.py" in contents:
                    if "app-icon.image" in contents:
                        icon = asset.Image(SysConstant.path + path + package + "app-icon")
                    else:
                        icon = self.APP_DEFAULT
                    apps.append(program.Program(SysConstant.path + path + package, icon))
                else:
                    if "folder-icon" in contents:
                        icon = asset.Image(SysConstant.path + path + package + "folder-icon")
                    else:
                        icon = self.FOLDER_DEFAULT
                    apps.append(folder.Folder(SysConstant.path + path + package, icon))
        return apps

    def run(self, target):
        Backlight.fill(SysConfig.colour)
 


class AppDrawer(Window, Loader):

    POSITIONS = [(27, 21), (54, 21), (84, 21),
                 (27, 42), (54, 42), (84, 42)]
    ICON_SCALE = 15

    def __init__(self, path='programs/'):
        self.index, self.pos = 0, 0
        self.pages = self.group(6, super().index(path))
        self.icons = []
        for page in self.pages:
            self.icons.append([Image(Vector(self.POSITIONS[i]), app.icon)
                               for i, app in enumerate(page)])
        self.elements = [
            Rectangle(Vector(0, 0), Vector(128, 64))]

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
            target = self.pages[self.index][self.pos]
            if isinstance(target, program.Program):
                self.run(target)
            else:
                await(AppDrawer(target))

        async def back(null, window):
            window.finish()


class AppList(Loader):
    pass


main = AppDrawer()
