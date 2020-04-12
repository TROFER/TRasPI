import core
from app import App

class MainWindow(core.render.Window):

    # Set a template for the background of the window
    # template = 

    def __init__(self):
        super().__init__()

        # Some variables
        self.count = 0

        # Set up some elements
        self.text = core.element.Text(
            core.Vector(core.sys.const.width // 2, core.sys.const.height // 2), # The position of the element
            "This is a Text Element", # Text
            # Font
        )

        self.counter = core.element.Text(
            core.Vector(core.sys.const.width // 2, core.sys.const.height // 2 + 16), # Position
            self.count,
            # Font
        )

    def render(self):
        # Called every frame
        # Render the elements
        core.interface.render(self.text)

    async def show(self):
        # Called when the window is shown and given focus

        self.count += 1
        self.counter.text = self.count

class HandlerMainWindow(core.input.Handler):

    window = MainWindow # The Window to bind the Handler to

    class press: # Type of event - e.g. press events

        @core.input.event # Enforce func is spelt correctly - Not required
        async def down(null, window: MainWindow):
            # Name corresponds to the button required to invoke the callback
            # window will be the window that has invoked the function
            window.count -= 1

        @core.input.event
        async def centre(null, window: MainWindow):

            # Finish will end this window and return to the previous window in the stack
            window.finish(window.count)

        @core.input.event
        async def up(null, window: MainWindow):
            # To call a new window, await on the window object
            self.count = await SecondWindow(self.count)



class SecondWindow(core.render.Window):

    def __init__(self, count: int):
        super().__init__()

        self.count = count
