import logging
import json
import xmpp
import commandEngine
import lcdDataFileUtils

logging.basicConfig(level=logging.DEBUG, filename="errors.txt")

def getConfigFileDict():
    f = open("/home/pi/rpi-fun/config.json", "r")
    fileData = f.read()
    f.close()
    return json.loads(fileData)

def message_handler(connect_object, message_node):
    msgText = str(message_node.getBody())
    if (msgText != 'None'):
        ce = commandEngine.CommandEngine("/home/pi/rpi-fun/data.txt")
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
