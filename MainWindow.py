import requests, traceback, sys, path, subprocess, random, time, json, psutil, platform, reg
from PyQt5 import QtCore
from PyQt5 import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QAction, QMenu, QSystemTrayIcon, QDialog
from PyQt5.QtCore import QThread, pyqtSignal
from ui.Ui_form import Ui_Form
from ui.titleWindow import TitleWindow
from ui.Ui_ZBDialog import Ui_ZBDialog
from ui.Ui_TestDialog import Ui_TestDialog
from ui.Ui_password import Ui_PasswordDialog
import pygetwindow as gw
from qt_material import apply_stylesheet

def checkTUN(url="https://example.com"):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # 如果响应状态码不是200，将抛出HTTPError异常
        return False
    except Exception as e:
        print(e)
    return True

def kill_process_by_port(port):
    try:
        for conn in psutil.net_connections():
            if conn.laddr.port == port and conn.status == 'LISTEN':
                psutil.Process(conn.pid).terminate()
                print(f"Process with PID {conn.pid} killed.")
                break
    except Exception as e:
        print("Cannot kill process:", e)

class ZBDialog(QDialog, Ui_ZBDialog):
    def __init__(self, labelText, parent=None):
        super(ZBDialog, self).__init__(parent)
        self.setupUi(self)
        self.label.setText(labelText)

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.label.setStyleSheet(f"color: rgb({r}, {g}, {b})")

        self.adjustSize()
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.activateWindow()
        self.setFocus()

class TestDialog(QDialog, Ui_TestDialog):
    def __init__(self, parent=None):
        super(TestDialog, self).__init__(parent)
        self.setupUi(self)

class PasswordDialog(QDialog, Ui_PasswordDialog):
    def __init__(self, config, func, parent=None):
        super(PasswordDialog, self).__init__(parent)
        self.setupUi(self)
        self.config = config
        self.func = func
        self.label_2.setVisible(False)
        self.passwordInput.setEchoMode(Qt.QLineEdit.Password)
        self.confirmBtn.clicked.connect(self.check)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    
    def check(self):
        if self.passwordInput.text() == self.config.get("password", "ZBZ666"):
            self.func()
            self.close()
        else:
            self.label_2.setVisible(True)

class MyMainWindow(QWidget, Ui_Form):
    _TUNCmd = r"{} -f {}".format(path.path(r".\TUNBlock\clash-{}.exe"), path.path(r".\TUNBlock\config.yml"))
    getGWThreadStatus = False

    def __init__(self,parent =None):
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowIcon(QIcon("./icon.jpg"))
    
    def _initTray(self):
        self.openAction = QAction("打开主界面", self)
        self.exitAction = QAction("退出程序", self)
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.openAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.exitAction)
        self.openAction.triggered.connect(self.openPwdDialog(myWin.show))
        self.exitAction.triggered.connect(self.openPwdDialog(app.quit))
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(QIcon(path.path("icon.jpg")))
        self.trayIcon.setToolTip(self.config.get("ToolTip", "GeoGebra"))
        self.trayIcon.show()
    
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

        self.getTUNStatusThread = GetTUNStatusThread(self.config)
        self.getTUNStatusThread.trigger.connect(self.runGWThread)
        self.getTUNStatusThread.start()
        self.DisableTUN.clicked.connect(self.disableTUN)
        self.EnableTUN.clicked.connect(self.enableTUN)
        self.openTestDialogButton.clicked.connect(self.openTestDialog)
        self.clearLogsBtn.clicked.connect(self.clearLogs)
        self.titleBtn.clicked.connect(self.runGWThread)
        self.stopGetGWThread.clicked.connect(self.stopGWThread)
        self.enableAutoStart.clicked.connect(self.setAutoStart)
        self.AutoStartTipLabel.setText(path.cwdPath(self.config.get("EXEFileName", "AntiZTools.exe")))
        self.execCode.clicked.connect(self.execCodeFunc)
        
        self.crashThread = CrashThread()

        if self.config.get("TUNAutoStart", True):
            self.autoStartThread = AutoStartThread()
            self.autoStartThread.start()
        if self.config.get("StartShow", False):
            myWin.show()        
    
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
            self.getWindowThread = GetWindowThread(self.config.get("ZBMsg", []))
            self.getWindowThread.trigger.connect(self.openZBDialog)
            self.getWindowThread.trigger1.connect(self.stopGWThread)
            self.getWindowThread.start()
            self.getGWThreadStatus = True
            self.getgwstatus.setText("正在运行")
            self.getgwstatus.setStyleSheet("color: green;")
    
    def stopGWThread(self):
        try:
            self.getWindowThread.exitFlag = True
            self.getWindowThread.quit()
            self.getGWThreadStatus = False
            self.getgwstatus.setText("未运行")
            self.getgwstatus.setStyleSheet("color: red;")
        except Exception:
            pass

    def setAutoStart(self):
        autoStarter = reg.AutoStarter(path.cwdPath(self.config.get("EXEFileName", "AntiZTools.exe")), self.config.get("RegAppName", "AntiZTools"))
        if not autoStarter.is_auto_start():
            autoStarter.set_auto_start()
        if autoStarter.is_auto_start():
            self.AutoStartLabel.setText("已启用")
            self.AutoStartLabel.setStyleSheet("color: green")
            self.enableAutoStart.setDisabled(True)
    
    def openTestDialog(self):
        TestDialog().exec_()
    
    def openZBDialog(self, msg, w, h):
        zbDialog = ZBDialog(msg)
        zbDialog.label.adjustSize()
        zbDialog.move(random.randint(0, w - zbDialog.width()), random.randint(0, h - zbDialog.height()))
        zbDialog.exec_()

    def clearLogs(self):
        self.logTextarea.clear()
    
    def log(self, *args):
        self.logTextarea.append(" ".join(args))

    def disableTUN(self):
        try:
            self.crashThread.stop()
            self.TUNProcess.terminate()
        except Exception as e:
            print(e)

    def enableTUN(self):
        self._TUNCmd = self._TUNCmd.format("win32" if platform.architecture()[0] == "32bit" else "win64")
        print("Exec", self._TUNCmd)
        kill_process_by_port(9090)
        kill_process_by_port(7890)
        kill_process_by_port(7777)
        self.TUNProcess = subprocess.Popen(
            self._TUNCmd,
            stdout=subprocess.PIPE,
            universal_newlines=True,
            encoding='utf-8'
        )
        self.TUNStatus.setText("启动中...")
        self.TUNStatus.setStyleSheet("color: yellow")
        self.crashThread.start()

class AutoStartThread(QThread):
    def __init__(self):
        super(AutoStartThread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        self.times = 0
        while self.times <= 6:
            if self.times == -1: return;
            if checkTUN(): self.times += 1;
            else: self.times = -1;
        # Start TUN Mode
        if checkTUN():
            print("Cannot connect to the Internet. Starting TUN Mode...")
            myWin.widget_2_sub.enableTUN()

class GetTUNStatusThread(QThread):
    trigger = pyqtSignal()
    trigger1 = pyqtSignal()
    emitFlag = True
    emitFlag2 = True

    def __init__(self, config):
        super(GetTUNStatusThread, self).__init__()
        self.config = config

    def __del__(self):
        self.wait()

    def run(self):
        self.emitFlag = True
        self.emitFlag2 = True
        autoStarter = reg.AutoStarter(path.cwdPath(self.config.get("EXEFileName", "AntiZTools.exe")), self.config.get("RegAppName", "AntiZTools"))
        if autoStarter.is_auto_start():
            myWin.widget_2_sub.AutoStartLabel.setText("已启用")
            myWin.widget_2_sub.AutoStartLabel.setStyleSheet("color: green")
            myWin.widget_2_sub.enableAutoStart.setDisabled(True)
        else:
            myWin.widget_2_sub.AutoStartLabel.setText("未启用")
            myWin.widget_2_sub.AutoStartLabel.setStyleSheet("color: red")
        while True:
            try:
                print("getStatus...")
                if checkTUN(url=self.config.get("checkUrl", "https://example.com")):
                    if self.emitFlag:
                        self.trigger.emit()
                        self.emitFlag = False
                    myWin.widget_2_sub.TUNStatus.setStyleSheet("color: green")
                    myWin.widget_2_sub.TUNStatus.setText("已启用")
                elif "启动中..." not in myWin.widget_2_sub.TUNStatus.text():
                    if self.emitFlag2:
                        self.trigger1.emit()
                        self.emitFlag2 = False
                    myWin.widget_2_sub.TUNStatus.setStyleSheet("color: red")
                    myWin.widget_2_sub.TUNStatus.setText("未启用")
            except Exception as e:
                print(e)
            time.sleep(1)
            break

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

class CrashThread(QThread):
    trigger = pyqtSignal()
    flag = False

    def __init__(self):
        super(CrashThread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        oldLine = None
        while True:
            if self.flag:
                self.trigger.emit()
                break
            try:
                output = myWin.widget_2_sub.TUNProcess.stdout.readline().strip()
                print("Output", output)
                if output != oldLine:
                    # update text browser
                    self.appendText(output)
                    oldLine = output
            except Exception as e:
                try:
                    self.appendText(e)
                except Exception:
                    print(e)
            time.sleep(1)
    
    def appendText(self, str):
        myWin.widget_2_sub.logTextarea.append(str.rstrip())
        myWin.widget_2_sub.logTextarea.moveCursor(myWin.widget_2_sub.logTextarea.textCursor().End)
    
    def stop(self):
        self.flag = True

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
app = QApplication(sys.argv)
# setup stylesheet
# apply_stylesheet(app, theme='dark_teal.xml')
QApplication.setQuitOnLastWindowClosed(False)
myWin = TitleWindow(widget_2_sub=MyMainWindow(),icon_path=path.path("icon.jpg"),title='AntiZTools | Made for Class 6.')
myWin.setWindowIcon(QIcon("./icon.jpg"))
myWin.setWindowTitle("AntiZTools | Made for Class 6.")
myWin.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.FramelessWindowHint)

def run():
    # init widget
    myWin.widget_2_sub.init()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()