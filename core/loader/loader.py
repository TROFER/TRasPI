import os
import core
import core.sys

core.asset.Template("home", path="core/resource/template/std_window.template")
core.asset.Image("pyscript", path="core/resource/icon/pyfile.icon")
core.asset.Image("folder", path="core/resource/icon/folder.icon")

class ProgramMenu(core.render.Window):

    def __init__(self):
        # Backlight Cfg
        core.hardware.Backlight.gradient((0, 44, 44, 0, 0))
        # Load Templates / Icons
        self.template = core.asset.Template("home")
        self.py_icon = core.asset.Image("pyscript")
        self.folder_icon = core.asset.Image("folder")
        # Index /programs
        self.contents = []
        self.index = 0
        for item in os.listdir(f"{core.sys.PATH}programs"):
            if item[len(item)-3:] == ".py":
                self.contents.append((item, self.py_icon))
            elif "." in item:
                pass
            else:
                self.contents.append((item, self.folder_icon))
        self.contents.insert(0, ("return", "RETURN"))
        while len(self.contents) % 4 != 0:
            self.contents.append(("", ""))
        # Elements
        self.dynamic_elements()
        self.title1 = core.render.element.Text(core.Vector(3, 5), "Programs", justify="L")

    def dynamic_elements(self):
        self.table = [
        core.render.element.Text(core.Vector(12, 20), (self.contents[self.index][0]).capitalize(), justify="L"),
        core.render.element.Text(core.Vector(12, 30), (self.contents[self.index + 1][0]).capitalize(), justify="L"),
        core.render.element.Text(core.Vector(12, 40), (self.contents[self.index + 2][0]).capitalize(), justify="L"),
        core.render.element.Text(core.Vector(12, 50), (self.contents[self.index + 3][0]).capitalize(), justify="L")]
        self.cursor = core.render.element.Text(core.Vector(12 + self.table[self.index]._font_size()[0] + 3, self.table[self.index].pos[1]), "<", justify="L")
        self.icons = [
        core.render.element.Image(self.contents[self.index][1], core.Vector(1, 20)),
        core.render.element.Image(self.contents[self.index + 1][1], core.Vector(1, 30)),
        core.render.element.Image(self.contents[self.index + 2][1], core.Vector(1, 40)),
        core.render.element.Image(self.contents[self.index + 3][1], core.Vector(1, 50))
        ]

    def render(self):
        self.dynamic_elements()
        for element in self.table:
            element.render()
        #for icon in self.icons: #While waiting for workaround
            #icon.render()

    def up(self):
        if self.index + 1 < len(self.contents) - 1:
            self.index += 1

    def down(self):
        if self.index - 1 > 0:
            self.index -= 1

    @core.render.Window.focus
    def select(self):
        if ".py" in self.contents[self.index][0]:
            command = self.content[self.index][0]
        else:
            pass
            # Needs to open a submenu with items from the folder

        res = yield command

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
    window = Mainwindow

    def press(self):
        pass
        # self.window.change_sort() Wait for sort to be implemented

main = ProgramMenu()
