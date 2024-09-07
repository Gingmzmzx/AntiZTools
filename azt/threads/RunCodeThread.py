from PyQt5.QtCore import QThread, pyqtSignal


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
