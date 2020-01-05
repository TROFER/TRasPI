import core
import time

def make_log(entry):
    try:
        log = open(f"{core.sys.PATH}core/log.txt", 'a')
    except IOError:
        log = open(f"{core.sys.PATH}core/log.txt", "w+")

class Log:

    @classmethod
    def error(cls, name, traceback):
        make_log(f"[Error]@({time.strftime("%I:%M:%S")}) '{traceback}' appid={name}")

    @classmethod
    def warning(cls, name, description):
        make_log(f"[Warning]@({time.strftime("%I:%M:%S")}) '{description}' appid={name}")

    @classmethod
    def infomation(cls, name, infomation):
        make_log(f"[Information]@({time.strftime("%I:%M:%S")}) '{infomation}' appid={name}")
