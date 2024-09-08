import os
from azt.utils.config import Config
from azt.utils import path
from azt.utils.crypt import DESCrypt

path.makeSurePathExists("")

if not os.path.exists(path.path("icon.jpg")):
    from azt.resources import data
    with open(path.path("icon.jpg"), "wb") as f:
        f.write(data.icon)

if not os.path.exists(path.path("icon_colored.png")):
    from azt.resources import data
    with open(path.path("icon_colored.png"), "wb") as f:
        f.write(data.icon_colored)

config = Config()
config.update()

key: str = config.get("Config.DESKey")
desCrypt = DESCrypt(key)

import sys
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
# import qt_material

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
app = QApplication(sys.argv)
# setup stylesheet
# qt_material.apply_stylesheet(app, theme='dark_teal.xml')
if config.get("Fonts.Enable"):
    QApplication.setFont(QFont(config.get("Fonts.FontFamily"), int(config.get("Fonts.FontPointSize"))))
QApplication.setQuitOnLastWindowClosed(False)
