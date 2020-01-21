import core
import json
import time
import traceback


def exception_info(error: Exception) -> dict:
    if error.__cause__ is not None:
        cause = exception_info(error.__cause__)
    else:
        cause = {}

    trace = traceback.extract_tb(error.__traceback__)
    stack = []
    for frame in trace:
        stack.append({
            "lineno": frame.lineno,
            "file": frame.filename,
            "name": frame.name,
            "line": frame.line
        })

    return {
        "type": error.__class__.__name__,
        "message" : str(error),
        "line": stack[-1]["line"],
        "time": time.strftime("%d/%m/%y @ %H:%M"),

        "stack": stack,
        "cause": cause
    }

class Log:

    @classmethod
    def log(cls, , _error, _message=None, _type):
        _error = exception_info(_error)
        try:
            logfile = json.load(open(f"{core.sys.PATH}core/error/eventlog.txt", 'r'))
        except IOError:
            logfile = open(f"{core.sys.PATH}core/error/eventlog.txt", 'w')
        try:
            newfile = logfile.append(_error)
        except:
            logfile.append(f"[{_type}] {_message}")
        with open(f"{core.sys.PATH}core/error/eventlog.txt", 'w') as oldfile:
            json.dump(logfile, oldfile)
        logfile.close()
