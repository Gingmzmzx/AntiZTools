import path, os, json

if not os.path.exists(path.path("config.json")):
    with open(path.path("config.json"), "w+") as f:
        f.write(json.dumps({
            "TUNAutoStart": True,
            "StartShow": False,
            "AntiZB": True,
            "ZBMsg": [
                {
                    "title": "服务",
                    "fuzzyMatching": False,
                    "msg": ["检测到有人在装逼，我不说是谁", "装逼遭雷劈"],
                    "times": 10
                },
                {
                    "title": "计算机管理",
                    "fuzzyMatching": False,
                    "msg": ["检测到有人在装逼，我不说是谁", "装逼遭雷劈"],
                    "times": 10
                }
            ],
            "EXEFileName": "HackTools.exe",
            "RegAppName": "AntiZTools",
            "password": "ZBZ666"
        }))

if not os.path.exists(path.path("icon.jpg")):
    import data
    with open(path.path("icon.jpg"), "wb") as f:
        f.write(data.icon)

import MainWindow
MainWindow.run()