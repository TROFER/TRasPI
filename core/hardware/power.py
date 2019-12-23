from core.render.single import Singleton

class PowerControls(metaclass=Singleton):

    def halt():
        print("WOULD HALT")
        # os.system("halt")
        # core.render.renderer.close()
        # core.Hardware.DisplayFunctions.clear()

    def restart():
        print("WOULD REBOOT")
        # os.system("reboot")
        # core.render.renderer.close()
        # core.Hardware.DisplayFunctions.clear()
