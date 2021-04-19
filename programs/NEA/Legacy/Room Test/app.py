import core

class App(core.type.Application):
    name = "Room Test"

    class var(core.type.Config):
        pass

    class const(core.type.Constant):
        path = f"{core.sys.const.path}user/dungeon_quest_dat/"

    class asset(core.type.Pool):
        pass

main = App