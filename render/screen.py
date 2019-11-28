from render.single import Singleton

__all__ = ["Screen"]

class Screen(metaclass=Singleton):

    def __init__(self):
        self.active = None
        self._test = [None] * 6

    def show(self, window):
        print("SHOW", window)
        self.active = window
        self.bind_handles()

    def bind_handles(self):
        for key, handler in enumerate(self.active._handles):
            def handle(ch, event):
                try:
                    print("geting event")
                    func = getattr(handler(self.active), event)(self.active)
                except AttributeError:
                    print("err")
                    return
                print("running event")
                return func()
            # lcd.bind(handle)
            self._test[key] = handle

    def render(self):
        self.active.render()

    def test_event(self, key, event):
        print("TEST EVENT")
        self._test[key](key, event)

def render():
    Screen().render()

def test(key, event):
    Screen().test_event(key, event)
