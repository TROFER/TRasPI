import sys
levels = ["FATAL", "ERR", "WARN", "INFO"]

LEVEL = 4

def level(lvl=3):
    global LEVEL
    if type(lvl) == str:
        lvl = levels.index(lvl)
    LEVEL = lvl + 1

class name:
    def __init__(self, name="Log"):
        self.name = name
    def info(self, msg):
        info(msg, self.name)
    def warn(self, msg):
        warn(msg, self.name)
    def err(self, msg):
        err(msg, self.name)
    def fatal(self, msg):
        fatal(msg, self.name)

def output(msg, name, lvl):
    if lvl < LEVEL:
        print("[{}] ({}) {}".format(levels[lvl], name.title() if name else "Log", msg))

def info(msg, name=None):
    output(msg, name, 3)
def warn(msg, name=None):
    output(msg, name, 2)
def err(msg, name=None):
    output(msg, name, 1)
def fatal(msg, name=None):
    output(msg, name, 0)
