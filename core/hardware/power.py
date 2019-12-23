import core
import time

class Power:

    @classmethod
    def halt(cls):
        core.render.Render().close()
        core.hardware.Display.clear()
        time.sleep(1)
        os.system("halt")

    @classmethod
    def restart(cls):
        core.render.Render().close()
        core.hardware.Display.clear()
        time.sleep(1)
        os.system("reboot")
