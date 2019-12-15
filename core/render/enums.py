import enum

@enum.unique
class Button(enum.IntEnum):
    UP = 0
    DOWN = 1
    BACK = 2
    LEFT = 3
    CENTRE = 4
    RIGHT = 5
    NONE = 6


@enum.unique
class Event(enum.Enum):
    NONE = None
    PRESS = "press"
    RELEASE = "release"
    HELD = "held"
