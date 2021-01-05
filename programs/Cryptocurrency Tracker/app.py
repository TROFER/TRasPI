import core

class App(core.type.Application):
    name = "Crypto Tracker"

    class var(core.type.Config):
        pass

    class const(core.type.Constant):
        pass

    class asset(core.type.Pool):
        title_font = core.asset.Font("bitocra-13-full", 13)
        ethereum = core.asset.Image("eth-logo")
        bitcoin = core.asset.Image("btc-logo")

        
