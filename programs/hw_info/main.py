import core
import gpiozero
import psutil
import time

class HardwareWindow(core.render.Window):

    def __init__(self):
        self.time = time.time()
        core.hardware.backlight.fill(255, 255, 255)
        self.title = core.render.element.Text(core.Vector(3, 5), "HW_Info", justify="L")
        self.labels = [core.element.Text(core.Vector(3, 10), justify="L"),
        core.element.Text(core.Vector(3, 20), justify="L"),
        self.element.Text(core.Vector(3, 30), justify="L")]
        self.update()

    def update(self):
        if time.time() - self.time > 1000:
            self.data = gpiozero.CPUTemperature(), psutil.cpu_percent(), psutil.virtual_memory()
            for index, label in enumerate(self.labels):
                label.text(self.data[index])
            self.time = time.time()

    def render(self):
        self.update()
        for label in self.labels:
            label.render()
        title.render()

class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = HardwareWindow

    def press(self):
        self.window.finish()

main = HardwareWindow()
