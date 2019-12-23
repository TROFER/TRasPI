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
        if time.time() - self.time > 1:
            self.data = f"CPU Temp: {gpiozero.CPUTemperature().temperature}°C", f"CPU Usage: {psutil.cpu_percent()}%", f"Memory Usage: {psutil.virtual_memory().percent}%"
            print(self.data)
            for index, label in enumerate(self.labels):
                label.text(self.data[index])
            self.time = time.time()

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
