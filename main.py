try:
    import core
except ImportError as e:
    raise OSError("FAILURE TO LOAD CORE!") from e

try:
    module = core.sys.load.window("main", "home/")
except core.error.SystemLoadError as e:
    raise core.error.FatalCoreException("FAILURE TO BOOT!") from e

while True:
    try:
        try:
            module.main.show()
            core.render.loop()
        except core.error.RenderError as e:
            raise core.error.FatalCoreException() from e
    except core.error.FatalCoreException as e:
        # core.system.log.Log.error("MAIN", e._log())
        print(e._log())
