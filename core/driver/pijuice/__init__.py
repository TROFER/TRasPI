from . import pijuice
PiJuice = pijuice.PiJuice
def available() -> bool:
    return pijuice.get_versions()[1] is not None
