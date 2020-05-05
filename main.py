import core

# from home.main import main

if __name__ == "__main__":

    # print(core.sys.load.tree)
    # p = core.sys.load.app("home", "power")
    # print(p)
    # core.sys.load.close(p)

    main = core.sys.load.app("home", "main")
    # print(main.application.var)
    app = core.application.Application(main)
    core.Interface.run(app)
    #1694078748864
    #1694078756416
    #1694078748864