from render.single import Singleton

__all__ = ["Screen"]

class Screen(metaclass=Singleton):

    def __init__(self):
        self.active = None
        self.callstack = []
        self.test = [lambda *args: None] * 6 # TEMP

    def call_focus(self, generator, window):
        self.callstack.append((window, generator))

    def call_lost(self) -> tuple:
        return self.callstack.pop()

    def show(self, window):
        self.active = window
        self.bind_handles()

    def bind_handles(self):
        for key, handler in enumerate(self.active._handles):
            if handler is None:
                self.test[key] = lambda *args: None # TEMP
                continue
            def wrap(handler):
                def handle(ch, event):
                    try:
                        func = getattr(handler(self.active), event)
                    except AttributeError:    return
                    result = func()
                    if type(result).__name__ == "generator":
                        self.active._handle_focus(None, result)

                return handle
            # print("BIND", key, wrap(handler))
            self.test[key] = wrap(handler) # TEMP
            # lcd.bind(key, wrap(handler))

    def render(self):
        self.active.render()

def render():
    Screen().render()
