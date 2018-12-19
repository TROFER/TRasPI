import core.log
import _thread
import time

log = core.log.name("Execute")
flag = False

def exec(module, *args):
    global flag
    flag = False
    _thread.start_new_thread(_run, (module.main, *args))
    while not flag:
        time.sleep(0.005)
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
            return False
    flag = True
