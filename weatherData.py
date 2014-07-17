import sys
import json
try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

class WeatherData:

    WEATHER_URL = "https://api.forecast.io/forecast/59ae0eaf99cb6d6f3549b8a75ef343e3/40.008370,-105.267114"

    def __init__(self):
        self.desc = "ND"
        self.tempF = "ND"
        self.updateData()

    def updateData(self):
        #get weather data
        try:
            allWeatherData = urlopen(self.WEATHER_URL).read()
            weatherObj = json.loads(allWeatherData)
            self.desc = weatherObj['currently']['summary']
            self.tempF = weatherObj['currently']['temperature']
        except IOError as e:
            print "IOError: ({0}) {1}".format(e.errno, e.strerror)
        except:
            raise
