import core

class App(core.type.Application):
    name = "Weather"

    class var(core.type.Config):
        alternative_locations = [
            "Isle of wight".replace(" ", "%20")
        ]
        refresh_period = 2

    class const(core.type.Constant):
        path = f"{core.sys.const.path}user/openweatherkey.txt"
        default_location = "Isle of wight".replace(" ", "%20")

    class asset(core.type.Pool):
        Bitocra7 = core.asset.Font("bitocra7", 7)
        DSEG_Weather = core.asset.Font("DSEG-Weather", 62)
        DSEG7ClassicMini_Regular = core.asset.Font("DSEG7ClassicMini-Regular", 20)

main = App