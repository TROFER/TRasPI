"""
from core.error import RenderError
from core.render.renderer import Renderer
from core.render.screen import render
from core.hardware.hardware import Backlight, Button
from core.hardware.display import Display

def open():
    Renderer().start()
    Backlight.fill(255, 255, 255)
    Display.clear()
    #Button.led(True)
    # Display.contrast(40)

def loop():
    open()
    try:
        renderer = Renderer()
        while renderer._render_event.is_set():
            render()
            renderer.frame()
    except Exception as e:
        raise RenderError("Main Render Loop") from e
    finally:
        close()

def close():
    Renderer().close()
    Backlight.fill(0, 0, 0)
    Button.led(False)
    Display.clear()

"""