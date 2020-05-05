import core

class App(core.type.Application):

    class var(core.type.Config):
        time_cache = [0, 0, 0, 0, 0]
        weather_cache = [0, {}]

    class const(core.type.Constant):
        time = "%I:%M%p"

    class asset(core.type.Pool):
        panel_font = core.asset.Font("bitocra7", 7)

    async def close():
        if None in App.var.time_cache:
            App.var.time_cache[0] = 0