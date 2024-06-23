from PyQt5.QtCore import QThread, pyqtSignal
import random
import pygetwindow as gw
voidTitles = [
    "Studio",
    "窗口的艺术",
    "AntiZTools"
]

class MyQThread(QThread):
    exitFlag = False

    def __init__(self, width, height, parent=None):
        super().__init__(parent)
        self.width = width
        self.height = height
    
    def forceStop(self):
        self.exitFlag = True
    
    def loop(self):
        pass

    def init(self):
        pass

    def run(self):
        self.init()
        while True:
            try:
                if self.exitFlag:
                    break
                self.loop()
            except Exception:
                pass

class Aow2(MyQThread):
    def init(self):
        self.x = dict()
        self.y = dict()
        
    def moveWindow(self, window: gw.Window):
        for i in voidTitles:
            if i in window.title:
                return
        
        idx = window._hWnd
        if window.width != 200 or window.height != 200:
            window.resizeTo(200, 200)
        if (not self.x.get(idx)) or (not self.y.get(idx)):
            self.x[idx] = 2
            self.y[idx] = 2
        if window.top <= 0:
            self.y[idx] *= -1
        if window.left <= 0:
            self.x[idx] *= -1
        if window.right >= self.width:
            self.x[idx] *= -1
        if window.bottom >= self.height:
            self.y[idx] *= -1
        window.moveTo(window.left + self.x[idx], window.top + self.y[idx])

    def loop(self):
        windows = gw.getAllWindows()
        for window in windows:
            self.moveWindow(window)


class Aow1(MyQThread):
    def moveTo(self, window: gw.Window, left: int, top: int, div: int = 10):
        for i in voidTitles:
            if i in window.title:
                return

        oldLeft, oldTop = window.left, window.top
        oldLeft += (left - oldLeft) / div
        oldTop += (top - oldTop) / div
        window.moveTo(int(oldLeft), int(oldTop))
    
    def loop(self):
        for window in gw.getAllWindows():
            self.moveTo(
                window,
                random.randint(1, self.width),
                random.randint(1, self.height)
            )

class Aow3(MyQThread):
    def resizeWindow(self, window: gw.Window):
        for i in voidTitles:
            if i in window.title:
                return
        
        width, height = random.randint(200, self.width), random.randint(200, self.height)
        x, y, times, _w, _h = 6, 6, 0, 0, 0
        if width < window.width: x *= -1;
        if height < window.height: y *= -1;
        while abs(window.width - width) > 100 or abs(window.height - height) > 100:
            if abs(window.width - width) > 100:
                window.resize(x, 0)
            if abs(window.height - height) > 100:
                window.resize(0, y)
            
            if _w == 0: _w = window.width;
            if _h == 0: _h = window.height;
            if _w == window.width and _h == window.height: times += 1;
            else: times = 0;
            if times >= 10: break;
            _w, _h = window.width, window.height

            window.moveTo(
                int((self.width - window.width) / 2),
                int((self.height - window.height) / 2)
            )
    
    def loop(self):
        window = gw.getActiveWindow()
        self.resizeWindow(window)