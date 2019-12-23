import core
import time

class Power:

    @classmethod
    def halt(cls):
        core.render.renderer.close()
        core.Hardware.Display.clear()
        time.sleep(0.2)
        os.system("halt")

    @classmethod
    def restart(cls):
        core.render.renderer.close()
        core.Hardware.Display.clear()
        time.sleep(0.2)
        os.system("reboot")
