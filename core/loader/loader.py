import os
import core
import core.sys

class ProgramMenu(core.render.Window):

    def __init__(self):
        # Load Template
        self.template = core.asset.Template("home", path="core/resource/template/std_window.template")
        # Index /programs
        self.contents = []
        self.index = 0
        for item in os.listdir(f"{core.sys.PATH}programs"):
            if item[len(item)-3:] == ".py":
                self.contents.append((item.capitalize(), ".py"))
            else:
                self.contents.append((item.capitalize(), "folder"))
        while len(self.contents) % 4 != 0:
            self.contents.append(("", ""))
        # Elements
        self.dynamic_elements()
        self.title1 = core.render.element.Text(core.Vector(3, 5), "Programs", justify="L")

    def dynamic_elements(self):
        self.table = [
        core.render.element.Text(core.Vector(12, 20), self.contents[self.index][0], justify="L"),
        core.render.element.Text(core.Vector(12, 40), self.contents[self.index + 1][0], justify="L"),
        core.render.element.Text(core.Vector(12, 50), self.contents[self.index + 2][0], justify="L"),
        core.render.element.Text(core.Vector(12, 60), self.contents[self.index + 3][0], justify="L")]
        self.cursor = core.render.element.Text(core.Vector(12 + self.table[self.index]._font_size()[0] + 3, self.table[self.index].pos[1]), "<", justify="L")

    def render(self):
        self.dynamic_elements()
        for element in self.table:
            element.render()
        self.title1.render()
        self.cursor.render()

main = ProgramMenu()
