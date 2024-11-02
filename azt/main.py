import sys

from . import app, tmp


def createMainWindow():
    from .ui.MainWindow import MyMainWindow

    return MyMainWindow()

myWin = createMainWindow()
firstFlag = True

def run():
    if tmp.get("eula", False):
        # 首次启动需要同意协议
        from .ui.EulaForm import EulaForm
        eulaForm = EulaForm()
        eulaForm.show()
        tmp.pop("eula")
    else:
        myWin.init()
    
    global firstFlag
    if firstFlag:
        firstFlag = False
        sys.exit(app.exec_())

if __name__ == "__main__":
    run()
