from ..vector import Vector
from ..error.attributes import SysConstant as const

__all__ = [""]

centre = Vector(const.width // 2, const.height // 2)

# Next to Buttons
button_up = Vector(0, 0)
button_down = Vector(0, 0)
button_home = Vector(0, 0)
button_left = Vector(0, 0)
button_right = Vector(0, 0)
button_centre = Vector(0, 0)

# Title Bar
title = Vector(3, 5)