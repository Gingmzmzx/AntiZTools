import requests
from PyQt5.QtCore import QThread, pyqtSignal

from .. import config

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
