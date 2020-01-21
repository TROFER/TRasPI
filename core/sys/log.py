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
    def log(cls, error):
        _error = exception_info(error)
        try:
            with open(f"{core.sys.PATH}core/error/eventlog.txt", 'r') as eventlog:
                data = json.load(eventlog)
        except (IOError, json.JSONDecodeError):
            data = []
        with open(f"{core.sys.PATH}core/error/eventlog.txt", 'w') as eventlog:
            data.append(_error)
            json.dump(data, eventlog)

