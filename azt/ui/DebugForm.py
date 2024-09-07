from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, Qt
from PyQt5.QtGui import QIcon

from .. import path
from .design.Ui_debugForm import Ui_debugForm

class DebugForm(QMainWindow, Ui_debugForm):
    def __init__(self, title, width, height, parent=None):
        super(DebugForm, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowIcon(QIcon(path.path("icon.jpg")))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(title)
        self.move(
            width - self.width() - 10,
            height - self.height() - 50
        )

    def setTitleText(self, text):
        self.titletext.setText(text)
