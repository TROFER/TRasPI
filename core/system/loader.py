import os
import core
import importlib.util
import core.load.load

__all__ = ["ProgramMenu"]

core.asset.Image("std::script", path="pyfile.icon")
core.asset.Image("std::folder", path="folder.icon")
core.asset.Image("std::return", path="return.icon")

VISABLE = 4

class Item:

    def __init__(self, name: str, image: str, path: str):
        self.icon = core.element.Image(core.Vector(0, 0), core.asset.Image(image))
        self.label = core.element.Text(core.Vector(0, 0), name, justify="L")
        self.name = name
        self.path = path

    def select(self):
        pass

    def render(self, index):
        self.icon.pos = core.Vector(5, 20 + 10 * index)
        self.icon.render()
        self.label.pos = core.Vector(12, 20 + 10 * index)
        self.label.render()

class FolderItem(Item):

    def __init__(self, name, path):
        super().__init__(name, "std::folder", path)

    def select(self):
        return ProgramMenu("{}/{}".format(self.path, self.name))

class ProgramItem(Item):

    def __init__(self, name, path):
        super().__init__(name, "std::script", path)

    def select(self):
        core.load.load.load(self.name, self.path)

class BackItem(Item):

    def __init__(self, name="Return", path=None):
        super().__init__(name, "std::return", path)

    def select(self):
        return None

class ProgramMenu(core.std.Menu):

    def __init__(self, path="programs"):
        # Backlight
        # Index /programs
        elements = []

        for item in os.listdir(f"{core.sys.PATH}{path}"):
            p = f"{core.sys.PATH}{path}/{item}"
            if "main.py" in os.listdir(p):
                image, func = "std::script", self._program
            elif os.path.isdir(p):
                image, func = "std::folder", self._folder
            elements.append(core.std.Menu.Element(
                core.element.Image(core.Vector(4, 0), core.asset.Image(image)),
                core.element.Text(core.Vector(10, 0), item, justify="L"),
                data = (item, path),
                select = func))
        elements.append(core.std.Menu.Element(
            core.element.Image(core.Vector(4, 0), core.asset.Image("std::return")),
            core.element.Text(core.Vector(10, 0), "Return", justify="L"),
            select = lambda s, w: w.back))

        super().__init__(*elements, title=path, end=False)

    def show(self):
        super().show()
        core.hardware.Backlight.gradient((240, 180, 240, 180, 240))

    @core.render.Window.focus
    def _folder(self, element, window):
        yield ProgramMenu("{}/{}".format(element.data[1], element.data[0]))
    @core.render.Window.focus
    def _program(self, element, window):
        yield core.load.load.load(*element.data)

    def back(self):
        core.hardware.Backlight.fill(255, 255, 255)
        self.finish()

class Handle(core.render.Handler):

    key = core.render.Button.RIGHT
    window = ProgramMenu

    def press(self):
        pass
        # self.window.change_sort() Wait for sort to be implemented

main = ProgramMenu()
