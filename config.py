import os, path, json

class ConfigException(Exception): pass;

class Config:
    originData = {
        "Update":{
            "version": 115,
            "forceUpdate": True
        },
        "Config": {
            "StartShow": False,
            "EXEFileName": "AntiZTools.exe",
            "Password": "ZBZ666",
            "RegAppName": "AntiZTools",
            "CheckUrl": "https://example.com",
            "FontFamily": "幼圆",
            "FontPointSize": 10
        },
        "News": {
            "NewsApi": "https://azt.xzynb.top/news/news.json",
            "Enable": True,
        },
        "TempFileClear": {
            "CleanFailedTimes": 2,
            "TempFilePrefix": "_MEI"
        },
        "Notification": {
            "Messager": {
                "MaxWidth": 300,
                "MinWidth": 300
            },
            "NotifyWindow": {
                "Height": 300,
                "Width": 200
            }
        },
        "WindowTitle": {
            "Enable": True,
            "Interval": 1,
            "hook": [
                {
                    "title": "服务",
                    "enable": True,
                    "fuzzyMatching": False,
                    "handler": "ZBDialog",
                    "data": {
                        "msg": ["检测到有人在装逼，我不说是谁", "震惊，六班竟然突破了科技封锁", "原神哥真的是太有实力啦"],
                        "times": 5,
                        "notify": True
                    }
                },
                {
                    "title": "网络和共享中心",
                    "enable": True,
                    "fuzzyMatching": False,
                    "handler": "ZBDialog",
                    "data": {
                        "msg": ["别装了..."],
                        "times": 1,
                        "notify": True
                    }
                },
                {
                    "title": "控制面板",
                    "enable": True,
                    "fuzzyMatching": False,
                    "handler": "ZBDialog",
                    "data": {
                        "msg": ["别装了..."],
                        "times": 1,
                        "notify": True
                    }
                },
                {
                    "title": "计算机管理",
                    "enable": True,
                    "fuzzyMatching": False,
                    "handler": "ZBDialog",
                    "data": {
                        "msg": ["别装了..."],
                        "times": 1,
                        "notify": True
                    }
                },
                {
                    "title": "账号登录",
                    "enable": False,
                    "fuzzyMatching": False,
                    "handler": "keyboardListener",
                    "data": {
                        "fileName": "input_analysis.log"
                    }
                },{
                    "title": "火绒",
                    "enable": True,
                    "fuzzyMatching": True,
                    "handler": "closeWindow",
                    "data": {
                        "msg": "已自动关闭不良界面",
                        "notify": True
                    }
                }
            ]
        },
        "Tray": {
            "ToolTip": "GeoGebra",
            "StartMsg": "已在后台运行"
        },
        "ScreenSaver": {
            "StartScreenSaverTimer": 0,
            "StartScreenSaverLastTime": 30*60,
            "ScreenSaverCmd": r"D:\HiteVision\electron.exe D:\HiteVision\HiteVision"
        }
    }

    def __init__(self, config_path: str = path.path("config.json")) -> None:
        self.configPath = config_path
        self.load()
    
    def load(self) -> bool:
        try:
            if not os.path.exists(self.configPath):
                with open(self.configPath, "w+", encoding="utf-8") as f:
                    f.write(json.dumps(self.originData, ensure_ascii=False))
                    self.data = self.originData
            else:
                with open(self.configPath, "r", encoding="utf-8") as f:
                    self.data = json.loads(f.read())
        except Exception as e:
            raise ConfigException(f"Error with init config.\n{e}")
        return True
        
    def get(self, key: str, defaultValue: any = None, passOnNotExists: bool = False) -> any:
        keyList = key.split(".")
        data = self.data
        originData = self.originData

        for item in keyList:
            data = data.get(item)
            originData = originData.get(item)
            if originData == None:
                if not passOnNotExists:
                    raise ConfigException(f"Unknown key {item} in {key}")
                else:
                    return defaultValue
            if data == None:
                if defaultValue == None:
                    data = originData
                else:
                    return defaultValue
        
        return data
    
    def set(self, key, value: any) -> bool:
        keyList = key.split(".")
        data = self.data

        for item in keyList[:-1]:
            if item not in data:
                data[item] = {}
            data = data[item]

        data[keyList[-1]] = value
        return True

    def save(self) -> bool:
        cfg_str = self.data
        try:
            with open(self.configPath, "w", encoding="utf-8") as f:
                f.write(json.dumps(cfg_str, ensure_ascii=False))
            return True
        except Exception as e:
            raise ConfigException(f"Error with saving config.\n{e}")

    def update(self) -> bool:
        currentVersion = self.originData.get("Update").get("version")
        if self.get("Update.version", currentVersion-1) < currentVersion and self.originData.get("Update").get("forceUpdate"):
                self.data = self.originData
                self.save()
                return True
        return False

    def autoComplete(self) -> None:
        for key in self.originData:
            if key not in self.data:
                self.data[key] = self.originData[key]
            elif type(self.originData[key]) == dict:
                for subKey in self.originData[key]:
                    if subKey not in self.data[key]:
                        self.data[key][subKey] = self.originData[key][subKey]
        self.save()

    def __del__(self):
        # self.save()
        pass

if __name__ == "__main__":
    config = Config(path.path("test_config.json"))
    print(config.get("WindowTitle.Enable"))
    config.set("WindowTitle.Enable", False)
    print(config.get("WindowTitle.Enable"))
    config.save()