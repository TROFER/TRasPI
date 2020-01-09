import core
import json
import cmd

__all__ = ["SettingsWindow"]

class SettingsWindow(core.render.Window):
    """ Open all the other settings windows. """

    template = core.asset.Template("std::window")
    core.asset.Image("core", path="config.icon")
    core.asset.Image("cmd", path="cmd.icon")
    core.asset.Image("cursor", path="cursor.icon")

    def __init__(self):
        self.index = 0
        self.title = core.element.Text(core.Vector(3, 5), "Settings", justify="L")
        self.core_icon = core.element.Image(core.Vector(42, 32), core.asset.Image("core"))
        self.cmd_icon = core.element.Image(core.Vector(84, 32), core.asset.Image("cmd"))
        self.cursor = core.element.Image(core.Vector(42 * (self.index + 1), 18), core.asset.Image("cursor"))

    def left(self):
        if self.index > 0:
            self.index -= 1

    def right(self):
        if self.index < 1:
            self.index += 1

    def select(self):
        if self.index == 0:
            window = Core()
        elif self.index == 1:
            window = cmd.cmd()
        yield window

    def render(self):
        self.title.render()
        self.core_icon.render(), self.cmd_icon.render()
        core.element.Image(core.Vector(42 * (self.index + 1), 18), core.asset.Image("cursor"))
        self.cursor.render()

class Handle(core.render.Handler):

    key = core.render.Button.UP
    window = StartScreen

    def press(self):
        self.window.left()

class Handle(core.render.Handler):

    key = core.render.Button.UP
    window = StartScreen

    def press(self):
        self.window.right()

    class Handle(core.render.Handler):

        key = core.render.Button.UP
        window = StartScreen

        def press(self):
            self.window.select()

    class Handle(core.render.Handler):

        key = core.render.Button.UP
        window = StartScreen

        def press(self):
            self.window.finish()

class _Settings(core.std.Menu):
    """ Parent class for all settings """

    def __init__(self, file: str, title: str):
        self._file = file # file to .cfg
        # Elements

        self.load()
        elements = []
        for name, data in self.data.items():
            elements.append(core.std.Menu.Element(
                core.element.Text(core.Vector(0, 0), data["name"], justify="L"),
                data = {**data, "key": name},
                select = self.edit))

        super().__init__(*elements, title=title)

    def render(self):
        self.title.render()
        super().render()

    @core.render.Window.focus
    def edit(self, element, window):
        if element.data["type"] == "bool":
            res = yield core.std.Query(element.data["desc"], cancel=True)
            if res is None:
                res = element.data["value"]
        elif element.data["type"] == "int":
            res = yield core.std.Numpad(element.data["min"], element.data["max"], element.data["value"], element.data["desc"])
        element.data["value"] = res
        self.save()

    def load(self):
        with open(self._file, "r") as file:
            self.data = json.load(file)

    def save(self):
        with open(self._file, "w") as file:
            json.dump(self.data, file)

@core.render.Window.focus
class Core(_Settings):
    """ Core settings """

    def __init__(self):
        super().__init__(core.sys.PATH+"core/system/system.cfg", "Settings - Core")


## Notes ##
'''
core settings
program settings -edits config


Stuff to change (Core Settings):
bluetooth state
wifi conections?
exit local session
git pull?
'''
