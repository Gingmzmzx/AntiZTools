import sys

from . import app

def createMainWindow():
    from .ui.MainWindow import MyMainWindow

    return MyMainWindow()

myWin = createMainWindow()

def run():
    # init widget
    myWin.init()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()
