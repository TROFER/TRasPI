import os
import core
import core.sys

class ProgramMenu(core.render.Window):

    def __init__(self):
        # Load Template
        self.contents = []
        self.index = 0
        # Index /programs
        for item in os.listdir(f"{core.sys.PATH}programs"):
            if item[len(item)-3:] == ".py":
                self.contents.append((item, ".py"))
            else:
                self.contents.append((item, "folder"))
        while self.contents % 4 != 0:
            self.contents.append(("", ""))
        # Elements
        self.dynamic_elements()
        self.title1 = core.render.element.Text(core.Vector(3, 5), "Programs")

    def dynamic_elements(self):
        self.table = [
        core.render.element.Text(core.Vector(12, 10), self.contents[self.index][0]),
        core.render.element.Text(core.Vector(12, 10), self.contents[self.index + 1][0]),
        core.render.element.Text(core.Vector(12, 10), self.contents[self.index + 2][0]),
        core.render.element.Text(core.Vector(12, 10), self.contents[self.index + 3][0])]
        self.cursor = core.render.element.Text(core.Vector(12 + self.table[self.index]._font_size()[0] + 3, self.table[self.index].pos[1]), "<", justify="L")

    def render(self):
        dynamic_elements()
        for element in self.table:
            element.render()
        self.title1.render()

main = ProgramMenu()
