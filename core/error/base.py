import traceback

__all__ = [
"CoreException",
"ExecutorProcess", "ExecutorProcessCPU", "ExecutorProcessIO",
"Event",
]

def _fmt_exc_only(error: Exception):
    return traceback.format_exception_only(type(error), error)[0][:-1]

def _fmt_exc(error: Exception):
    return "".join(traceback.format_exception(error, error, error.__traceback__))

class CoreException(Exception):

    def __init__(self, msg="Engine Error"):
        self.msg = msg

    def __str__(self) -> str:
        return "Error" if self.msg is None else self.msg.__str__()

class ExecutorProcess(CoreException):

    def __init__(self, err: Exception):
        self.err = err

    def __str__(self) -> str:
        return f"{_fmt_exc_only(self.err)}"

class ExecutorProcessCPU(ExecutorProcess):
    pass
class ExecutorProcessIO(ExecutorProcess):
    pass

class Event(CoreException):

    def __init__(self, err: Exception, key: str, event: str, handler: "Handler", window: "Window"):
        self.err, self.key, self.event, self.handler, self.window = err, key, event, handler, window

    def __str__(self) -> str:
        return f"{self.handler.__module__}.{self.handler.__qualname__}.{self.event}-{self.key} on {type(self.window).__qualname__} | {_fmt_exc_only(self.err)}\nFull Cause: {_fmt_exc(self.err)}"

class Load(CoreException):

    def __init__(self, msg="Load Error"):
        super().__init__(msg)