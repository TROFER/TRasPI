import os
import core

core.asset.Template("home", path="core/resource/template/std_window.template")
core.asset.Image("pyscript", path="core/resource/icon/pyfile.icon")
core.asset.Image("folder", path="core/resource/icon/folder.icon")

class Item:

    def __init__(self, name: str, image: str):
        self.icon = core.element.Image(core.Vector(0, 0), core.asset.Image(image))
        self.label = core.element.Text(core.Vector(0, 0), name, justify="L")

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
        super().__init__(name, "folder")
        self.path = path

    def select(self):
        return ProgramMenu

class ProgramItem(Item):

    def __init__(self, name):
        super().__init__(name, "pyscript")

    def select(self):
        pass

class ProgramMenu(core.render.Window):

    template = core.asset.Template("home")

    def __init__(self, path="programs"):
        self.index = 0
        # Backlight
        core.hardware.Backlight.gradient((240, 180, 240, 180, 240))
        # Index /programs
        self.contents = []
        for item in os.listdir(f"{core.sys.PATH}{path}"):
            if "main.py" in os.listdir(f"{core.sys.PATH}{path}/{item}"):
                self.contents.append(ProgramItem(item))
            else:
                self.contents.append(FolderItem(item, path))
        # Elements
        self.title1 = core.render.element.Text(core.Vector(3, 5), "Programs", justify="L")
        self.cursor = core.render.element.Text(core.Vector(12 + self.contents[self.index].label._font_size()[0] + 3, self.contents[self.index].label.pos[1]), "<", justify="L")

    def render(self):
        self.title1.render()
        self.cursor.render()
        for index in range(min(4, len(self.contents))):
            item = self.contents[self.index + index]
            item.render(index)

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
