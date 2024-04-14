import path, os, json

if not os.path.exists(path.path("config.json")):
    with open(path.path("config.json"), "w+") as f:
        f.write(json.dumps({
            "TUNAutoStart": True,
            "StartShow": False,
            "ZBMsg": True,
            "ZBMsgText": ["检测到有人在装逼，我不说是谁", "装逼遭雷劈"],
            "ZBFuzzyMatching": False,
            "EXEFileName": "HackTools.exe"
        }))

import MainWindow
MainWindow.run()