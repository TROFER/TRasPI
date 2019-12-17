from core.render.single import Singleton
import sys
import os

PATH = os.path.dirname(os.path.abspath(sys.argv[0])).replace("\\", "/") + "/"
WIDTH, HEIGHT = 128, 64

class PowerOptions(metaclass=Singleton):

    def halt(self):
        os.system("halt")

    def restart(self):
        os.system("reboot")
