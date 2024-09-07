import os, shutil, tempfile
from PyQt5.QtCore import QThread, pyqtSignal

from .. import config
from ..utils import reg, path


class AutoStartThread(QThread):
    execer = pyqtSignal(str, tuple)
    logger = pyqtSignal(str)
    messager = pyqtSignal(str)

    def __init__(self):
        super(AutoStartThread, self).__init__()

    def __del__(self):
        self.wait()

    def run(self):
        autoStarter = reg.AutoStarter(path.cwdPath(config.get("Config.EXEFileName")), config.get("Config.RegAppName"))
        if autoStarter.is_auto_start():
            self.execer.emit("changeStatus", ("autoStarter", True))
        else:
            self.execer.emit("changeStatus", ("autoStarter", False))
        
        controllerStatus = reg.ControllerStatus()
        if controllerStatus.status():
            self.execer.emit("changeStatus", ("controllerStatus", True))
        else:
            self.execer.emit("changeStatus", ("controllerStatus", False))
        
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
