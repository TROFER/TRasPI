from core.render.single import Singleton

class PowerControls(metaclass=Singleton):

    def halt():
        print("WOULD HALT")
        # os.system("halt")

    def restart():
        print("WOULD REBOOT")
        # os.system("reboot")
