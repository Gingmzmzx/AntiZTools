from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, Qt
from PyQt5.QtGui import QIcon

from .. import path
from ..utils.aow import Aow1, Aow2, Aow3
from .design.Ui_aowForm import Ui_aowForm

class AowForm(QMainWindow, Ui_aowForm):
    scriptThreadStatus = False

    def __init__(self, width, height, parent=None):
        super(AowForm, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowIcon(QIcon(path.path("icon.jpg")))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.move(
            width - self.width() - 10,
            height - self.height() - 50
        )
        self.screenWidth = width
        self.screenHeight = height
        self.stopBtn.clicked.connect(self.stop)
        self.stopBtn.setDisabled(True)
        self.aow1Btn.clicked.connect(self.runScript(Aow1))
        self.aow2Btn.clicked.connect(self.runScript(Aow2))
        self.aow3Btn.clicked.connect(self.runScript(Aow3))
    
    def runScript(self, script):
        def _runScript():
            if not self.scriptThreadStatus:
                self.aow1Btn.setDisabled(True)
                self.aow2Btn.setDisabled(True)
                self.aow3Btn.setDisabled(True)
                self.stopBtn.setDisabled(False)
                self.scriptThread = script(self.screenWidth, self.screenHeight)
                self.scriptThread.start()
                self.scriptThreadStatus = True
        return _runScript

    def stop(self):
        self.scriptThread.forceStop()
        self.scriptThread.quit()
        self.scriptThread.wait()
        self.scriptThreadStatus = False
        self.aow1Btn.setDisabled(False)
        self.aow2Btn.setDisabled(False)
        self.aow3Btn.setDisabled(False)
        self.stopBtn.setDisabled(True)

