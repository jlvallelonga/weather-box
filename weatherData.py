import sys
import json
try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

def getConfigFileDict():
    f = open("/home/pi/rpi-fun/config.json", "r")
    fileData = f.read()
    f.close()
    return json.loads(fileData)

class WeatherData:

    WEATHER_URL = getConfigFileDict()['weatherUrl']

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
