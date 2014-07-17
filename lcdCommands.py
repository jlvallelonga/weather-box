import time
import serial
import bluetooth

class LCDDisplay:

    def __init__(self):
        self.ser = None
        self.getSerialConnection()

    def isConnected(self):
        return self.ser is not None

    def disconnect(self):
        if (self.ser is not None):
            self.ser.close()
        self.ser = None

    def getSerialConnection(self):
        try:
            self.disconnect()
            self.ser = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            self.ser.connect(('00:06:66:05:61:2E', 1))
            print "connected!"
            self.resetLCD()
        except:
            self.ser = None
            print "Could not connect"

    def sendData(self, data):
        self.ser.send(data)

    def sendCommand(self):
        self.sendData(chr(0xFE))

    def clearScreen(self):
        self.sendCommand()
        self.sendData(chr(0x01))

    def goToLine(self, lineNumber):
        self.sendCommand()
        if lineNumber == 1:
            self.sendData(chr(128))
        elif lineNumber == 2:
            self.sendData(chr(192))
        else:
            print "Line not available: " + str(lineNumber)
            self.goToLine(1)

    def goToPos(self, pos):
        self.sendCommand()
        if pos < 16:
            self.sendData(chr(pos + 128))
        elif pos < 32:
            self.sendData(chr(pos + 128 + 48))
        else:
            self.goToPos(0)

    def displayWordOnLine(self, word, line):
        self.goToLine(line)
        self.sendData(word)

    def displayWordAtPos(self, word, pos):
        self.goToPos(pos)
        self.sendData(word)

    def rightJustifyTextOnLine(self, text, line):
        startPos = (line - 1) * 16 + (16 - len(text))
        self.displayWordAtPos(text, startPos)

    def scrollTextLeftOnLine(self, text, line, pause):
        spacePadding = "                " #to add to the beginning and end of the text
        newText = spacePadding + text + spacePadding
        for currTextPos in range(len(newText) - 16):
            self.clearScreen()
            self.displayWordOnLine(newText[currTextPos:currTextPos + 16], line)
            time.sleep(pause)

    def slideLetters(self, word, endPause):
        for currCharPos in range(len(word)):
            for lcdPos in range(15, currCharPos - 1, -1):
                if word[currCharPos] != " ":
                    self.goToPos(lcdPos)
                    self.sendData(word[currCharPos])
                    for i in range(currCharPos):
                        self.goToPos(i)
                        self.sendData(word[i])
                    time.sleep(0.07)
                    if currCharPos != len(word) - 1 or lcdPos != currCharPos:
                        self.clearScreen()
                    else:
                        time.sleep(endPause)

    #Be sure to cycle the power after you do this. it seems to freeze up the screen.
    def resetLCD(self):
        self.sendData(chr(0x7C))
        self.sendData(chr(0x04))
        self.sendData(chr(0x7C))
        self.sendData(chr(0x06))
