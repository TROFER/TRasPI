import core
import json

__all__ = ["SettingsWindow"]

class SettingsWindow(core.std.MenuSingle):
    """ Open all the other settings windows. """

    def __init__(self):
        super().__init__(Core=Core())

class _Settings(core.std.Menu):
    """ Parent class for all settings """

    def __init__(self, file: str):
        self._file = file # file to .cfg
        # Elements
        self.title = core.element.Text(core.Vector(3, 5), "", justify="L")

        elements = [
            core.std.Menu.Element(core.element.Text(core.Vector(0, 0), "Test")),
        ]

        super().__init__(*elements)

    def render(self):
        self.title()
        super().render()

    def load(self):
        with open(self._file, "r") as file:
            self.data = json.load(file)

    def save(self):
        with open(self._file, "w") as file:
            json.dump(self.data, file)

    def __enter__(self):
        self.load()
    def __exit__(self, *args):
        self.save()

class Core(_Settings):
    """ Core settings """

    def __init__(self):
        super().__init__(core.sys.PATH+"core/system/system.cfg") 

class Application(_Settings):
    """ Application settings"""

    def __init__(self):
        super()._init__("test")


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
