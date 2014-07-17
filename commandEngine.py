import lcdDataFileUtils

class CommandEngine:

    def __init__(self, dataFilePath):
        self.dataFileUtils = lcdDataFileUtils.LCDDataFileUtils(dataFilePath)

    def getHelpContents(self):
        helpContents = "Commands:\n"
        helpContents = "queue rm clearall show loop stoploop\n"
        return helpContents

    def runCommand(self, command):
        returnMessage = "" #what will be sent back to the user
        commandName = self.getCommandNameFromCommand(command).lower()
        if (commandName == "queue"):
            returnMessage = self.runQueueCommand(command)
        elif (commandName == "rm"):
            returnMessage = self.runRemoveCommand(command)
        elif (commandName == "clearall"):
            returnMessage = self.runClearAllCommand(command)
        elif (commandName == "show"):
            returnMessage = self.runShowCommand(command)
        elif (commandName == "loop"):
            returnMessage = self.runLoopCommand(command)
        elif (commandName == "looplast"):
            returnMessage = self.runLoopLastCommand(command)
        elif (commandName == "stoploop"):
            returnMessage = self.runStopLoopCommand(command)
        elif (commandName == "help"):
            returnMessage = self.getHelpContents()
        else:
            returnMessage = self.runQueueCommand(command)
        return returnMessage

    def getCommandNameFromCommand(self, command):
        commandArr = str.split(command, " ")
        commandName = ""
        if (len(commandArr) >= 1):
            commandName = commandArr[0]
        return commandName

    def runQueueCommand(self, command):
        self.dataFileUtils.writeCommand(command)
        return "message has been queued"

    def runStopLoopCommand(self, command):
        self.dataFileUtils.writeCommand(command)
        return "loop will be stopped now"
        
    def runRemoveCommand(self, command):
        commandArr = str.split(command, " ")
        returnMessage = ""
        if (len(commandArr) == 2):
            msgToRemove = int(commandArr[1])
            returnMessage = self.dataFileUtils.removeMessage(msgToRemove)
        else:
            returnMessage = "remove command error: wrong number of arguments"
        return returnMessage

    def runClearAllCommand(self, command):
        return self.dataFileUtils.clearAllMessages()

    def runShowCommand(self, command):
        commandArr = str.split(command, " ")
        returnMessage = ""
        if (len(commandArr) == 2):
            msgToShow = commandArr[1]
            if (msgToShow.isdigit()):
                self.dataFileUtils.writeCommand(command)
                returnMessage = "message will be displayed once now"
            else:
                returnMessage = "show command error: argument must be numeric"
        else:
            returnMessage = "show command error: wrong number of arguments"
        return returnMessage

    def runLoopLastCommand(self, command):
        lastMessageNum = self.dataFileUtils.getNumOfMessages()
        command = "loop " + str(lastMessageNum)
        self.dataFileUtils.writeCommand(command)
        return "last message will be looped"

    def runLoopCommand(self, command):
        commandArr = str.split(command, " ")
        returnMessage = ""
        if (len(commandArr) == 2):
            msgToShow = commandArr[1]
            if (msgToShow.isdigit()):
                self.dataFileUtils.writeCommand(command)
                returnMessage = "message will be displayed repeatedly now"
            else:
                returnMessage = "loop command error: argument must be numeric"
        else:
            returnMessage = "loop command error: wrong number of arguments"
        return returnMessage
