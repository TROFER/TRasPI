import core
import sys


core.asset.Template("std::power", path="std_window.template")

class PowerMenu(core.render.Window):

    def __init__(self):



class PowerOptions():

    def halt(self):
        os.system("halt")

    def restart(self):
        os.system("reboot")
