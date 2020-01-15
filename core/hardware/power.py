import core
import os
import time

class Power:

    @classmethod
    def halt(cls):
        os.system("halt")

    @classmethod
    def restart(cls):
        os.system("reboot")
