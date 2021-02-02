from . import pijuice
PiJuice = pijuice.PiJuice
def available() -> bool:
    return pijuice.PiJuice().status.GetChargeLevel()["error"] == "NO_ERROR"
