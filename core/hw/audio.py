import os
import subprocess
from ..interface import Interface
from ..error.attributes import SysConstant, SysConfig

if SysConstant.pipeline == "GFXHAT":
    _FLAG = True
else:
    _FLAG = False

if _FLAG:
    class Audio:

        def __init__(self):
            os.system(f"amixer set Headphone {SysConfig.volume}%")
            self.volume = SysConfig.volume

        def current(self):
            return self.volume
            
        def increse(self, percent):
            if self.volume + percent <= 100:
                os.system(f"amixer set Headphone {self.volume + percent}%")
                self.volume += percent
        
        def decrese(self, percent):
            if self.volume - percent >= 0:
                os.system(f"amixer set Headphone {self.volume - percent}%")
                self.volume -= percent

        def set(self, percent):
            if 0 <= percent >= 100:
                os.system(f"amixer set Headphone {percent}%")
                self.volume = percent
else:
     class Audio:

        def current(cls):
             return 0
        
        def increse(cls, percent):
            pass
        
        def decrese(cls, percent):
            pass

        def set(cls, percent):
            pass
        
Audio = Audio()
