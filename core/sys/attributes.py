import sys
import os
from core.type.config import Config
from core.type.constant import Constant

__all__ = ["SysConstant", "SysConfig"]

class SysConstant(Constant):
    width = 128
    height = 7
    path = os.path.dirname(os.path.abspath(sys.argv[0])).replace("\\", "/") + "/"
    platform = "NT" if os.name == "nt" else "POSIX"
    pipeline = "DUMMY" # "GFXHAT" or "DUMMY"


class SysConfig(Config):
    brightness = 65