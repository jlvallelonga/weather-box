import logging
import sys
import datetime
import time
import lcdCommands as lcd
import weatherData
import lcdDataFileUtils
import os

thisDir = os.path.dirname(os.path.realpath(__file__))
configFile = thisDir + "/config.json"
dataFile = thisDir + "/data.txt"

numMessages = 0
currTime = ""
wd = ""
date = ""
updateIteration = 0

def readDataFile():
    f = open(dataFile, 'r')
    firstLine = f.readline().strip()
    secondLine = f.readline().strip()
    return firstLine

def getTime():
    now = datetime.datetime.now()
    hour = int(now.strftime("%I"))
    period = now.strftime("%p").lower()
    timeStr = str(hour) + now.strftime(":%M") + period
    return timeStr

def getDate():
    now = datetime.datetime.now()
    dateStr = str(now.month) + "/" + str(now.day)
    return dateStr

logging.basicConfig(level=logging.DEBUG, filename="errors.txt")
try:
    myLCD = lcd.LCDDisplay()
    dataFileUtils = lcdDataFileUtils.LCDDataFileUtils(dataFile)
    while 1:
        #try:
        if myLCD.isConnected():
            updateScreen = False
            # get time every 3 seconds
            updateScreen = True
            nowTime = getTime()
            if (nowTime != ""):
                currTime = nowTime
            date = getDate()
            # get weather data every 90 seconds (960 times a day)
            if (updateIteration % 90 == 0):
                updateScreen = True
                wd = weatherData.WeatherData()
            # if there's a loop command the loop the referenced message
            loopMessage = dataFileUtils.getLoopCommandMessage()
            if (loopMessage != ""):
                stopLoop = False
                while(not(stopLoop)):
                    myLCD.clearScreen()
                    myLCD.scrollTextLeftOnLine(loopMessage, 1, 0.2)
                    stopLoop = dataFileUtils.isStopLoopCommandPresent()
            # if there's a show command the show the referenced message
            showMessage = dataFileUtils.getShowCommandMessage()
            if (showMessage != ""):
                myLCD.clearScreen()
                myLCD.scrollTextLeftOnLine(showMessage, 1, 0.2)
            # get and show number of messages between time and date
            num = dataFileUtils.getNumOfMessages()
            if (num != numMessages):
                updateScreen = True
                numMessages = num
            # only update the screen if there is data to update
            if (updateScreen):
                myLCD.clearScreen()
                if (numMessages > 0):
                    myLCD.displayWordAtPos(str(numMessages), 8)
                myLCD.displayWordOnLine(currTime , 1)
                myLCD.rightJustifyTextOnLine(date, 1)
                myLCD.rightJustifyTextOnLine(wd.desc, 2)
                myLCD.displayWordOnLine(str(int(round(wd.tempF))) + chr(223), 2)
            updateIteration = updateIteration + 1
            time.sleep(1)
        else:
            print "establishing connection..."
            myLCD.getSerialConnection()
            time.sleep(10)
        #except:
        #    print "Error writing to bluetooth"
        #    myLCD.disconnect()
except:
    logging.exception("ERROR: ")
