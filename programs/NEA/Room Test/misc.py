import core
import os
import sys

def align(image, axis: str, alignment: str):
    alignments = {
        "x": {
            'C': 0 - (image.width / 2),
            'L': image.width,
            'R': 0 + image.width},
        "y": {
            'C': 0 - (image.height / 2),
            'T': image.height,
            'B': 0 - image.height}}
    return int(alignments[axis][alignment])

#CD = os.path.dirname(os.path.abspath(sys.argv[0])).replace("\\", "/") + "/"
CD = core.sys.const.path