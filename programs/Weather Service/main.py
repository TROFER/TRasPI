import core
import json
from urllib.error import HTTPError, URLError
from urllib import request
import time
import colorsys

core.asset.Template("weather", path="Weather Service/gui.template")
refresh_speed = 600 # Secconds


class Mainwindow(core.render.Window):

    def __init__(self):
        R, G, B = colorsys.hsv_to_rgb(core.sys.Config(
            "std::system")["system_colour"]["value"] / 100, 1, 1)
        core.hardware.Backlight.fill(int(R * 255), int(G * 255), int(B * 255))
        self.template = core.asset.Template("weather")
        self.API = "&appid=dd440727faee99efb0b572bc6d78e7b3"
        self.URL = "http://api.openweathermap.org/data/2.5/weather?"
        self.location = ["id=2641598", "Newport GB"]
        self.time = time.time()
        self.title = core.element.Text(core.Vector(3, 5), f"For {self.location[1]}", colour=1, justify="L")
        self.header1 = core.element.Text(core.Vector(3, 50), "Current Weather:", justify="L")
        self.get_weather()

    def render(self):
        if time.time() - self.time > refresh_speed:
            self.get_weather()
            self.time = time.time()
        self.title.render(), self.header1.render()
        self.tempreture.render(), self.pressure.render(), self.humidity.render(), self.wind.render()
        self.weather.render()

    @core.render.Window.focus
    def get_weather(self):
        try:
            self.data = json.load(request.urlopen(self.URL+self.location[0]+self.API, timeout=5))
        except:
            yield core.std.Error("Unable To Connect")
            return self.finish()
        self.tempreture = core.element.Text(core.Vector(3, 14), f"Temperature: {round(self.data['main']['temp'] - 273.1, 1)}°C", justify="L")
        self.pressure = core.element.Text(core.Vector(3, 22), f"Pressure: {self.data['main']['pressure']}Pa", justify="L")
        self.humidity = core.element.Text(core.Vector(3, 30), f"Humidity: {self.data['main']['humidity']}%", justify="L")
        self.wind = core.element.Text(core.Vector(3, 38), f"Wind Speed: {self.data['wind']['speed']}Mph", justify="L")
        self.weather = core.element.Text(core.Vector(3, 58), f"{self.data['weather'][0]['description'].capitalize()}", justify="L")

class Handle(core.render.Handler):

    key = core.render.Button.CENTRE
    window = Mainwindow

    def press(self):
        self.window.get_weather()

class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = Mainwindow

    def press(self):
        self.window.finish()

main = Mainwindow()
