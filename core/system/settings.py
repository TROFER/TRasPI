import core
import json

class SettingsWindow(core.render.Window):
    """ Open all the other settings windows. """

    def __init__(self):
        pass

class _Settings(core.render.Window):
    """ Parent class for all settings """

    def __init__(self, file: str):
        self._file = file # file to .cfg
        # Elements
        self.title = core.element.Text(core.Vector(3, 5), "", justify="L")

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
        super()._init__()

class Application(_Settings):
    """ Application settings"""

    def __init__(self):
        super()._init__()


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
