import core
import time

def log(appid=None, type='None', desc='None'):
    if appid is None:
        print("Cannot create log missing 'appid'")
        return
    try:
        logfile =  open(f"{core.sys.PATH}core/log.txt", 'a')
    except IOError:
        logfile = open(f"{core.sys.PATH}core/log.txt", 'w+')
    logfile.write(f"[{type}] -{time.time()}- {desc}")
