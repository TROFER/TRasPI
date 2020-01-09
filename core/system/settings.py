import core
import json

__all__ = ["SettingsWindow"]

class SettingsWindow(core.render.Window):
    """ Open all the other settings windows. """

    template = core.asset.Template("std::window")
    core.asset.Image("core", path="config.icon")
    core.asset.Image("cmd", path="cmd.icon")

    def __init__(self):
        self.index = 0
        self.title = core.element.Text(core.Vector(3, 5), "Settings", justify="L")
        self.core_icon = core.element.Image(core.Vector(42, 32), core.asset.Image("core"))
        self.cmd_icon = core.element.Image(core.Vector(84, 32), core.asset.Image("cmd"))
        # Needs cursors

    def render(self):
        self.title.render()
        self.core_icon.render(), self.cmd_icon.render()

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

class Core(_Settings):
    """ Core settings """

    def __init__(self):
        super().__init__(core.sys.PATH+"core/system/system.cfg", "Settings - Core")

class Application(_Settings):
    """ Application settings"""

    def __init__(self):
        super()._init__("test", "Settings - App")

def Action(name: str, func: callable):
    return core.std.Menu.Element(
        core.element.Text(core.Vector(0, 0), name, justify="L"),
        select=func)

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
