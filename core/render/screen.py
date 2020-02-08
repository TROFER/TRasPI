import core.error
from core.sys.single import Singleton
from core.hardware.touch import Touch
from core.sys.log import Log
import queue

__all__ = ["Screen"]

class Screen(metaclass=Singleton):

    def __init__(self, error_callback: callable=lambda e: None):
        self.active = None
        self.callstack = []
        self.callback = error_callback
        self.event_queue = queue.Queue()

        Touch.repeat(50)

    def template(self):
        return self.active.template

    def call_focus(self, generator, window):
        self.callstack.append((window, generator))

    def call_lost(self) -> tuple:
        try:
            return self.callstack.pop()
        except IndexError as e:
            raise core.error.WindowStackError() from None

    def show(self, window):
        self.active = window
        self.bind_handles()
        # print("SSHOW", self.active)

    def bind_handles(self):
        for key, handler in enumerate(self.active._handles):
            if handler is None:
                Touch.bind(key, lambda c, e: None)
                continue
            def wrap(handler):
                def handle(event):
                    try:
                        func = getattr(handler(self.active), event)
                    except AttributeError:    return
                    try:
                        print("Process:", handler)
                        return func()
                    except Exception as e:
                        # print("EVENT ERROR", e)
                        try: # TEMPORARY
                            raise core.error.EventError(handler) from e
                        except core.error.EventError as e:
                            Log.log(e)
                            self.callback(e)
                        return

                def send_to_queue(ch, event):
                    print("Event:", ch, event)
                    self.event_queue.put((handle, event))

                return send_to_queue
            Touch.bind(key, wrap(handler))

    def render(self):
        self.active.render()

    def process_events(self):
        try:
            while True:
                func, event = self.event_queue.get(False)
                func(event)
        except queue.Empty:    return

    def pause(self):
        pass

    def resume(self):
        pass

# from core.std.popup import Error
