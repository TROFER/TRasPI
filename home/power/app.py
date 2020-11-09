import core


class App(core.type.Application):
    name = "Power Window"

    class var(core.type.Config):
        pass

    class const(core.type.Constant):
        pass

    class asset(core.asset.Pool):
        pass