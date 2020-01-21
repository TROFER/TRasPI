import core
import json
import time

class Log:

    @classmethod
    def log(cls, _type, _error):
        try:
            logfile = open(f"{core.sys.PATH}core/error/eventlog.txt", 'r')
        except IOError:
            logfile = open(f"{core.sys.PATH}core/error/eventlog.txt", 'w')
        json.dump([{"type": _type,
         "time": time.strftime("%d/%m/%y @ %H:%M"),
         "line" : _error.line}])
