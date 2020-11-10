import view, model
import logging
import sys
import os
from PyQt5.QtWidgets import QApplication
import re
import logging

parsers = [
    re.compile(".*I need help with ([^\s]*).*"),
    re.compile(".*I have a problem with ([^\s]*).*"),
    re.compile(".*I have an issue with ([^\s]*).*"),
    re.compile(".*I need help.*"),
    re.compile(".*I don't understand.*"),
    re.compile(".*I'm stuck.*"),
    re.compile(".*I don't get.*"),
    re.compile(".*I didn't get.*"),
    re.compile(".*I can't get.*"),
    re.compile(".*It makes no sense.*"),
    re.compile(".*It doesn't make sense.*"),
    re.compile(".*I don't follow.*"),
    re.compile(".*I can't follow.*"),
    re.compile(".*I'm lost.*"),
    re.compile(".*I'm confused.*"),
    re.compile(".*I can't understand.*")
]

def speechAnalyze(mainWindow, speech):
    logging.info(f"speech detected : {speech}")
    for expr in parsers:
        match = expr.match(speech)
        if match:
            try:
                notificationText = f"You need help with {match.group(1)}, a teacher is coming!"
            except:
                notificationText = "It seems that you are stuck, check out this resource: https://miro.com/app/board/o9J_kiTrGzQ=/"
                
            logging.info(f"notification sent : {notificationText}")
            mainWindow.notify(notificationText, 3)
            return

if __name__ == '__main__':
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    app = QApplication(sys.argv)
    mainWindow = view.MainWindow()
    mainWindow.showMaximized()
    speechThread = model.Model()
    speechThread.addSpeechHandler(lambda x: speechAnalyze(mainWindow, x))
    speechThread.start()
    
    os._exit(app.exec_())
