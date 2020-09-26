import os
from ..interface import Interface

if SysConstant.pipeline == "GFXHAT":
    _FLAG = True
else:
    _FLAG = False

if _FLAG:
    class Power:

        def halt(cls):
            os.system("poweroff")

        def restart(cls):
            os.system("reboot")
else:
     class Power:

        def halt(cls):
            Interface.stop()

        def restart(cls):
            Interface.stop()

Power = Power()