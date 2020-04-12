import enum

__all__ = ["Key", "name"]

@enum.unique
class Key(enum.IntEnum):
    UP = 0
    DOWN = 1
    BACK = 2
    LEFT = 3
    CENTRE = 4
    RIGHT = 5

name = tuple([i.name.lower() for i in Key])