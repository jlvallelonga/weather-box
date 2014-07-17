try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

class InternetTime:

    #returns the time in MST 24 hour format
    TIME_URL = "http://www.timeapi.org/mdt/now?\H:\M"
    
    @staticmethod
    def getTime():
        timeData = urlopen(InternetTime.TIME_URL).read()
        timeArr = str.split(timeData, ":")
        if (RepresentsInt(timeArr[0])):
            hour = int(timeArr[0])
            isAM = True
            if hour >= 12:
                isAM = False
            amPm = "a" if isAM else "p"
            hour = hour % 12
            hour = 12 if hour == 0 else hour
            currTime = str(hour) + ":" + timeArr[1] + amPm
            return currTime
        else:
            return ""
