import requests, traceback, random, json, os, ctypes, webbrowser, base64
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QImage
from PyQt5.QtWidgets import QApplication, QMessageBox, QMenu, QSystemTrayIcon, QMainWindow
from PyQt5.QtCore import QTimer

from .. import config
from ..utils.notify import NotificationWindow, WindowNotify
from ..utils import reg, path, checkNetwork, MyQAction
from ..ui.design.Ui_form import Ui_Form
from ..ui.DebugForm import DebugForm
from ..ui.PasswordDialog import PasswordDialog
from ..ui.ZBDialog import ZBDialog
from ..ui.AowForm import AowForm
from ..threads.AutoStartThread import AutoStartThread
from ..threads.GetWindowThread import GetWindowThread
from ..threads.KeyBoardThread import KeyBoardThread
from ..threads.GetNewsThread import GetNewsThread
from ..threads.RunCodeThread import RunCodeThread
from .. import app


class MyMainWindow(QMainWindow, Ui_Form):
    getGWThreadStatus = False
    ssTimerFlag = False
    keyboardThreadStatus = False

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
        self.openAction = MyQAction("打开主界面", self)
        self.exitAction = MyQAction("退出程序", self)
        self.aowAction = MyQAction("窗口的艺术", self)
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addActions((self.stOnStAction, self.winTitleAction, self.conStatusAction))
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.aowAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addActions((self.openAction, self.exitAction))
        self.openAction.triggered.connect(self.openPwdDialog(self.show))
        self.exitAction.triggered.connect(self.openPwdDialog(app.quit))
        self.aowAction.triggered.connect(self.openAowDialog)
        self.winTitleAction.changeText("未运行")
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(self.qIcon)
        self.trayIcon.setToolTip(config.get("Tray.ToolTip"))
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
        self._initTray()
        self.desktop = QApplication.desktop()

        self.autoStartThread = AutoStartThread()
        self.autoStartThread.execer.connect(self.execInnerFunc)
        self.autoStartThread.logger.connect(self.log)
        self.autoStartThread.messager.connect(self.showMessage)
        self.autoStartThread.start()
        
        self.clearLogsBtn.clicked.connect(self.clearLogs)
        self.titleBtn.clicked.connect(self.runGWThread)
        self.stopGetGWThread.clicked.connect(self.stopGWThread)
        self.enableAutoStart.clicked.connect(self.setAutoStart)
        self.AutoStartTipLabel.setText(path.cwdPath(config.get("Config.EXEFileName")))

        self.execCode.clicked.connect(self.execCodeFunc)
        self.execCode_2.clicked.connect(self.execCodeThreadFunc)
        self.debugHelpBtn.clicked.connect(self.debugHelp)

        self.disableController.clicked.connect(self.disableControllerFunc)
        self.enableController.clicked.connect(self.enableControllerFunc)

        self.openDebugForm.clicked.connect(self.openDebugFormFunc)
        
        self.resetCfg()
        self.saveCfgBtn.clicked.connect(self.saveCfg)
        self.reCfgBtn.clicked.connect(self.resetCfg)
        self.acCfgBtn.clicked.connect(self.acCfg)

        self.reFileBtn.clicked.connect(self.loadFileContent)
        self.saveFileBtn.clicked.connect(self.saveFileContent)

        self.getWindowThread = GetWindowThread(self.desktop.width(), self.desktop.height())
        self.getWindowThread.execer.connect(self.execInnerFunc)
        self.getWindowThread.logger.connect(self.log)
        self.getWindowThread.stopThread.connect(self.stopGWThread)
        self.runGWThread()

        self.keyboardThread = KeyBoardThread()

        self.log("<p style='color:green;'>Init Success!</p>")

        if int(config.get("ScreenSaver.StartScreenSaverTimer")) != 0:
            self.ssTimer = QTimer()
            self.ssTimer.timeout.connect(self.startScreenSaver)
            self.ssTimer.start(int(config.get("ScreenSaver.StartScreenSaverTimer"))*1000)
        if config.get("Config.StartShow"):
            self.log("<i>Show on starting.</i>")
            self.show()
        if config.get("Tray.StartMsg") != "":
            self.log("<i>Show Tray Message.</i>")
            self.showMessage(config.get("Tray.StartMsg"))
        if config.get("News.Enable"):
            self.getNewsThread = GetNewsThread()
            self.getNewsThread.execer.connect(self.execInnerFunc)
            self.getNewsThread.logger.connect(self.log)
            self.getNewsThread.start()

    def changeStatus(self, type: str, flag: bool):
        if type == "autoStarter":
            if flag:
                self.AutoStartLabel.setText("已启用")
                self.AutoStartLabel.setStyleSheet("color: green")
                self.enableAutoStart.setDisabled(True)
                self.stOnStAction.changeText("已启用")
            else:
                self.AutoStartLabel.setText("未启用")
                self.AutoStartLabel.setStyleSheet("color: red")
                self.stOnStAction.changeText("未启用")
        elif type == "controllerStatus":
            if flag:
                self.controllerStatus.setText("已禁用")
                self.controllerStatus.setStyleSheet("color: red")
                self.disableController.setDisabled(True)
                self.conStatusAction.changeText("已禁用")
            else:
                self.controllerStatus.setText("未禁用")
                self.controllerStatus.setStyleSheet("color: green")
                self.enableController.setDisabled(True)
                self.conStatusAction.changeText("未禁用")

    def loadFileContent(self):
        _path: str = self.filepathInput.text()
        self.log(f"Load file in {_path}")
        content: str = ""
        if not os.path.exists(path.path(_path)):
            self.log("<b style='color:red;'>File not found!</b>")
            self.viewFileTextarea.setText("<b style='color:red;'>File not found!</b>")
            return
        with open(path.path(_path), "r", encoding="utf-8") as f:
            content = f.read()
        try:
            content = base64.b64decode(content).decode("utf-8")
        except Exception:
            self.log("Cannot b64decode file content!")
        self.viewFileTextarea.setText(content)

    def saveFileContent(self):
        _path: str = self.filepathInput.text()
        self.log(f"Load file in {_path}")
        if not os.path.exists(path.path(_path)):
            self.log("<b style='color:red;'>File not found!</b>")
            self.viewFileTextarea.setText("<b style='color:red;'>File not found!</b>")
            return
        content: str = self.viewFileTextarea.toPlainText()
        flag = True
        with open(path.path(_path), "w", encoding="utf-8") as f:
            try:
                f.write(base64.b64encode(bytes(content, "utf-8")).decode("utf-8"))
            except Exception as e:
                flag = False
                QMessageBox.warning(self, "保存失败", str(e))
        if flag:
            QMessageBox.information(self, "保存成功", "保存成功！")

    def NotifyWindow(self, title, content, banner=False, detail=None, timeout=1000*60*3):
        def viewCallback(_):
            print(detail)
            if detail:
                webbrowser.open(detail)
        img = False
        if banner:
            res = requests.get(banner)
            img = QImage.fromData(res.content)
        WindowNotify(app, f"{config.get('Tray.ToolTip')}每日资讯", title, content, img, timeout=timeout, viewCallback=viewCallback, parent=self).show().showAnimation()

    def openAowDialog(self):
        self.aowForm = AowForm(self.desktop.width(), self.desktop.height())
        self.aowForm.show()

    def openDebugFormFunc(self):
        if self.getGWThreadStatus:
            tt = self.debugFormTitle.text()
            tt = tt if tt else "debugForm"
            self.debugForm = DebugForm(tt, self.desktop.width(), self.desktop.height())
            self.debugForm.closeBtn.clicked.connect(self.closeDebugForm)
            self.getWindowThread.debugFormStatus = True
            self.debugForm.show()
        else:
            QMessageBox.warning(self, "调试窗口", "请先启动getGW线程")

    def setDebugForm(self, title):
        if self.debugForm:
            self.debugForm.setTitleText(title)

    def closeDebugForm(self):
        if self.getGWThreadStatus:
            self.getWindowThread.debugFormStatus = False
        self.debugForm.close()

    def startScreenSaver(self):
        try:
            lit = self.getLastInputTime()
            self.log("LastInputTime:", lit)
            if lit >= int(config.get("ScreenSaver.StartScreenSaverLastTime")):
                if not self.ssTimerFlag:
                    self.ssTimerFlag = True
                    self.log("<p style='color:green;'>Starting ScreenSaver</p>")
                    os.system(config.get("ScreenSaver.ScreenSaverCmd"))
            else:
                self.ssTimerFlag = False
        except Exception as e:
            self.log("<p style='color:red;'>StartingScreenTimerException:", str(e), "</p>")
            self.log("<i>Stopping StartingScreenTimer</i>")
            self.ssTimer.stop()

    def getLastInputTime(self):
        user32 = ctypes.windll.user32
        kernel32 = ctypes.windll.kernel32

        class LASTINPUTINFO(ctypes.Structure):
            _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_ulong)]

        lii = LASTINPUTINFO()
        lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
        user32.GetLastInputInfo(ctypes.byref(lii))
        millis = kernel32.GetTickCount() - lii.dwTime
        seconds = millis / 1000
        return seconds
    
    def showMessage(self, msg, *args, **kwargs):
        try:
            self.trayIcon.showMessage(config.get("Tray.ToolTip"), msg, self.qIcon, *args, **kwargs)
        except Exception:
            pass

    def saveCfg(self):
        cfg_str = self.CfgTextarea.toPlainText()
        try:
            config.data = json.loads(cfg_str)
            config.save()
            QMessageBox.information(self, "保存成功", "保存成功！\n有些功能重启程序后生效")
        except Exception as e:
            QMessageBox.warning(self, "保存失败", "保存失败！\n{}".format(str(e)))
    
    def resetCfg(self):
        self.CfgTextarea.setText(json.dumps(config.data, ensure_ascii=False, indent=4))
    
    def acCfg(self):
        config.autoComplete()
        self.resetCfg()
    
    def debugHelp(self):
        QMessageBox.information(self, "调试指南", """
        主线程执行：在MainWindow中执行代码\n
        子线程执行：在RunCodeThread中执行代码\n
        在主线程中，调用self.log(*args)来输出调试信息到日志框\n
        在子线程中，调用self.logger.emit(str)来输出调试信息到日志框\n
        在子线程中，调用self.execer.emit(str, (args,))来执行主线程名为str的方法，并附带参数*(args,)
        """)

    def execCodeFunc(self):
        try:
            exec(self.DebugCode.toPlainText())
        except Exception as e:
            self.log(str(e))
    
    def execCodeThreadFunc(self):
        runCodeThread = RunCodeThread(self.DebugCode.toPlainText())
        runCodeThread.logger.connect(self.log)
        runCodeThread.execer.connect(self.execInnerFunc)
        runCodeThread.start()
    
    def execInnerFunc(self, func, args):
        try:
            getattr(self, func)(*args)
        except Exception as e:
            self.log(str(e))
    
    def notifySuccess(self, title, msg):
        NotificationWindow.success(app, title, msg)
    
    def notifyError(self, title, msg):
        NotificationWindow.error(app, title, msg)

    def notifyInfo(self, title, msg):
        NotificationWindow.info(app, title, msg)
    
    def notifyWarning(self, title, msg):
        NotificationWindow.warning(app, title, msg)

    def openPwdDialog(self, func):
        def _openPwdDialog():
            PasswordDialog(func).exec_()
        return _openPwdDialog

    def runGWThread(self):
        if config.get("WindowTitle.Enable") and self.getGWThreadStatus == False:
            self.getWindowThread.exitFlag = False
            self.getWindowThread.start()
            self.getGWThreadStatus = True
            self.getgwstatus.setText("正在运行")
            self.getgwstatus.setStyleSheet("color: green;")
            self.winTitleAction.changeText("正在运行")

    def stopGWThread(self):
        try:
            self.getWindowThread.forceStop()
            self.getWindowThread.quit()
            self.getGWThreadStatus = False
            self.getgwstatus.setText("未运行")
            self.winTitleAction.changeText("未运行")
            self.getgwstatus.setStyleSheet("color: red;")
        except Exception:
            pass
    
    def runKeyBoardThread(self, fileName):
        if self.keyboardThreadStatus == False:
            self.keyboardThreadStatus = True
            self.keyboardThread.fileName = fileName
            self.keyboardThread.start()
    
    def stopKeyBoardThread(self):
        try:
            self.keyboardThread.forceStop()
            self.keyboardThread.quit()
            self.keyboardThreadStatus = False
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
        autoStarter = reg.AutoStarter(path.cwdPath(config.get("Config.EXEFileName")), config.get("Config.RegAppName"))
        if not autoStarter.is_auto_start():
            autoStarter.set_auto_start()
        if autoStarter.is_auto_start():
            self.AutoStartLabel.setText("已启用")
            self.stOnStAction.changeText("已启用")
            self.AutoStartLabel.setStyleSheet("color: green")
            self.enableAutoStart.setDisabled(True)
    
    def openZBDialog(self, msg, w, h):
        zbDialog = ZBDialog(msg)
        # zbDialog.label.adjustSize()
        zbDialog.move(random.randint(0, w - zbDialog.width()), random.randint(0, h - zbDialog.height()))
        zbDialog.exec_()

    def clearLogs(self):
        self.logTextarea.clear()
    
    def log(self, *args):
        logStr = ""
        for i in args:
            logStr += str(i) + " "
        self.logTextarea.append(logStr)
