import core

class App(core.type.Application):

    class var(core.type.Config):
        pass

    class const(core.type.Constant):
        pass

    class asset(core.type.Pool):
        pass

    # We will set this later
    # window = MainWindow()

# Tells core this is the main app
main = App