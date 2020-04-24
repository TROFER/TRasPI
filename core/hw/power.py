import os

class Power:

    def halt(cls):
        os.system("halt")

    def restart(cls):
        os.system("reboot")

Power = Power()