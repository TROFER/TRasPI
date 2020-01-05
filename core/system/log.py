import core
import time

def make_log(string):
    try:
        log = open(f"{core.sys.PATH}core/log.txt", 'a')
        log.write('\n')
    except IOError:
        log = open(f"{core.sys.PATH}core/log.txt", "w")
    log.write(string)
    log.close()

class Log:

    @classmethod
    def error(cls, name, traceback):
        make_log(f"[Error]@({time.strftime('%I:%M:%S')}) '{traceback}' appid={name}")

    @classmethod
    def warning(cls, name, description):
        make_log(f"[Warning]@({time.strftime('%I:%M:%S')}) '{description}' appid={name}")

    @classmethod
    def infomation(cls, name, infomation):
        make_log(f"[Information]@({time.strftime('%I:%M:%S')}) '{infomation}' appid={name}")
