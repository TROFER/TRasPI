import os
from ..interface import Interface

class Power:

    def halt(cls):
        Interface.stop()
        # Disabled so i don't accidently turn it off
        # os.system("halt")

    def restart(cls):
        Interface.stop()
        # Disabled so i don't accidently turn it off
        # os.system("reboot")

Power = Power()