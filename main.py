if __name__ == "__main__":
    import core

    # Read Config
    core.sys.io.ConfigCache.read("core/", core.sys.var)
    # Schedule Write Config
    core.interface.termintate.schedule(core.sys.io.ConfigCache.write, "core/", core.sys.var)

    # Load Home Screen Application
    core.sys.load.rescan("home/")
    main = core.sys.load.app("home", "main", default=True)
    app = core.application.Application(main)

    # Run Main Loop
    core.Interface.main(app)