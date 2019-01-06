import core.log
import threading
import time

log = core.log.name("Execute")
flag = False

def exec(module, *args):
    global flag
    flag = False
    t = threading.Thread(target=_run, args=(module.main, *args))
    t.start()
    t.join()
    if isinstance(flag, BaseException):
        log.err("Error in module ({}): {}: {}".format(module.__name__, type(flag).__name__, flag))

def _run(func, *args):
    global flag
    try:
        func(*args)
    except BaseException as e:
        print(type(e).__name__, e)
        if type(e) not in (SystemExit, KeyboardInterrupt):
            flag = e
