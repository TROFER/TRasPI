from ..interface import Interface
from ..error.attributes import SysConstant, SysConfig
from ..sys.proc import Process

if SysConstant.pipeline == "GFXHAT":
    _FLAG = True
else:
    from ..driver.dummy import audio as DummyAudio
    _FLAG = False

class Audio:

    if _FLAG:
        def __init__(self):
            self.__update()
    else:
        def __init__(self):
            self.__volume = DummyAudio.Volume(SysConfig.volume)

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

    def update(self, *args, **kwargs):
        self.__update()

    if _FLAG:
        def __update(self):
            Process(f"amixer set Headphone {SysConfig.volume}%", shell=True)
    else:
        def __update(self):
            self.__volume.set(SysConfig.volume)

if SysConstant.process:
    Audio = Audio()
    SysConfig._callback_ = ("volume", Audio.update)