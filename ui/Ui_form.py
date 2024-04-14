# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'e:\HackTools\ui\form.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(375, 319)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        Form.setFont(font)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 376, 320))
        self.tabWidget.setAcceptDrops(False)
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabsClosable(False)
        self.tabWidget.setTabBarAutoHide(False)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_run = QtWidgets.QWidget()
        self.tab_run.setObjectName("tab_run")
        self.runBox = QtWidgets.QGroupBox(self.tab_run)
        self.runBox.setGeometry(QtCore.QRect(10, 10, 351, 90))
        self.runBox.setObjectName("runBox")
        self.EnableTUN = QtWidgets.QPushButton(self.runBox)
        self.EnableTUN.setGeometry(QtCore.QRect(160, 30, 71, 23))
        self.EnableTUN.setObjectName("EnableTUN")
        self.TUNStatusLabel = QtWidgets.QLabel(self.runBox)
        self.TUNStatusLabel.setGeometry(QtCore.QRect(20, 30, 54, 12))
        self.TUNStatusLabel.setObjectName("TUNStatusLabel")
        self.TUNStatus = QtWidgets.QLabel(self.runBox)
        self.TUNStatus.setGeometry(QtCore.QRect(80, 30, 54, 12))
        self.TUNStatus.setObjectName("TUNStatus")
        self.DisableTUN = QtWidgets.QPushButton(self.runBox)
        self.DisableTUN.setGeometry(QtCore.QRect(240, 30, 71, 23))
        self.DisableTUN.setObjectName("DisableTUN")
        self.TUNAutoStartCheckbox = QtWidgets.QCheckBox(self.runBox)
        self.TUNAutoStartCheckbox.setGeometry(QtCore.QRect(20, 60, 301, 16))
        self.TUNAutoStartCheckbox.setChecked(True)
        self.TUNAutoStartCheckbox.setObjectName("TUNAutoStartCheckbox")
        self.testBox = QtWidgets.QGroupBox(self.tab_run)
        self.testBox.setGeometry(QtCore.QRect(10, 210, 350, 70))
        self.testBox.setObjectName("testBox")
        self.openTestDialogButton = QtWidgets.QPushButton(self.testBox)
        self.openTestDialogButton.setGeometry(QtCore.QRect(20, 30, 90, 23))
        self.openTestDialogButton.setObjectName("openTestDialogButton")
        self.titleBtn = QtWidgets.QPushButton(self.testBox)
        self.titleBtn.setGeometry(QtCore.QRect(120, 30, 100, 23))
        self.titleBtn.setObjectName("titleBtn")
        self.AutoStartBox = QtWidgets.QGroupBox(self.tab_run)
        self.AutoStartBox.setGeometry(QtCore.QRect(10, 110, 350, 90))
        self.AutoStartBox.setObjectName("AutoStartBox")
        self.enableAutoStart = QtWidgets.QPushButton(self.AutoStartBox)
        self.enableAutoStart.setGeometry(QtCore.QRect(160, 30, 101, 23))
        self.enableAutoStart.setObjectName("enableAutoStart")
        self.AutoStart = QtWidgets.QLabel(self.AutoStartBox)
        self.AutoStart.setGeometry(QtCore.QRect(20, 30, 54, 12))
        self.AutoStart.setObjectName("AutoStart")
        self.AutoStartLabel = QtWidgets.QLabel(self.AutoStartBox)
        self.AutoStartLabel.setGeometry(QtCore.QRect(80, 30, 54, 12))
        self.AutoStartLabel.setObjectName("AutoStartLabel")
        self.AutoStartTipLabel = QtWidgets.QLabel(self.AutoStartBox)
        self.AutoStartTipLabel.setGeometry(QtCore.QRect(20, 60, 310, 12))
        self.AutoStartTipLabel.setObjectName("AutoStartTipLabel")
        self.tabWidget.addTab(self.tab_run, "")
        self.tab_log = QtWidgets.QWidget()
        self.tab_log.setObjectName("tab_log")
        self.logTextarea = QtWidgets.QTextBrowser(self.tab_log)
        self.logTextarea.setGeometry(QtCore.QRect(10, 10, 351, 190))
        self.logTextarea.setObjectName("logTextarea")
        self.clearLogsBtn = QtWidgets.QPushButton(self.tab_log)
        self.clearLogsBtn.setGeometry(QtCore.QRect(10, 200, 75, 23))
        self.clearLogsBtn.setObjectName("clearLogsBtn")
        self.tabWidget.addTab(self.tab_log, "")
        self.tab_about = QtWidgets.QWidget()
        self.tab_about.setObjectName("tab_about")
        self.tabWidget.addTab(self.tab_about, "")

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "HackTools"))
        self.runBox.setTitle(_translate("Form", "网络相关"))
        self.EnableTUN.setText(_translate("Form", "启用TUN"))
        self.TUNStatusLabel.setText(_translate("Form", "TUN状态"))
        self.TUNStatus.setText(_translate("Form", "获取中..."))
        self.DisableTUN.setText(_translate("Form", "禁用TUN"))
        self.TUNAutoStartCheckbox.setText(_translate("Form", "开机自动检测网络状态并适时启用TUN"))
        self.testBox.setTitle(_translate("Form", "测试"))
        self.openTestDialogButton.setText(_translate("Form", "打开测试窗口"))
        self.titleBtn.setText(_translate("Form", "检测窗口标题"))
        self.AutoStartBox.setTitle(_translate("Form", "开机自启"))
        self.enableAutoStart.setText(_translate("Form", "启用开机自启"))
        self.AutoStart.setText(_translate("Form", "开机自启"))
        self.AutoStartLabel.setText(_translate("Form", "获取中..."))
        self.AutoStartTipLabel.setText(_translate("Form", "请提前在配置文件中修改exe路径"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_run), _translate("Form", "面板"))
        self.logTextarea.setPlaceholderText(_translate("Form", "暂无..."))
        self.clearLogsBtn.setText(_translate("Form", "清空日志"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_log), _translate("Form", "日志"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_about), _translate("Form", "关于"))