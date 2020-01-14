import sys
import os

__all__ = ["PATH", "WIDTH", "HEIGHT"]

PATH = os.path.dirname(os.path.abspath(sys.argv[0])).replace("\\", "/") + "/"
WIDTH, HEIGHT = 128, 64
