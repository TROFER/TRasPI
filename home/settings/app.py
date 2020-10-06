import core


class App(core.type.Application):
    name = "Settings"

    class var(core.type.Config):
        pass

    class const(core.type.Constant):
        pass
    
    class asset(core.type.Pool):
        pass

    async def open():
        core.sys.io.ConfigCache.read("core/", core.sys.var)

    async def close():
        core.sys.io.ConfigCache.write("core/", core.sys.var)


main = App
