from core.error.base import SystemError

class SystemLoadError(SystemError):
    pass

class SystemLoadModuleError(SystemLoadError):
    pass

class SystemLoadWindowError(SystemLoadError):
    pass
