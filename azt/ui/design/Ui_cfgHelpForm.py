# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\Projects\AntiZTools\azt\ui\design\cfgHelpForm.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_cfgHelpForm(object):
    def setupUi(self, cfgHelpForm):
        cfgHelpForm.setObjectName("cfgHelpForm")
        cfgHelpForm.resize(514, 383)
        self.textBrowser = QtWidgets.QTextBrowser(cfgHelpForm)
        self.textBrowser.setGeometry(QtCore.QRect(0, -1, 514, 385))
        self.textBrowser.setObjectName("textBrowser")

        self.retranslateUi(cfgHelpForm)
        QtCore.QMetaObject.connectSlotsByName(cfgHelpForm)

    def retranslateUi(self, cfgHelpForm):
        _translate = QtCore.QCoreApplication.translate
        cfgHelpForm.setWindowTitle(_translate("cfgHelpForm", "配置指南"))