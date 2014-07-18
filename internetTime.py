import requests
import arrow

def getTime():
    """
    Returns a string in the format of Hour(12):Minutes am/pm
    """
    res = requests.get("http://timeapi.org/utc/now")
    if res.status_code == 200:
        time = arrow.get(res.content)
        return time.to("US/Mountain").format("h:mm")
    else:
        return ""

class InternetTime:
    @staticmethod
    def getTime():
        """
        Return getTime() from above, this exists as just a
        backwards compatability thing for now.
        """
        return getTime()
