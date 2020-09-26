from ..error.attributes import SysConstant
if SysConstant.pipeline == "GFXHAT":
    _FLAG = True
    from ..driver import pijuice
else:
    _FLAG = False

__all__ = ["Battery"]

class Battery:

    if _FLAG:

        def __init__(self):
            self.__juice = pijuice.PiJuice()

        def percentage(self) -> int:
            """Current Battery Charge %"""
            self.__juice.status.GetChargeLevel()["data"]
        def temperature(self) -> int:
            """Temperature of the Battery"""
            self.__juice.status.GetBatteryTemperature()["data"]

    else: # _FLAG

        def __init__(self):
            pass

        def percentage(self) -> int:
            """Current Battery Charge %"""
            return 0
        def temperature(self) -> int:
            """Temperature of the Battery"""
            return 0

Battery = Battery()