import os
import core
import importlib.util

core.asset.Template("home", path="std_window.template")
core.asset.Image("pyscript", path="pyfile.icon")
core.asset.Image("folder", path="folder.icon")
core.asset.Image("return", path="return.icon")

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
        self.icon.pos = core.Vector(2, 15 + 10 * index)
        self.icon.render()
        self.label.pos = core.Vector(12, 20 + 10 * index)
        self.label._calc_justify()
        self.label.render()

class FolderItem(Item):

    def __init__(self, name, path):
        super().__init__(name, "folder", path)

    def select(self):
        return ProgramMenu("{}/{}".format(self.path, self.name))

class ProgramItem(Item):

    def __init__(self, name, path):
        super().__init__(name, "pyscript", path)

    def select(self):
        path = "{}{}/{}/main.py".format(core.sys.PATH, self.path, self.name)
        spec = importlib.util.spec_from_file_location("module", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.main

class BackItem(Item):

    def __init__(self, name="Return", path=None):
        super().__init__(name, "return", path)

    def select(self):
        return None

class ProgramMenu(core.render.Window):

    template = core.asset.Template("home")

    def __init__(self, path="programs"):
        self.index = 0
        self.cursor_index = self.index
        # Backlight
        core.hardware.Backlight.gradient((240, 180, 240, 180, 240))
        # Index /programs
        self.contents = []
        for item in os.listdir(f"{core.sys.PATH}{path}"):
            p = f"{core.sys.PATH}{path}/{item}"
            if "main.py" in os.listdir(p):
                self.contents.append(ProgramItem(item, path))
            elif os.path.isdir(p):
                self.contents.append(FolderItem(item, path))
        self.contents.append(BackItem())
        # Elements
        self.title1 = core.render.element.Text(core.Vector(3, 5), "Programs", justify="L")
        self.cursor = core.render.element.Text(core.Vector(12 + self.contents[self.cursor_index].label._font_size()[0] + 3, 20), "<", justify="L")

    def render(self):
        self.title1.render()
        self.cursor.render()
        for index in range(min(VISABLE, len(self.contents))):
            item = self.contents[self.index + index]
            item.render(index)

    def _update_cursor(self):
        self.cursor.pos = core.Vector(12 + self.contents[self.cursor_index].label._font_size()[0] + 3, self.contents[self.cursor_index].label.pos[1])
        self.cursor._calc_justify()

    def up(self):
        if self.cursor_index > 0:
            self.cursor_index -= 1
            if self.cursor_index < self.index:
                self.index -= 1
            self._update_cursor()

    def down(self):
        if self.cursor_index + 1 < len(self.contents):
            self.cursor_index += 1
            if self.cursor_index >= self.index + VISABLE:
                self.index += 1
            self._update_cursor()

    @core.render.Window.focus
    def select(self):
        res = self.contents[self.cursor_index].select()
        if res is not None:
            yield res
        else:
            self.finish()

    def show(self):
        super().show()
        core.hardware.Backlight.gradient((240, 180, 240, 180, 240))

class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = ProgramMenu

    def press(self):
        self.window.select()

class Handle(core.render.Handler):

    key = core.render.Button.UP
    window = ProgramMenu

    def press(self):
        self.window.up()

class Handle(core.render.Handler):

    key = core.render.Button.DOWN
    window = ProgramMenu

    def press(self):
        self.window.down()

class Handle(core.render.Handler):

    key = core.render.Button.RIGHT
    window = ProgramMenu

    def press(self):
        pass
        # self.window.change_sort() Wait for sort to be implemented

main = ProgramMenu()
