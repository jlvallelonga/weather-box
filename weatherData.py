import json
import requests

configFileData = {}

def getConfigFileDict():
    global configFileData 
    """
    Attempts to cache the config file, and will fetch it if its not cached.
    """
    if (not configFileData):
        with open("/home/pi/rpi-fun/config.json", "r") as f:
            configFileData = json.loads(f.read())
            
    return configFileData

class WeatherData(object):
    WEATHER_URL = getConfigFileDict()['weatherUrl']

    def __init__(self):
        self.desc = "ND"
        self.tempF = "ND"
        self.updateData()

    def updateData(self):
        #get weather data
        try:
            res = requests.get(self.WEATHER_URL)
            if res.status_code == 200:
                weatherObj = res.json()
                self.desc = weatherObj['currently']['summary']
                self.tempF = weatherObj['currently']['temperature']
        except requests.exceptions.connectionError as e:
            print "Couldn't connect to weather API: ({0}) {1}".format(e.errno, e.strerror)
