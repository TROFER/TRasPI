import core
import os
from core.render.element import Text, Image
from core.asset.image import Image as ImageAsset
from core import Vector
from core.std import menu
from app import App
import shutil
import os


class Open(menu.Menu):

    def __init__(self, target=None, directories=True):
        if target is None:
            target = App.const.path
        elements = []
        for obj in os.scandir(target):
            if obj.is_dir() and directories:
                elements.append(menu.MenuElement(
                    Text(Vector(0, 0), obj.name, justify='L'),
                    data=obj.path,
                    func=self.open_folder))
            elif obj.is_file and obj.name.split(".")[-1] in ["png", "jpg"]:
                elements.append(menu.MenuElement(
                    Text(Vector(0, 0), obj.name, justify='L'),
                    data=obj.path,
                    func=self.open_file))
        super().__init__(*elements, title=target)

    async def open_folder(self, path):
        await Open(target=path)

    async def open_file(self, path):
        await Viewer(path)


class Viewer(core.render.Window):

    def __init__(self, path):
        shutil.copy(path, f"{core.sys.const.path}programs/Photo Viewer/resource/temp/current.image")
        self.image = Image(Vector(0, 0), ImageAsset(f"programs/Photo Viewer/resource/temp/current"), just_w='L')
        super().__init__()

    def render(self):
        core.interface.render(self.image)


class Handle(core.input.Handler):

    window = Viewer

    class press:
        async def down(null, window):
            os.remove(f"{core.sys.const.path}programs/Photo Viewer/resource/temp/current.image")
            window.finish()


App.window = Open
main = App
