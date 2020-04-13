import core

from home.main import main

if __name__ == "__main__":

    app = core.application.Application(main)
    core.Interface.run(app)