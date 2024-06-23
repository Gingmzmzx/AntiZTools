import path, os, json

path.makeSurePathExists("")

if not os.path.exists(path.path("icon.jpg")):
    import data
    with open(path.path("icon.jpg"), "wb") as f:
        f.write(data.icon)

if not os.path.exists(path.path("icon_colored.png")):
    import data
    with open(path.path("icon_colored.png"), "wb") as f:
        f.write(data.icon_colored)

import MainWindow
MainWindow.run()