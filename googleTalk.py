import logging
import json
import xmpp
import commandEngine
import lcdDataFileUtils
import os

thisDir = os.path.dirname(os.path.realpath(__file__))
configFile = thisDir + "/config.json"
dataFile = thisDir + "/data.txt"

logging.basicConfig(level=logging.DEBUG, filename="errors.txt")

def getConfigFileDict():
    f = open(configFile, "r")
    fileData = f.read()
    f.close()
    return json.loads(fileData)

def message_handler(connect_object, message_node):
    msgText = str(message_node.getBody())
    if (msgText != 'None'):
        ce = commandEngine.CommandEngine(dataFile)
        message = ce.runCommand(msgText)
        connect_object.send(xmpp.Message(message_node.getFrom(), message))

try:
    config = getConfigFileDict()
    jid = xmpp.JID(config['user'])
    connection = xmpp.Client(config['server'],debug=[])
    connection.connect()
    result = connection.auth(jid.getNode(), config['password'], "LFY-client")
    connection.RegisterHandler('message', message_handler)
    connection.sendInitPresence()
    while connection.Process(1):
        pass
except:
    logging.exception("ERROR: ")
