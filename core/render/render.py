from core.error import RenderError
from core.render.renderer import Renderer
from core.render.screen import Screen
from core.hardware.hardware import Backlight, Button
from core.hardware.display import Display
from core.sys.single import Singleton
from core.sys.config import Config

# from core.sys.config import Config

# Config("system")

__all__ = ["Render"]

class Render(metaclass=Singleton):

    def __init__(self):
        self.render = Renderer()
        self.screen = Screen()

    def open(self):
        Backlight.fill(255, 255, 255)
        Display.contrast(Config("std::system")["display_contrast"]["value"])
        Display.clear()
        self.render.open()
    def close(self):
        self.render.close()
        Backlight.fill(0, 0, 0)
        Button.led(False)
        Display.clear()

    def update(self):
        if self.render._render_event.is_set() and self.render._pause_event.is_set():
            try:
                self.screen.process_events()
                self.render.frame()
                self.screen.render()
            except Exception as e:
                raise RenderError("Main Render Loop") from e

    def pause(self):
        self.render.pause()
    def resume(self):
        self.render.resume()

    def __enter__(self):
        self.open()
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        return self.close()