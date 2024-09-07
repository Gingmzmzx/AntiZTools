import requests
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage
from ..utils.notify import WindowNotify
from .. import app

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
                # title, content, banner, detail = i.get("title"), i.get("content"), i.get("banner", False), i.get("detail", None)
                # img = False
                # def viewCallback(_):
                #     if detail:
                #         import webbrowser
                #         webbrowser.open(detail)
                # if banner:
                #     res = requests.get(banner)
                #     img = QImage.fromData(res.content)
                # WindowNotify(app, f"{config.get('Tray.ToolTip')}每日资讯", title, content, img, timeout=60*5, viewCallback=viewCallback).show().showAnimation()
                self.execer.emit("NotifyWindow", (i.get("title"), i.get("content"), i.get("banner", False), i.get("detail", None)))
                break
        except Exception:
            self.logger.emit(f"<p style='color:red;'>Cannot get News from '{config.get('News.NewsApi')}'!</p>")
