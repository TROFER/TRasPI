import os
from ..interface import Interface
from ..error.attributes import SysConstant

if SysConstant.pipeline == "GFXHAT":
    from ..driver import pijuice

    class Power:

        def __init__(self):
            self.__juice = pijuice.PiJuice(1, 0x14)

        def halt(self):
            self.__juice.power.SetPowerOff(30)
            os.system("shutdown -h now")

        def restart(self):
            os.system("reboot")
else:
     class Power:

        def halt(cls):
            Interface.stop()

        def restart(cls):
            Interface.stop()

Power = Power()