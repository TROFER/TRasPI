import itertools
import os
import time

from core import asset
from core.hw.backlight import Backlight
from core.input.event import Handler
from core.interface import Interface
from core.render import Window
from core.render.element import Image, Rectangle, Line, Text
from core.sys.attributes import SysConfig, SysConstant
from core.vector import Vector
from home.loader import program
from home.app import App


class Loader:

    APP_DEFAULT = asset.Image("app-default")
    FOLDER_DEFAULT = asset.Image("folder-default")

    def index(self, path):
        apps = []
        for package in os.scandir(SysConstant.path + path):
            if package.is_dir:
                contents = [item.name for item in list(
                    os.scandir(SysConstant.path + path + package.name))]
                if "main.py" in contents:
                    if "app-icon.image" in contents:
                        icon = asset.Image(
                            SysConstant.path + path + package.name + "app-icon")
                    else:
                        icon = self.APP_DEFAULT
                    apps.append(program.Program(
                        SysConstant.path + path + package.name, icon))
                else:
                    if "folder-icon" in contents:
                        icon = asset.Image(
                            SysConstant.path + path + package.name + "folder-icon")
                    else:
                        icon = self.FOLDER_DEFAULT
                    apps.append(program.Folder(
                        SysConstant.path + path + package.name, icon))
        return apps

    def run(self, target):
        Backlight.fill(SysConfig.colour)


class AppDrawer(Window, Loader):

    POSITIONS = [(12, 13), (39, 13), (66, 13), (93, 13),
                 (12, 39), (39, 39), (66, 39), (93, 39)]
    ICON_SCALE = Vector(24, 24)

    def __init__(self, path='programs/'):
        super().__init__()
        self.index, self.pos = 0, 0
        self.pages = self.group(8, super().index(path))
        self.icons = []
        for page in self.pages:
            for i, app in enumerate(page):
                self.icons.append(Image(*Vector(self.POSITIONS[i]), app.icon, just_w='L'))
        self.elements = [
            Text(Vector(3, 5), "App Drawer", justify='L'),
            Text(Vector(127, 5), time.strftime("%I:%M%p"), justify='R'),
            Line(Vector(0, 10), Vector(128, 10)),
            Rectangle(Vector(*self.POSITIONS[0]), Vector(*self.POSITIONS[0]) + self.ICON_SCALE)]
        App.interval(self.refresh)

    def group(self, groupsize, iterable, fillvalue=None):
        args = [iter(iterable)] * groupsize
        pages = list(itertools.zip_longest(*args, fillvalue=fillvalue))
        for i in range(len(pages)):
            page = list(pages[i])
            while None in page:
                page.remove(None)
            pages[i] = page
        return pages

    def render(self):
        for icon in self.icons[8 * self.index : 8 * self.index + 8]:
            Interface.render(icon)
        for element in self.elements:
            Interface.render(element)

    def refresh(self):
        self.elements[-1].pos1 = Vector(*self.POSITIONS[self.pos]) + Vector(-1, -1)
        self.elements[-1].pos2 = Vector(*self.POSITIONS[self.pos]) + self.ICON_SCALE


class Handle(Handler):

    window = AppDrawer

    class press:
        async def left(null, window):
            if window.pos > 0:
                window.pos -= 1
                window.refresh() 

        async def right(null, window):
            if window.pos < len(window.pages[window.index])-1:
                window.pos += 1
                window.refresh()

        async def up(null, window):
            if window.index > 0:
                window.index -= 1
                window.refresh()

        async def down(null, window):
            if window.index < len(window.pages)-1:
                window.index += 1
                window.refresh()

        async def centre(null, window):
            target = window.pages[window.index][window.pos].location
            if isinstance(target, program.Program):
                window.run(target)
            else:
                await(AppDrawer(target))

        async def back(null, window):
            window.finish()


class AppList(Loader):
    pass


main = AppDrawer()
