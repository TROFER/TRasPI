import core
import gpiozero
import psutil
import time

class HardwareWindow(core.render.Window):

    template = core.asset.Template("std::window")

    def __init__(self):
        self.time = time.time()
        core.hardware.Backlight.fill(255, 255, 255)
        self.title = core.element.Text(core.Vector(3, 5), "HW_Info", justify="L")
        self.labels = [core.element.Text(core.Vector(3, 15), justify="L"),
        core.element.Text(core.Vector(3, 25), justify="L"),
        core.element.Text(core.Vector(3, 35), justify="L")]
        self.update()

    def update(self):
        if time.time() - self.time > 10:
            self.data = gpiozero.CPUTemperature(), psutil.cpu_percent(), psutil.virtual_memory()
            for index, label in enumerate(self.labels):
                label.text(self.data[index])
            self.time = time.time()
        else:
            print("False")

    def render(self):
        self.update()
        for label in self.labels:
            label.render()
        self.title.render()

class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = HardwareWindow

    def press(self):
        self.window.finish()

main = HardwareWindow()
