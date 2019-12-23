from core.render.single import Singleton

class PowerControls(metaclass=Singleton):

    def halt():
        print("WOULD HALT")
        # core.render.renderer.close()
        # core.Hardware.DisplayFunctions.clear()
        # os.system("halt")

    def restart():
        print("WOULD REBOOT")
        # core.render.renderer.close()
        # core.Hardware.DisplayFunctions.clear()
        # os.system("reboot")
