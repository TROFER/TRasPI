import core

if __name__ == "__main__":

    core.sys.load.rescan("home/")
    core.sys.load.rescan("programs/")
    main = core.sys.load.app("home", "main")
    app = core.application.Application(main)
    core.Interface.run(app)
