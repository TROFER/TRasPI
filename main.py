import core

if __name__ == "__main__":

    # Read SysConfig
    core.sys.io.ConfigCache.read("core/", core.sys.var)

    # Load Home Screen Application
    core.sys.load.rescan("home/")
    main = core.sys.load.app("home", "main", default=True)
    app = core.application.Application(main)

    # Run Main Loop
    core.Interface.run(app)
    core.sys.io.ConfigCache.write("core/", core.sys.var)