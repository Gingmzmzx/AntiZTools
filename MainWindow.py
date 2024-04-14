import requests, traceback, sys, path, subprocess, random, time, json, psutil, platform, reg, os
from PyQt5 import QtCore
from PyQt5 import Qt
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QAction, QMenu, QSystemTrayIcon, QDialog, QLabel, QSizePolicy
from PyQt5.QtCore import QThread, pyqtSignal
from ui.Ui_form import Ui_Form
from ui.titleWindow import TitleWindow
from ui.Ui_ZBDialog import Ui_ZBDialog
from ui.Ui_TestDialog import Ui_TestDialog
import pygetwindow as gw

def checkTUN():
    try:
        response = requests.get("https://example.com", timeout=5)
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
        self.label.setText(random.choice(labelText))

        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.label.setStyleSheet(f"QLabel {{ color: rgb({r}, {g}, {b}) }}")

        self.adjustSize()

class TestDialog(QDialog, Ui_TestDialog):
    def __init__(self, parent=None):
        super(TestDialog, self).__init__(parent)
        self.setupUi(self)

class MyMainWindow(QWidget, Ui_Form):
    _TUNCmd = r"{} -f {}".format(path.path(r".\TUNBlock\clash-{}.exe"), path.path(r".\TUNBlock\config.yml"))

    def __init__(self,parent =None):
        super(MyMainWindow,self).__init__(parent)
        self.setupUi(self)
        self.setFixedSize(self.width(), self.height())
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowIcon(QIcon("./icon.jpg"))
    
    def _initTray(self):
        self.openAction = QAction("打开主界面", self)
        self.exitAction = QAction("退出程序", self)
        self.aboutAction = QAction("关于", self)
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.openAction)
        self.trayIconMenu.addAction(self.exitAction)
        self.trayIconMenu.addSeparator()
        self.trayIconMenu.addAction(self.aboutAction)
        self.openAction.triggered.connect(myWin.show)
        self.exitAction.triggered.connect(app.quit)
        self.aboutAction.triggered.connect(self.about)
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(QIcon(path.path("icon.jpg")))
        self.trayIcon.setToolTip("HackTools")
        self.trayIcon.show()
    
    def init(self):
        try:
            self._init()
        except Exception as e:
            print(traceback.format_exc())
            QMessageBox.warning(self, "发生错误", "运行发生错误，请将下列错误信息提交给开发者：\n{}".format(str(e)))

    def _init(self):
        with open(path.path("config.json"), "r") as f:
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
        self.enableAutoStart.clicked.connect(self.setAutoStart)
        self.AutoStartTipLabel.setText(path.path(self.config.get("EXEFileName", "HackTools.exe")))
        self.TUNAutoStartCheckbox.stateChanged.connect(self.switchAutoStartStatus)

        if self.config.get("TUNAutoStart", True):
            self.TUNAutoStartCheckbox.setChecked(True)
        else:
            self.TUNAutoStartCheckbox.setChecked(False)
        
        self.crashThread = CrashThread()

        if self.config.get("TUNAutoStart", True):
            self.autoStartThread = AutoStartThread()
            self.autoStartThread.start()
        if self.config.get("StartShow", False):
            myWin.show()
    
    def runGWThread(self):
        if self.config.get("ZBMsg", True):
            self.getWindowThread = GetWindowThread(self.config)
            self.getWindowThread.trigger.connect(self.openZBDialog)
            self.getWindowThread.start()

    def setAutoStart(self):
        autoStarter = reg.AutoStarter(path.path(self.config.get("EXEFileName", "HackTools.exe")), "HackTools")
        if not autoStarter.is_auto_start():
            autoStarter.set_auto_start()
    
    def openTestDialog(self):
        TestDialog().exec_()
    
    def openZBDialog(self):
        zbDialog = ZBDialog(self.config.get("ZBMsgText", ["检测到有人在装逼，我不说是谁", "装逼遭雷劈"]))
        zbDialog.label.adjustSize()
        zbDialog.exec_()
    
    def switchAutoStartStatus(self):
        status = self.TUNAutoStartCheckbox.isChecked()

    def clearLogs(self):
        self.logTextarea.clear()

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

    def about(self):
        QMessageBox.information(self, "About", "关于HackTools。\n由xzy编写。")

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

    def __init__(self, config):
        super(GetTUNStatusThread, self).__init__()
        self.config = config

    def __del__(self):
        self.wait()

    def run(self):
        autoStarter = reg.AutoStarter(path.path(self.config.get("EXEFileName", "HackTools.exe")), "HackTools")
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
                if checkTUN():
                    self.trigger.emit()
                    myWin.widget_2_sub.TUNStatus.setStyleSheet("color: green")
                    myWin.widget_2_sub.TUNStatus.setText("已启用")
                elif "启动中..." not in myWin.widget_2_sub.TUNStatus.text():
                    myWin.widget_2_sub.TUNStatus.setStyleSheet("color: red")
                    myWin.widget_2_sub.TUNStatus.setText("未启用")
            except Exception as e:
                print(e)

class GetWindowThread(QThread):
    flag = False
    trigger = pyqtSignal()

    def __init__(self, config):
        super(GetWindowThread, self).__init__()
        self.config = config

    def __del__(self):
        self.wait()
    
    def run(self):
        while True:
            try:
                title = gw.getActiveWindowTitle()
                print("Active Window Title:", title)
                if title == "服务" or (self.config.get("ZBFuzzyMatching", False) and "服务" in title):
                    self.flag = True
                    self.trigger.emit()
                elif self.flag and "ZBMsgDialog" not in title:
                    break
            except Exception as e:
                print(e)
            time.sleep(1)

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

app = QApplication(sys.argv)
# setup stylesheet
# apply_stylesheet(app, theme='dark_teal.xml')
QApplication.setQuitOnLastWindowClosed(False)
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
myWin = TitleWindow(widget_2_sub=MyMainWindow(),icon_path=path.path("icon.jpg"),title='HackTools | Made for Class 6.')
myWin.setWindowIcon(QIcon("./icon.jpg"))
myWin.setWindowTitle("HackTools | Made for Class 6.")
myWin.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint|QtCore.Qt.FramelessWindowHint)

def run():
    # init widget
    myWin.widget_2_sub.init()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()