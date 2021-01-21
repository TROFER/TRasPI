import core

class App(core.type.Application):
    name = "System Information"

    class var(core.type.Config):
        pass

    class const(core.type.Constant):
        # Global
        colour = (255, 153, 102)
        # Remote Config Only
        server_address = "192.168.1.216"
        refresh_period = 1.5

    class asset(core.type.Pool):
        pass

main = App