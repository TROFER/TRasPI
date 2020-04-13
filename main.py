import core



if __name__ == "__main__":

    App.window = TWin()
    app = core.application.Application(App)
    core.Interface.run(app)