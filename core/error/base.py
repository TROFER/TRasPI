__all__ = ["FatalCoreException", "WindowError", "RenderError", "AssetError", "HardwareError", "FocusError", "EventError", "SystemError"]

class CoreBaseException(Exception):

    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self) -> str:
        return self.msg.__str__()
    def __repr__(self) -> str:
        return self.__str__()

    def _log(self):
        _string = "{}\n\t".format(self)
        _string += self._log_()
        return _string

    def _log_(self):
        _string = ""
        if self.__cause__:
            if isinstance(self.__cause__, CoreBaseException):
                _string += "{}\n\t".format(self.__cause__._log_())
            else:
                _string += "Line[{}:{}] {}: {}\n\t".format(self.__cause__.__traceback__.tb_lineno, self.__cause__.__traceback__.tb_frame.f_code.co_name, self.__cause__.__class__.__name__, self.__cause__)
        _string += "Line[{}:{}] {}".format(self.__traceback__.tb_lineno, self.__cause__.__traceback__.tb_frame.f_code.co_name, self)
        return _string

class FatalCoreException(CoreBaseException):
    pass

class WindowError(CoreBaseException):

    def __init__(self, window, msg):
        self.window = window
        self.msg = msg

    def __str__(self) -> str:
        return "{} -> {}".format(self.window, self.msg)

class ScreenError(CoreBaseException):
    pass

class WindowStackError(ScreenError):
    pass

class RenderError(CoreBaseException):
    pass

class AssetError(CoreBaseException):
    pass

class HardwareError(CoreBaseException):
    pass

class EventError(CoreBaseException):

    def __init__(self, window, handler):
        self.window = window
        self.handler = handler

    def __str__(self) -> str:
        return "Window: {} {}".format(self.window, self.handler)

class FocusError(CoreBaseException):

    def __init__(self, window):
        self.window = window

    def __str__(self) -> str:
        return "WINDOW {}".format(self.window)

class SystemError(CoreBaseException):
    pass
