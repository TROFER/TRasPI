from core.error import RenderError
from core.render.renderer import Render
from core.render.screen import render
from core.hardware.hardware import Backlight, Button
from core.hardware.display import Display

def open():
    Render().start()
    #Backlight.fill(255, 255, 255)
    #Button.led(True)
    Display.clear()
    # Display.contrast(40)

def loop(func: callable=None):
    if func is None:
        func = lambda: None

    open()
    try:
        renderer = Render()
        while renderer._render_event.is_set():
            func()
            render()
            renderer.frame()
    except Exception as e:
        raise RenderError("Main Render Loop") from e
    finally:
        close()

def close():
    Render().close()
    Backlight.fill(0, 0, 0)
    Button.led(False)
    Display.clear()
