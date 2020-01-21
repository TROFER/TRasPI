from core.error import RenderError
from core.render.renderer import Renderer
from core.render.screen import Screen
from core.hardware.hardware import Backlight, Button
from core.hardware.display import Display
from core.sys.single import Singleton

# from core.sys.config import Config

# Config("system")

__all__ = ["Render"]

class Render(metaclass=Singleton):

    def __init__(self):
        self.render = Renderer()
        self.screen = Screen()

    def open(self):
        self.render.open()
        Backlight.fill(255, 255, 255)
        Display.clear()
    def close(self):
        self.render.close()
        Backlight.fill(0, 0, 0)
        Button.led(False)
        Display.clear()

    def update(self):
        if self.render._render_event.is_set() and not self.render._pause_event.is_set():
            try:
                print("Screen Render")
                self.screen.render()
                print("Render stack")
                self.render.frame()
            except Exception as e:
                raise RenderError("Main Render Loop") from e

    def pause(self):
        pass
    def resume(self):
        pass

    def __enter__(self):
        self.open()
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        return self.close()