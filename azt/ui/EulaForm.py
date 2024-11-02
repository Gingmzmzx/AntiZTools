import sys
import os
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtCore, Qt
from PyQt5.QtGui import QIcon

from .. import path, main
from .design.Ui_eulaForm import Ui_eulaForm

class EulaForm(QMainWindow, Ui_eulaForm):
    def __init__(self, parent=None):
        super(EulaForm, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowIcon(QIcon(path.path("icon.jpg")))

        self.normalClose = False

        with open(path.path("eula.html"), "r", encoding="utf-8") as f:
            file_content = f.read()

        self.textBrowser.setText(file_content)
        self.exitBtn.clicked.connect(self.closeEvent)
        self.agreeBtn.clicked.connect(self.agree)

    def closeEvent(self, event):
        if self.normalClose:
            event.accept()
            return
        os.remove(path.path("eula.html"))
        sys.exit(0)

    def agree(self):
        self.normalClose = True
        self.close()
        main.run()
