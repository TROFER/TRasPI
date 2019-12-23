from core.render.single import Singleton

class PowerControls(metaclass=Singleton):

    def halt(self):
        print("WOULD HALT")
        # os.system("halt")

    def restart(self):
        print("WOULD REBOOT")
        # os.system("reboot")
