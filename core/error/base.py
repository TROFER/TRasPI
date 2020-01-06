__all__ = ["FatalCoreException", "WindowError", "RenderError", "AssetError", "HardwareError"]

class MetaCoreError(type):

    node = "NODE"

    def __new__(cls, name, bases, dct):
        if "__str__" in dct:
            def new_str(func):
                def _str_(self):
                    return "{}: {}".format(self.__class__.__name__, func(self))
                return _str_
            dct["__str__"] = new_str(dct["__str__"])
        return super().__new__(cls, name, bases, dct)

    def __call__(cls, *args, **kwargs):
        self = super().__call__(*args, **kwargs)
        return self

class CoreBaseException(Exception, metaclass=MetaCoreError):

    def __init__(self, msg=""):
        self.msg = msg

    def __str__(self) -> str:
        return self.msg.__str__()

    def __repr__(self) -> str:
        return self.__str__()

    def log(self):
        _string = "{}\n\t".format(self)
        _string += self._log_()
        return _string

    def _log_(self):
        _string = ""
        if self.__cause__:
            if isinstance(self.__cause__, CoreBaseException):
                _string += "{}\n\t".format(self.__cause__._log_())
            else: # 'tb_frame', 'tb_lasti', 'tb_lineno', 'tb_next'
                # .__traceback__.tb_frame.f_code.co_filename
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

    def __init__(self, handler):
        self.handler = handler

    def __str__(self) -> str:
        return "Window: {}".format(handler.window)

class FocusError(CoreBaseException):

    def __init__(self, window):
        self.window = window

    def __str__(self) -> str:
        return "{}".format(self.window)
