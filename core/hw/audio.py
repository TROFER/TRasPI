import os
import subprocess
from ..interface import Interface
from ..error.attributes import SysConstant, SysConfig

if SysConstant.pipeline == "GFXHAT":
    _FLAG = True
else:
    _FLAG = False

class Audio:

    def __init__(self):
        self.__update()

    def current(self):
        return SysConfig.volume

    def increse(self, percent):
        SysConfig.volume = min(SysConfig.volume + percent, 100)
        self.__update()
    
    def decrese(self, percent):
        SysConfig.volume = max(SysConfig.volume - percent, 0)
        self.__update()

    def set(self, percent):
        SysConfig.volume = max(min(percent, 100), 0)
        self.__update()

    if _FLAG:
        def __update(self):
            os.system(f"amixer set Headphone {SysConfig.volume}%")

    else:
        def __update(self):
            pass

Audio = Audio()
