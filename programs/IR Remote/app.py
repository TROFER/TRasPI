import core


class App(core.type.Application):
    name = "IR Remote"

    class var(core.type.Config):
        pass

    class const(core.type.Constant):
        Path = f"{core.sys.const.path}user/remotes/"
        Port = "/dev/ttyUSB0"
        Baudrate = 9600
        Timeout = 2

    class asset(core.type.Pool):
        ReceiveScreen = core.asset.Image("irReceive")


main = App
