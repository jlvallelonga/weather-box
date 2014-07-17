class LCDDataFileUtils:

    def __init__(self, dataFilePath):
        self.dataFilePath = dataFilePath

    def getNumOfMessages(self):
        linesArr = self.getLinesArray()
        return len(linesArr)

    def getMessage(self, msgNum):
        message = "message #" + str(msgNum) + " does not exist"
        linesArr = self.getLinesArray()
        if ((msgNum != 0) and (len(linesArr) >= msgNum)):
            message = linesArr[msgNum - 1]
        return message

    def getShowCommandMessage(self):
        linesArr = self.getLinesArray()
        message = ""
        for index,value in enumerate(linesArr):
            currLineArr = str.split(value, " ")
            if ((len(currLineArr) >= 1) and (currLineArr[0].lower() == "show")):
                if (len(currLineArr) == 2):
                    msgNumToShow = currLineArr[1]
                    if (msgNumToShow.isdigit()):
                        message = self.getMessage(int(msgNumToShow))
                linesArr[index] = ""
        self.writeArrayToDataFile(linesArr)
        return message

    def getLoopCommandMessage(self):
        linesArr = self.getLinesArray()
        message = ""
        for index,value in enumerate(linesArr):
            currLineArr = str.split(value, " ")
            if ((len(currLineArr) >= 1) and (currLineArr[0].lower() == "loop")):
                if (len(currLineArr) == 2):
                    msgNumToShow = currLineArr[1]
                    if (msgNumToShow.isdigit()):
                        message = self.getMessage(int(msgNumToShow))
                linesArr[index] = ""
        self.writeArrayToDataFile(linesArr)
        return message

    def isStopLoopCommandPresent(self):
        stopLoop = False
        linesArr = self.getLinesArray()
        for index,value in enumerate(linesArr):
            if (linesArr[index].lower() == "stoploop"):
                stopLoop = True
                linesArr[index] = ""
        self.writeArrayToDataFile(linesArr)
        return stopLoop

    def removeMessage(self, msgNum): 
        returnMessage = ""
        #clear the line in the array and write everything but that line to the file
        linesArr = self.getLinesArray()
        if ((msgNum != 0) and (len(linesArr) >= msgNum)):
            linesArr[msgNum - 1] = "" #clear referenced line
            self.writeArrayToDataFile(linesArr)
            returnMessage = "message #" + str(msgNum) + " has been removed"
        else:
            returnMessage = "remove command error: invalid message number"
        return returnMessage

    def getLinesArray(self):
        fileData = self.getDataFileContent()
        linesArr = str.split(fileData, "\n")
        linesArr = filter(bool, linesArr)
        return linesArr

    def writeArrayToDataFile(self, linesArr):
        f = open(self.dataFilePath, "w")
        for line in linesArr:
            if (line != ""): #don't write the empty lines that you cleared above
                f.write(line + "\n")
        f.close()

    def getDataFileContent(self):
        f = open(self.dataFilePath, "r")
        fileData = f.read()
        f.close()
        return fileData

    def clearAllMessages(self):
        f = open(self.dataFilePath, "w")
        f.write("")
        f.close()
        return "all messages have been cleared"

    def writeCommand(self, command):
        f = open(self.dataFilePath, "a")
        f.write(command + "\n")
        f.close()
