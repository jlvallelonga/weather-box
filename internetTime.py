import requests
import arrow

def getTime():
  res = requests.get('http://timeapi.org/utc/now")
  if res.status_code == 200:
    time = arrow.get(res.content)
    return time.to("US/Mountain").format("hh:mm a")
  else
    return ""

class InternetTime:
    @staticmethod
    def getTime():
        return getTime()
