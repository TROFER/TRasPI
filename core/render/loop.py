from core.render.renderer import Render
from core.render.screen import render

def loop(func: callable=None):
    if func is None:
        func = lambda: None

    renderer = Render()
    try:
        renderer.start()
        while renderer._render_event.is_set():
            func()
            render()
            renderer.frame()
    except BaseException as e:
        print("Exiting", e)
        raise
    finally:
        renderer.close()
