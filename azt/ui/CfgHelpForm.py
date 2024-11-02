from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, Qt
from PyQt5.QtGui import QIcon

from .. import path
from .design.Ui_cfgHelpForm import Ui_cfgHelpForm

class CfgHelpForm(QMainWindow, Ui_cfgHelpForm):
    def __init__(self, parent=None):
        super(CfgHelpForm, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowIcon(QIcon(path.path("icon.jpg")))

        with open(path.path("cfgHelp.html"), "r", encoding="utf-8") as f:
            file_content = f.read()

        self.textBrowser.setText(file_content)

