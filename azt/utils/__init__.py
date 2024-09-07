from PyQt5.QtWidgets import QAction
import requests


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
