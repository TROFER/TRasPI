class Power:

    @classmethod
    def halt(cls):
        core.render.renderer.close()
        core.Hardware.Display.clear()
        os.system("halt")

    @classmethod
    def restart(cls):
        core.render.renderer.close()
        core.Hardware.Display.clear()
        os.system("reboot")
