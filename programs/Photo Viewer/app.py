import core

class App(core.type.Application):
    name = "Photo Viewer"

    class var(core.type.Config):
        pass

    class const(core.type.Constant):
        pass

    class asset(core.type.Pool):
        pass

main = App