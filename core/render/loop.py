from core.render.renderer import Render
from core.render.screen import render

def loop(func: callable=None):
    if func is None:
        func = lambda: None

    renderer = Render()
    renderer.start()
    try:
        while renderer._render_event.is_set():
            func()
            render()
            renderer.frame()
    except BaseException:
        print("Exiting")
    finally:
        renderer.close()
