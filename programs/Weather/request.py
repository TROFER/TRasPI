import core
import json
import urllib.request
from datetime import datetime
from time import strftime

class CurrentData:

    URL = 'http://api.openweathermap.org/data/2.5/weather?'

    def __init__(self, location):
        self.data = self.request(location)

    def description(self):
        return f"{self.data['weather'][0]['description'].capitalize()}"
    
    def icon(self):
        return f"{self.data['weather'][0]['icon']}"

    def temperature(self):
        return f"{self.data['main']['temp']}°C"

    def feelsLike(self):
        return f"Feels Like: {self.data['main']['feels_like']}*C"

    def temperatureMin(self):
        return f"Min Temp: {self.data['main']['temp_min']}*C"

    def temperatureMax(self):
        return f"Max Temp: {self.data['main']['temp_max']}*C"
    
    def temperatureEnv(self):
        return "Not Yet Implemented"

    def pressure(self):
        return f"Pressure: {self.data['main']['pressure']} hPa"

    def humidity(self):
        return f"Humidity: {self.data['main']['humidity']}%"

    def visibility(self):
        return f"Visibility: {self.data['visibility']}M"

    def windSpeed(self):
        return f"Wind Speed: {self.data['wind']['speed']}M/s"

    def windDeg(self):
        return f"Direction: {self.data['wind']['deg']} Deg"

    def windGust(self):
        return f"Gust Speed: {self.data['wind']['gust']}M/s"

    def sunrise(self):
        return f"Sunrise: {datetime.utcfromtimestamp(self.data['sys']['sunrise']).strftime('%-I:%M %p')}"

    def sunset(self):
        return f"Sunset: {datetime.utcfromtimestamp(self.data['sys']['sunset']).strftime('%-I:%M %p')}"

    def request(self, location: str):
        with open(f'{core.sys.const.path}user/openweatherkey.txt') as key:
            key = key.read()
        return json.load(urllib.request.urlopen(f'{self.URL}q={location}&units=metric&appid={key}'))
