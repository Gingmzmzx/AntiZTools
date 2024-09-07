import random

from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore, Qt
from PyQt5.QtGui import QIcon

from ..utils import path
from .design.Ui_ZBDialog import Ui_ZBDialog

class ZBDialog(QDialog, Ui_ZBDialog):
    def __init__(self, labelText, parent=None):
        super(ZBDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(path.path("icon.jpg")))
        self.label.setText(labelText)

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.label.setStyleSheet(f"color: rgb({r}, {g}, {b})")

        self.adjustSize()
        self.setFixedSize(self.width(), self.height())
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.activateWindow()
        self.setFocus()


