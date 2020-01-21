try:
    import core
except ImportError as e:
    raise OSError("FAILURE TO LOAD CORE!") from e

try:
    module = core.sys.load.window("main", "home/")
except core.error.SystemLoadError as e:
    raise core.error.FatalCoreException("FAILURE TO BOOT!") from e

application = core.Application()

try:
    with application:
        module.main.show()
        application.run()
except core.error.FatalCoreException as e:
    core.sys.log(e)
    raise
