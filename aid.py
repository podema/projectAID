import view, model
import logging
import sys
import os
from PyQt5.QtWidgets import QApplication
import re
import logging

parsers = [
    re.compile(".*I need help with ([^\s]*).*"),
    re.compile(".*I need help.*"),
    re.compile(".*I don'understand this.*"),
    re.compile(".*I'm stooked.*")
]

def speechAnalyze(mainWindow, speech):
    logging.info(f"speech detected : {speech}")
    for expr in parsers:
        match = expr.match(speech)
        if match:
            try:
                notificationText = f"You need help with {match.group(1)}, a teacher is coming"
            except:
                notificationText = "Help is on the way!"
                
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
