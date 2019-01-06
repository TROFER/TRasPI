import sys
levels = ["FATAL", "ERR", "WARN", "INFO"]

LEVEL = 4
FILE = "log"

def level(lvl=3):
    global LEVEL
    if type(lvl) == str:
        lvl = levels.index(lvl)
    LEVEL = lvl + 1

class name:
    def __init__(self, name="Log"):
        self.name = name
    def info(self, *msg):
        info(*msg, name=self.name)
    def warn(self, *msg):
        warn(*msg, name=self.name)
    def err(self, *msg):
        err(*msg, name=self.name)
    def fatal(self, *msg):
        fatal(*msg, name=self.name)

def output(msg, name, lvl):
    if lvl < LEVEL:
        message = "[{}] ({}) {}".format(levels[lvl], name.title() if name else "Log", "".join((str(i) for i in msg)))
        print(message)
        with open("error/"+FILE+".txt", "a") as file:
            file.write(message+"\n")

def info(*msg, name=None):
    output(msg, name, 3)
def warn(*msg, name=None):
    output(msg, name, 2)
def err(*msg, name=None):
    output(msg, name, 1)
def fatal(*msg, name=None):
    output(msg, name, 0)

with open("error/"+FILE+".txt", "w") as file:
    file.write("Logging Setup Successful\n\n")
