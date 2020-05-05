import os
from core.sys.attributes import SysConstant

_clear_sys_ = "cls" if SysConstant.platform == "NT" else "clear"
__image = [[2 for x in range(SysConstant.width)] for y in range(SysConstant.height)]

def setup():
    for y in __image:
        for x in range(SysConstant.width):
            y[x] = 2

def clear():
    for y in __image:
        for x in range(SysConstant.width):
            y[x] = 0

if SysConstant.pipeline == "DUMMYNR": # Dummy No Render
    def show():
        return
else:
    def show():
        os.system(_clear_sys_)
        for y in __image:
            print("".join("#" if i else " " for i in y))

def set_pixel(x: int, y: int, value: int):
    __image[y][x] = value