import logging
import inspect as __inspect

_active_program = "INVALID PROGRAM"
def __setup():
    import multiprocessing as __mp
    if __mp.current_process().name != "MainProcess":
        level = logging.NOTSET
        handler = logging.NullHandler(level)
        handler_traceback = logging.NullHandler(level)
    else:
        from .attributes import SysConstant as __SysConstant
        # READ FROM CONFIG
        filename = f"{__SysConstant.path}log/output.log"
        level = logging.DEBUG
        handler = logging.FileHandler(filename, mode="w", encoding="utf-8") if filename else logging.StreamHandler()
        filename = f"{__SysConstant.path}log/traceback.log"
        handler_traceback = logging.FileHandler(filename, mode="w", encoding="utf-8") if filename else logging.StreamHandler()

    class Dispatch:
        def __init__(self, formatters, defaut):
            self.formatters = formatters
            self.default_format = defaut

        def format(self, record):
            return self.formatters.get(record.name, self.default_format).format(record)

    loggers = [
        logging.getLogger(name) for name in ("core", "core.program", "CoreTraceback")
    ]

    handler.setFormatter(Dispatch({logger.name: fmt for logger, fmt in zip(loggers[:-1], (
        logging.Formatter("[{asctime}>{levelname}] {module}.{funcName} -> {message}", datefmt="%H:%M:%S", style="{"),
        logging.Formatter("[{asctime}>{levelname}] {program_name}@{module}.{funcName} -> {message}", datefmt="%H:%M:%S", style="{")
    ))}, logging.Formatter("FAIL: {processName}-{name} -> {message}", style="{")))

    loggers[0].setLevel(level)
    loggers[0].addHandler(handler)

    handler_traceback.setFormatter(logging.Formatter("[{asctime}>{levelname}] {module}.{funcName}:{message}", datefmt="%H:%M:%S", style="{"))
    loggers[-1].setLevel(level)
    loggers[-1].addHandler(handler_traceback)

    loggers[0].debug("Enabled Logging[%s]: %s", logging.getLevelName(level), ", ".join(log.name for log in loggers))
    return loggers

core, program, traceback = __setup()

def log(level, msg, *args, **kwargs):
    return program.log(level, msg, *args, extra={"program_name": _active_program}, stacklevel=2, **kwargs)
def debug(msg, *args, **kwargs):
    return program.debug(msg, *args, extra={"program_name": _active_program}, stacklevel=2, **kwargs)
def info(msg, *args, **kwargs):
    return program.info(msg, *args, extra={"program_name": _active_program}, stacklevel=2, **kwargs)
def warning(msg, *args, **kwargs):
    return program.warning(msg, *args, extra={"program_name": _active_program}, stacklevel=2, **kwargs)
def error(msg, *args, **kwargs):
    return program.error(msg, *args, extra={"program_name": _active_program}, stacklevel=2, **kwargs)
def critical(msg, *args, **kwargs):
    return program.critical(msg, *args, extra={"program_name": _active_program}, stacklevel=2, **kwargs)
def exception(msg, *args, **kwargs):
    return program.exception(msg, *args, extra={"program_name": _active_program}, stacklevel=2, **kwargs)
