import path, os, json

path.makeSurePathExists("")

if not os.path.exists(path.path("config.json")):
    with open(path.path("config.json"), "w+", encoding="utf-8") as f:
        f.write(json.dumps({
            "TUNAutoStart": False,
            "StartShow": False,
            "AntiZB": True,
            "ZBMsg": [
                {
                    "title": "服务",
                    "fuzzyMatching": False,
                    "msg": ["检测到有人在装逼，我不说是谁", "震惊，六班竟然突破了科技封锁", "原神哥真的是太有实力啦"],
                    "times": 5
                },
                {
                    "title": "计算机管理",
                    "fuzzyMatching": False,
                    "msg": ["检测到有人在装逼，我不说是谁", "震惊，六班竟然突破了科技封锁", "原神哥真的是太有实力啦"],
                    "times": 5
                }
            ],
            "EXEFileName": "AntiZTools.exe",
            "RegAppName": "AntiZTools",
            "password": "ZBZ666",
            "checkUrl": "https://example.com",
            "ToolTip": "GeoGebra"
        }, ensure_ascii=False))

if not os.path.exists(path.path("icon.jpg")):
    import data
    with open(path.path("icon.jpg"), "wb") as f:
        f.write(data.icon)

import MainWindow
MainWindow.run()