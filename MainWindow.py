import requests, traceback, sys, path, random, time, json, reg, os, shutil, tempfile
from PyQt5 import QtCore
from PyQt5 import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox, QAction, QMenu, QSystemTrayIcon, QDialog, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal
from ui.Ui_form import Ui_Form
from ui.Ui_ZBDialog import Ui_ZBDialog
from ui.Ui_password import Ui_PasswordDialog
import pygetwindow as gw
# import qt_material

def checkNetwork(url="https://example.com"):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # 如果响应状态码不是200，将抛出HTTPError异常
        return False
    except Exception as e:
        print(e)
    return True

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

class PasswordDialog(QDialog, Ui_PasswordDialog):
    def __init__(self, config, func, parent=None):
        super(PasswordDialog, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.config = config
        self.func = func
        self.label_2.setVisible(False)
        self.passwordInput.setEchoMode(Qt.QLineEdit.Password)
        self.confirmBtn.clicked.connect(self.check)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon(path.path("icon.jpg")))
    
    def check(self):
        if self.passwordInput.text() == self.config.get("password", "ZBZ666"):
            self.func()
            self.close()
        else:
            self.label_2.setVisible(True)

class MyQAction(QAction):
    baseText = False
    def changeText(self, text):
        if not self.baseText: self.baseText = self.text();
        self.setText(self.baseText + text)

class MyMainWindow(QMainWindow, Ui_Form):
    getGWThreadStatus = False

    def __init__(self,parent =None):
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.qIcon = QIcon(path.path("icon.jpg"))
        self.setWindowIcon(self.qIcon)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("AntiZTools | Made for Class 6.")
    
    def _initTray(self):
        self.stOnStAction = MyQAction("开机自启：", self)
        self.winTitleAction = MyQAction("窗口标题：", self)
        self.conStatusAction = MyQAction("计算机管理：", self)
        self.openAction = QAction("打开主界面", self)
        self.exitAction = QAction("退出程序", self)
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addActions((self.stOnStAction, self.winTitleAction, self.conStatusAction))
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addActions((self.openAction, self.exitAction))
        self.openAction.triggered.connect(self.openPwdDialog(myWin.show))
        self.exitAction.triggered.connect(self.openPwdDialog(app.quit))
        self.winTitleAction.changeText("未运行")
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(self.qIcon)
        self.trayIcon.setToolTip(self.config.get("ToolTip", "GeoGebra"))
        self.trayIcon.show()
    
    def changeTrayIcon(self, icon):
        self.trayIcon.setIcon(QIcon(icon))
    
    def init(self):
        try:
            self._init()
        except Exception as e:
            print(traceback.format_exc())
            QMessageBox.warning(self, "发生错误", "运行发生错误，请将下列错误信息提交给开发者：\n{}".format(str(e)))

    def _init(self):
        with open(path.path("config.json"), "r", encoding="utf-8") as f:
            self.config = json.loads(f.read())

        self._initTray()

        self.autoStartThread = AutoStartThread(self.config)
        self.autoStartThread.trigger.connect(self.runGWThread)
        self.autoStartThread.messager.connect(self.showMessage)
        self.autoStartThread.start()
        self.clearLogsBtn.clicked.connect(self.clearLogs)
        self.titleBtn.clicked.connect(self.runGWThread)
        self.stopGetGWThread.clicked.connect(self.stopGWThread)
        self.enableAutoStart.clicked.connect(self.setAutoStart)
        self.AutoStartTipLabel.setText(path.cwdPath(self.config.get("EXEFileName", "AntiZTools.exe")))
        self.execCode.clicked.connect(self.execCodeFunc)
        self.disableController.clicked.connect(self.disableControllerFunc)
        self.enableController.clicked.connect(self.enableControllerFunc)
        self.getWindowThread = GetWindowThread(self.config.get("ZBMsg", []))
        self.getWindowThread.trigger.connect(self.openZBDialog)
        self.getWindowThread.trigger1.connect(self.stopGWThread)
        self.resetCfg()
        self.saveCfgBtn.clicked.connect(self.saveCfg)
        self.reCfgBtn.clicked.connect(self.resetCfg)

        if self.config.get("StartShow", False):
            myWin.show()
        if self.config.get("startMsg", "已在后台运行") != "":
            self.showMessage(self.config.get("startMsg", "已在后台运行"))
    
    def showMessage(self, msg, *args, **kwargs):
        try:
            self.trayIcon.showMessage(self.config.get("ToolTip", "GeoGebra"), msg, self.qIcon, *args, **kwargs)
        except Exception:
            pass

    def saveCfg(self):
        cfg_str = self.CfgTextarea.toPlainText()
        try:
            with open(path.path("config.json"), "w", encoding="utf-8") as f:
                f.write(cfg_str)
            QMessageBox.information(self, "保存成功", "保存成功！\n有些功能重启程序后生效")
        except Exception as e:
            QMessageBox.warning(self, "保存失败", "保存失败！\n{}".format(str(e)))
        self.config = json.loads(cfg_str)
        self.autoStartThread.config = self.config
        self.getWindowThread.config = self.config.get("ZBMsg", [])
    
    def resetCfg(self):
        self.CfgTextarea.setText(json.dumps(self.config, ensure_ascii=False, indent=4))
    
    def execCodeFunc(self):
        try:
            exec(self.DebugCode.toPlainText())
        except Exception as e:
            print(e)

    def openPwdDialog(self, func):
        def _openPwdDialog():
            PasswordDialog(self.config, func).exec_()
        return _openPwdDialog

    def runGWThread(self):
        if self.config.get("AntiZB", True) and self.getGWThreadStatus == False:
            self.getWindowThread.exitFlag = False
            self.getWindowThread.start()
            self.getGWThreadStatus = True
            self.changeTrayIcon(path.path("icon_colored.png"))
            self.getgwstatus.setText("正在运行")
            self.getgwstatus.setStyleSheet("color: green;")
            self.winTitleAction.changeText("正在运行")
    
    def stopGWThread(self):
        try:
            self.getWindowThread.exitFlag = True
            self.getWindowThread.quit()
            self.getGWThreadStatus = False
            self.changeTrayIcon(path.path("icon.jpg"))
            self.getgwstatus.setText("未运行")
            self.winTitleAction.changeText("未运行")
            self.getgwstatus.setStyleSheet("color: red;")
        except Exception:
            pass
    
    def enableControllerFunc(self):
        controllerStatus = reg.ControllerStatus()
        if controllerStatus.status():
            controllerStatus.enable()
        if not controllerStatus.status():
            self.controllerStatus.setText("未禁用")
            self.conStatusAction.changeText("未禁用")
            self.controllerStatus.setStyleSheet("color: green")
            self.enableController.setDisabled(True)
            self.disableController.setDisabled(False)

    def disableControllerFunc(self):
        controllerStatus = reg.ControllerStatus()
        if not controllerStatus.status():
            controllerStatus.disable()
        if controllerStatus.status():
            self.controllerStatus.setText("已禁用")
            self.conStatusAction.changeText("已禁用")
            self.controllerStatus.setStyleSheet("color: red")
            self.disableController.setDisabled(True)
            self.enableController.setDisabled(False)

    def setAutoStart(self):
        autoStarter = reg.AutoStarter(path.cwdPath(self.config.get("EXEFileName", "AntiZTools.exe")), self.config.get("RegAppName", "AntiZTools"))
        if not autoStarter.is_auto_start():
            autoStarter.set_auto_start()
        if autoStarter.is_auto_start():
            self.AutoStartLabel.setText("已启用")
            self.stOnStAction.changeText("已启用")
            self.AutoStartLabel.setStyleSheet("color: green")
            self.enableAutoStart.setDisabled(True)
    
    def openZBDialog(self, msg, w, h):
        zbDialog = ZBDialog(msg)
        zbDialog.label.adjustSize()
        zbDialog.move(random.randint(0, w - zbDialog.width()), random.randint(0, h - zbDialog.height()))
        zbDialog.exec_()

    def clearLogs(self):
        self.logTextarea.clear()
    
    def log(self, *args):
        self.logTextarea.append(" ".join(args))

class AutoStartThread(QThread):
    trigger = pyqtSignal()
    messager = pyqtSignal(str)
    emitFlag = True
    emitFlag2 = True

    def __init__(self, config):
        super(AutoStartThread, self).__init__()
        self.config = config

    def __del__(self):
        self.wait()

    def run(self):
        self.emitFlag = True
        self.emitFlag2 = True

        autoStarter = reg.AutoStarter(path.cwdPath(self.config.get("EXEFileName", "AntiZTools.exe")), self.config.get("RegAppName", "AntiZTools"))
        if autoStarter.is_auto_start():
            myWin.AutoStartLabel.setText("已启用")
            myWin.AutoStartLabel.setStyleSheet("color: green")
            myWin.enableAutoStart.setDisabled(True)
            myWin.stOnStAction.changeText("已启用")
        else:
            myWin.AutoStartLabel.setText("未启用")
            myWin.AutoStartLabel.setStyleSheet("color: red")
            myWin.stOnStAction.changeText("未启用")
        
        controllerStatus = reg.ControllerStatus()
        if controllerStatus.status():
            myWin.controllerStatus.setText("已禁用")
            myWin.controllerStatus.setStyleSheet("color: red")
            myWin.disableController.setDisabled(True)
            myWin.conStatusAction.changeText("已禁用")
        else:
            myWin.controllerStatus.setText("未禁用")
            myWin.controllerStatus.setStyleSheet("color: green")
            myWin.enableController.setDisabled(True)
            myWin.conStatusAction.changeText("未禁用")
        
        print("getStatus...")
        if checkNetwork(url=self.config.get("checkUrl", "https://example.com")):
            self.trigger.emit()
        
        temp_dir = tempfile.gettempdir()
        failedtimes, successtimes, cleantipstr = 0, 0, ""
        for item in os.listdir(temp_dir):
            if item.startswith(self.config.get("TempFilePrefix", "_MEI")):
                try:
                    print("Delete Temp:", item)
                    shutil.rmtree(os.path.join(temp_dir, item))
                    successtimes += 1
                except Exception as e:
                    failedtimes += 1
                    print(e)
        if failedtimes >= int(self.config.get("cleanFailedTimes", 2)):
            cleantipstr = "。\n失败数量过多，请引起注意！"
        self.messager.emit(f"临时文件清理完毕，成功{successtimes}个，失败{failedtimes}个{cleantipstr}")

class GetWindowThread(QThread):
    flag = False
    exitFlag = False
    trigger = pyqtSignal(str, int, int)
    trigger1 = pyqtSignal()
    times = 0

    def __init__(self, config):
        super(GetWindowThread, self).__init__()
        self.desktop = QApplication.desktop()
        self.config = config

    def __del__(self):
        self.wait()
    
    def run(self):
        while True:
            try:
                title = gw.getActiveWindowTitle()
                print("Active Window Title:", title)
                for i in self.config:
                    if (i.get("title") == title) or (i.get("fuzzyMatching") and i.get("title") in title):
                        for _ in range(i.get("times", 5)):
                            self.trigger.emit(
                                random.choice(i.get("msg", ["检测到有人在装逼，我不说是谁", "震惊，六班竟然突破了科技封锁", "原神哥真的是太有实力啦"])),
                                self.desktop.width(),
                                self.desktop.height()
                            )
                            time.sleep(0.4)
                        self.exitFlag = True
                if self.exitFlag:
                    break
            except Exception as e:
                print(e)
            time.sleep(1)
        self.trigger1.emit()


QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
app = QApplication(sys.argv)
# setup stylesheet
# qt_material.apply_stylesheet(app, theme='dark_teal.xml')
QApplication.setQuitOnLastWindowClosed(False)
myWin = MyMainWindow()

def run():
    # init widget
    myWin.init()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()