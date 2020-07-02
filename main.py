import core

if __name__ == "__main__":

    main = core.sys.load.app("home", "main")
    app = core.application.Application(main)
    core.Interface.run(app)
