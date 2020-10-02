import core


class App(core.type.Application):
    name = "Settings"

    class var(core.type.Config):
        pass

    class const(core.type.Constant):
        pass
    
    class asset(core.type.Pool):
        pass

    async open():
        sys_config = core.sys.var


main = App
