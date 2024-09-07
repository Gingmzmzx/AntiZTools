import os, json
from azt.utils.config import Config
from azt.utils import path

path.makeSurePathExists("")

if not os.path.exists(path.path("icon.jpg")):
    from azt.resources import data
    with open(path.path("icon.jpg"), "wb") as f:
        f.write(data.icon)

if not os.path.exists(path.path("icon_colored.png")):
    from azt.resources import data
    with open(path.path("icon_colored.png"), "wb") as f:
        f.write(data.icon_colored)

config = Config()
config.update()

