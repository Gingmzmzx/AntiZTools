import os
import copy
from azt.utils.config import Config
from azt.utils import path
from azt.utils.crypt import DESCrypt

def p(*args, **kwargs):
    print("AntiZTools:", *args, **kwargs)

path.makeSurePathExists("")


from azt.resources import res_list
tmp: dict = copy.deepcopy(res_list.res_list)
for k, v in res_list.res_list.items():
    if os.path.exists(path.path(v)):
        tmp.pop(k)

if tmp:
    from azt.resources import res_data
    for k, v in tmp.items():
        p(f"{v} not exists, creating...")
        with open(path.path(v), "wb") as f:
            f.write(getattr(res_data, k))


p("Reading config...")
config = Config()
config.update()

key: str = config.get("Config.DESKey")
p("DES Key:", key)
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
