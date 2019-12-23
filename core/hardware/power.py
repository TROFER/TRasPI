import core
import os
import time

class Power:

    @classmethod
    def halt(cls):
        core.render.close()
        time.sleep(1)
        os.system("halt")

    @classmethod
    def restart(cls):
        core.render.close()
        time.sleep(1)
        os.system("reboot")
