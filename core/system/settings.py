import core
import json

__all__ = ["SettingsWindow"]

class SettingsWindow(core.render.Window):
    """ Open all the other settings windows. """

    template = core.asset.Template("std::window", path="window.template")
    icon_core = core.asset.Template("core", path=f"{core.sys.PATH}core/resource/image/config_large.icon")
    icon_cmd = core.asset.Template("cmd", path=f"{core.sys.PATH}core/resource/image/cmd.icon")

    def __init__(self):
        self.index = 0
        self.title1 = core.element.Text(core.Vector(3, 5), "Settings", justify="L")
        self.core_icon = core.element.Image(core.Vector(42, 32), core.asset.Image("icon_core"))
        self.core_icon = core.element.Image(core.Vector(84, 32), core.asset.Image("icon_cmd"))
        # Needs cursors


        super().__init__(Core=Core())

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
