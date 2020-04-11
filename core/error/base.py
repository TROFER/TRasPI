__all__ = [
"CoreException",
"ExecutorProcess", "ExecutorProcessCPU", "ExecutorProcessIO"
]

class CoreException(Exception):

    def __init__(self, msg="Engine Error"):
        self.msg = msg

    def __str__(self) -> str:
        return "Error" if self.msg is None else self.msg.__str__()

class ExecutorProcess(CoreException):

    def __init__(self, err: Exception):
        self.err = err

    def __str__(self) -> str:
        return f"{self.err.__class__.__name__}: {self.err}"

class ExecutorProcessCPU(ExecutorProcess):
    pass
class ExecutorProcessIO(ExecutorProcess):
    pass

class Event(CoreException):

    def __init__(self, err: Exception, key: str, event: str, handler: "Handler", window: "Window"):
        self.err, self.key, self.event, self.handler, self.window = err, key, event, handler, window

    def __str__(self) -> str:
        return f"{self.event}-{self.key} {self.err.__class__.__name__}<{self.err}> {self.handler} {self.window}"