import core
import gpiozero
import psutil
import time
import socket
import colorsys
dfsf

class HardwareWindow(core.render.Window):

    template = core.asset.Template("std::window")

    def __init__(self):
        self.time = time.time()
        R, G, B = colorsys.hsv_to_rgb(core.sys.Config(
            "std::system")["system_colour"]["value"] / 100, 1, 1)
        core.hardware.Backlight.fill(int(R * 255), int(G * 255), int(B * 255))
        self.title = core.element.Text(core.Vector(3, 5), "HW Info", justify="L")
        self.labels = [core.element.Text(core.Vector(3, 15), justify="L"),
        core.element.Text(core.Vector(3, 25), justify="L"),
        core.element.Text(core.Vector(3, 35), justify="L"),
        core.element.Text(core.Vector(3, 45), justify="L")]
        self.update()

    def update(self):
        if time.time() - self.time > 1:
            try:
                self.ip = [l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) if l][0][0]
            except OSError:
                self.ip = "Offline"
            self.data = (f"CPU Temp: {round(gpiozero.CPUTemperature().temperature, 1)}°C",
             f"CPU Usage: {psutil.cpu_percent()}%", f"Memory Usage: {psutil.virtual_memory().percent}%",
             f"IP: {self.ip}")
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
