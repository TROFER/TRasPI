import requests
import pysnooper

def api():
    try:
        with open("key.key", 'r') as key:
            return "&appid="+key.read()
    except IOError:
        # core.error("Could not open file")
        pass


def main():
    location = "q=Isle of Wight, GB"
    url = f"http://api.openweathermap.org/data/2.5/weather?{location}&appid=dd440727faee99efb0b572bc6d78e7b3{api()}"
    data = requests.get(url).json()
    f_data = (f"""Temperature: {(round(data['main']['temp']-273.1, 1))}\nPressure: {data['main']['pressure']}
Humidity: {data['main']['humidity']}\nWeather: {data['weather'][0]['description']}""")
    print(f_data)
    log(f_data)

@pysnooper.snoop()
def log(f_data):
    with open("log.txt", 'w') as log:
        log.write(f_data)



main()
