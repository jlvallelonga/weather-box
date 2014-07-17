import sys
import lcdCommands as lcd

try:
    myLCD = lcd.LCDDisplay()
    myLCD.resetLCD()
except:
    raise
    #logging.exception("ERROR: ")
