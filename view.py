import sys
import time
import os
import logging
import threading
from PyQt5 import QtWidgets
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import pyqtSlot, pyqtSignal, QSize, Qt
from QNotifications import QNotificationArea

class MainWindow(QWidget):
    notifySignal = QtCore.pyqtSignal(str,str,int,bool)
    MARGIN = 20

    def __init__(self):
        super().__init__()
        imagePath = 'imgs/zoom.png'
        self.layout = QtWidgets.QVBoxLayout()
        self.image = QPixmap(self.res_path(imagePath))
        self.image = self.image.scaled(self.image.width() - self.MARGIN, self.image.height() - self.MARGIN, QtCore.Qt.KeepAspectRatio)
        self.label = QtWidgets.QLabel()
        self.label.setScaledContents(True)
        self.label.setPixmap(self.image)
        self.layout.addWidget(self.label)
        self.qna = QNotificationArea(self)
        self.qna.setEntryEffect('fadeIn', 500)
        self.qna.setExitEffect('fadeOut', 500)
        self.notifySignal.connect(self.qna.display)
        self.setLayout(self.layout)
        os.environ['QT_MAC_WANTS_LAYER'] = '1'
    
    def notify(self, text, time):
        self.notifySignal.emit(text,"danger",time*1000, False)
    
    def res_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """
        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)

def notificationsThread(mainWindow, *args, **kwargs):
    while True:
        mainWindow.notify('Help is on the way', 2)
        time.sleep(5)

def window():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.showMaximized()
    t = threading.Thread(target=notificationsThread, args=(mainWindow,))
    t.start()
    os._exit(app.exec_())

if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger().setLevel(logging.INFO)
    window()