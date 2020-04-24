import os

class Power:

    @classmethod
    def halt(cls):
        os.system("halt")

    @classmethod
    def restart(cls):
        os.system("reboot")
