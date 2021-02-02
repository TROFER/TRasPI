from ..error.attributes import SysConstant
if SysConstant.pipeline == "GFXHAT":
    _FLAG = True
    from ..driver import pijuice
else:
    _FLAG = False

__all__ = ["Battery"]

class Battery:

    if _FLAG and pijuice.available():

        def __init__(self):
            self.__juice = pijuice.PiJuice(1, 0x14)

        def percentage(self) -> int:
            """Current Battery Charge %"""
            return self.__juice.status.GetChargeLevel()["data"]
        def temperature(self) -> int:
            """Temperature of the Battery"""
            return self.__juice.status.GetBatteryTemperature()["data"]
        def status(self) -> bool:
            """Returns True if charging"""
            if self.__juice.status.GetStatus()["data"]["powerInput"] == "PRESENT":
                return True
            else:
                return False
        def voltage(self) -> int:
            """Returns battery voltage"""
            return self.__juice.status.GetBatteryVoltage()["data"]
        def amperage(self) -> int:
            """Returns battery amerage"""
            return self.__juice.status.GetIoCurrent()()["data"]

    else: # _FLAG

        def __init__(self):
            pass

        def percentage(self) -> int:
            """Current Battery Charge %"""
            return 0
        def temperature(self) -> int:
            """Temperature of the Battery"""
            return 0

        def status(self) -> bool:
            """Returns True if charging"""
            return None

        def voltage(self) -> float:
            """Returns battery voltage"""
            return 0

        def amerage(self) -> float:
            """Returns battery amerage"""
            return 0

Battery = Battery()
