import sys
import os

PATH = os.path.dirname(os.path.abspath(sys.argv[0])).replace("\\", "/") + "/"
WIDTH, HEIGHT = 128, 64

class PowerOptions():

    def halt(self):
        os.system("halt")

    def restart(self):
        os.system("reboot")
