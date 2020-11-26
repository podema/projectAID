import view, model
import logging
import sys
import os
from PyQt5.QtWidgets import QApplication
import re
import logging
import threading
import time

parsers = [
    ".*I need help with ([^\s]*).*",
    ".*I have a problem with ([^\s]*).*",
    ".*I have an issue with ([^\s]*).*",
    ".*I need help.*",
    ".*I don't understand.*",
    ".*I'm stuck.*",
    ".*I don't get.*",
    ".*I didn't get.*",
    ".*I can't get.*",
    ".*It makes no sense.*",
    ".*It doesn't make sense.*",
    ".*I don't follow.*",
    ".*I can't follow.*",
    ".*I'm lost.*",
    ".*I am lost.*",
    ".*I'm confused.*",
    ".*I can't understand.*",
    ".*I think we are not understanding.*",
    ".*I think we're not understanding.*"
]
changeImageRunning = False

def speechAnalyze(mainWindow, speech):
    global parsers
    global changeImageRunning
    logging.info(f"speech detected : {speech}")
    for expr in parsers:
        match = expr.match(speech)
        if match:
            try:
                notificationText = f"You need help with {match.group(1)}, a teacher is coming!"
            except:
                notificationText = "It seems that you are stuck, check out this resource: https://miro.com/app/board/o9J_kiTrGzQ=/"
                
            logging.info(f"notification sent : {notificationText}")
            #mainWindow.notify(notificationText, 3)
            if changeImageRunning == False:
                changeImage()
                changeImageRunning = True
            return
    
def compileRegexs():
    global parsers
    _parsers = []
    for parser in parsers:
        _parsers.append(re.compile(parser))
    parsers = _parsers

def changeImage():
    threading.Thread(target=_changeImage).start()

def _changeImage():
    global changeImageRunning
    for i in [1,2,3,0]:
        mainWindow.changeImage(f'imgs/image{i}.png')
        if (i == 2 or i == 1):
            time.sleep(1)
        elif i == 3:
            time.sleep(5)
    changeImageRunning = False

def test(mainWindow):
    while True:
        speechAnalyze(mainWindow, "I need help")
        time.sleep(5)

if __name__ == '__main__':
    compileRegexs()
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    app = QApplication(sys.argv)
    mainWindow = view.MainWindow('imgs/image0.png')
    mainWindow.showMaximized()
    speechThread = model.Model()
    speechThread.addSpeechHandler(lambda x: speechAnalyze(mainWindow, x))
    speechThread.start()
    #To test without speaking alone like a dumbass
    #threading.Thread(target=lambda: test(mainWindow)).start()
    os._exit(app.exec_())
