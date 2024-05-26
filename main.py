import path, os, json

path.makeSurePathExists("")

if not os.path.exists(path.path("config.json")):
    with open(path.path("config.json"), "w+", encoding="utf-8") as f:
        f.write(json.dumps({
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
                    "title": "网络和共享中心",
                    "fuzzyMatching": False,
                    "msg": ["别装了..."],
                    "times": 1
                },
                {
                    "title": "控制面板",
                    "fuzzyMatching": False,
                    "msg": ["别装了..."],
                    "times": 1
                },
                {
                    "title": "计算机管理",
                    "fuzzyMatching": False,
                    "msg": ["别装了..."],
                    "times": 1
                }
            ],
            "EXEFileName": "AntiZTools.exe",
            "RegAppName": "AntiZTools",
            "password": "ZBZ666",
            "checkUrl": "https://example.com",
            "ToolTip": "GeoGebra",
            "startMsg": "已在后台运行",
            "cleanFailedTimes": 2,
            "TempFilePrefix": "_MEI"
        }, ensure_ascii=False))

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