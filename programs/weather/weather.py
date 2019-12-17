import core
import json
from urllib import request


class Mainwindow(core.render.Window):

    def __init__(self):
        self.template = f"{core.sys.PATH}programs/weather/gui.template"
        self.API = "&appid=dd440727faee99efb0b572bc6d78e7b3"
        self.URL = "http://api.openweathermap.org/data/2.5/weather?"
        self.location = "q=Isle of wight".replace(' ', '%20')
        self.title = core.render.element.Text(core.Vector(4, 4), f"For {self.location}", colour=0)
        self.header1 = core.render.element.Text(core.Vector(4, 54), "Current Weather:")
        self.header2 = core.render.element.Text(core.Vector(4, 59), "Connected to: Open Weather Map")
        self.get_weather()

    def render(self):
        self.title.render(), self.header1.render(), self.header2.render()
        self.tempreture.render(), self.pressure.render(), self.humidity.render(), self.wind.render()
        self.weather.render()

    def get_weather(self):
        self.data = json.load(request.urlopen(self.URL+self.location+self.API))
        self.tempreture = core.render.element.Text(core.Vector(4, 13), f"Temperature: {round(self.data['main']['temp'] - 273.1, 1)}")
        self.pressure = core.render.element.Text(core.Vector(4, 24), f"Pressure: {self.data['main']['pressure']}")
        self.humidity = core.render.element.Text(core.Vector(4, 33), f"Humidity: {self.data['main']['humidity']}")
        self.wind = core.render.element.Text(core.Vector(4, 42), f"Wind Speed: {self.data['main']['humidity']}")
        self.weather = core.render.element.Text(core.Vector(4, 63), f"{self.data['weather'][0]['description']}")

class Handle(core.render.Handler):

    key = core.render.Button.UP
    window = Mainwindow

    def press(self):
        self.window.get_weather()

class Handle(core.render.Handler):

    key = core.render.Button.BACK
    window = Mainwindow

    def press(self):
        self.window.finish()

main = Mainwindow()




'''
def api():
    try:
        with open("key.key", 'r') as key:
            return "&appid="+key.read()
    except IOError:
        # core.error("Could not open file")
        pass


def main():
    location = "q=Isle%20of%20Wight%20GB"
    url = f"http://api.openweathermap.org/data/2.5/weather?{location}&appid=dd440727faee99efb0b572bc6d78e7b3{api()}"
    data = request.urlopen(url).json()
    f_data = (f"""Temperature: {(round(data['main']['temp']-273.1, 1))}\nPressure: {data['main']['pressure']}
Humidity: {data['main']['humidity']}\nWeather: {data['weather'][0]['description']}""")
    print(f_data)
    log(f_data)

def log(f_data):
    with open("log.txt", 'w') as log:
        log.write(f_data)
'''
