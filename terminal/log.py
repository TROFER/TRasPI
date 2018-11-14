levels = ["FATAL", "ERR", "WARN", "INFO"]

def output(msg, name, lvl):
    print("[{}] {}: {}".format(name, levels[lvl], msg))

def info(msg, name="Log"):
    output(msg, name, 3)
def warn(msg, name="Log"):
    output(msg, name, 2)
def err(msg, name="Log"):
    output(msg, name, 1)
def fatal(msg, name="Log"):
    output(msg, name, 0)
