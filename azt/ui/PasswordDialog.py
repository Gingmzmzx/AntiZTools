from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore, Qt
from PyQt5.QtGui import QIcon
from .. import config
from ..utils import path
from .design.Ui_password import Ui_PasswordDialog

class PasswordDialog(QDialog, Ui_PasswordDialog):
    def __init__(self, func, parent=None):
        super(PasswordDialog, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.func = func
        self.label_2.setVisible(False)
        self.passwordInput.setEchoMode(Qt.QLineEdit.Password)
        self.confirmBtn.clicked.connect(self.check)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(path.path("icon.jpg")))
    
    def check(self):
        if self.passwordInput.text() == config.get("Config.Password"):
            self.func()
            self.close()
        else:
            self.label_2.setVisible(True)


