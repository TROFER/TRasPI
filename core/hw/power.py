import os
from ..interface import Interface
from ..error.attributes import SysConstant
class Power:

    TIMER = 5

    if SysConstant.pipeline == "GFXHAT":

        def __init__(self):
            from ..driver import pijuice
            if pijuice.available():
                self.__juice = pijuice.PiJuice(1, 0x14)
            else:
                self.__juice = None

        def halt(self):
            Interface.stop()
            if self.__juice is not None:
                self.__juice.power.SetPowerOff(30)
            os.system(f"""nohup bash -c "sleep {self.TIMER}; shutdown -h now" > /dev/null 2>&1 &""")

        def restart(self):
            Interface.stop()
            os.system(f"""nohup bash -c "sleep {self.TIMER}; shutdown -r now" > /dev/null 2>&1 &""")

    else:

        def halt(cls):
            Interface.stop()

        def restart(cls):
            Interface.stop()

Power = Power()
