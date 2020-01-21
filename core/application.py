import core.render
import core.error
from core.sys.single import Singleton
from core.sys.deltatime import DeltaTime

class Application(metaclass=Singleton):

    def __init__(self):
        self.running = True
        self.delta_time = DeltaTime()
        self.render = core.render.Render()

    def run(self):
        try:
            while self.running:
                self.delta_time.next()
                self.render.update()
        except core.error.RenderError as e:
            raise core.error.FatalCoreException from e
        finally:
            self.close()

    def open(self):
        self.render.open()
    def close(self):
        self.render.close()

    def pause(self, update=True):
        pass
    def resume(self):
        pass

    def __enter__(self):
        self.open()
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        return self.close()
