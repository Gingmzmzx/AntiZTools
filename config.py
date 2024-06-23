import os, path, json

class ConfigException(Exception):
    def __init__(self, message):
        super().__init__(message)

class Config:
    originData = {
        "Config": {
            "StartShow": False,
            "EXEFileName": "AntiZTools.exe",
            "Password": "ZBZ666",
            "RegAppName": "AntiZTools",
            "CheckUrl": "https://example.com"
        },
        "TempFileClear": {
            "CleanFailedTimes": 2,
            "TempFilePrefix": "_MEI"
        },
        "WindowTitle": {
            "Enable": True,
            "Interval": 1,
            "hook": [
                {
                    "title": "服务",
                    "fuzzyMatching": False,
                    "handler": "ZBDialog",
                    "data": {
                        "msg": ["检测到有人在装逼，我不说是谁", "震惊，六班竟然突破了科技封锁", "原神哥真的是太有实力啦"],
                        "times": 5
                    }
                },
                {
                    "title": "网络和共享中心",
                    "fuzzyMatching": False,
                    "handler": "ZBDialog",
                    "data": {
                        "msg": ["别装了..."],
                        "times": 1
                    }
                },
                {
                    "title": "控制面板",
                    "fuzzyMatching": False,
                    "handler": "ZBDialog",
                    "data": {
                        "msg": ["别装了..."],
                        "times": 1
                    }
                },
                {
                    "title": "计算机管理",
                    "fuzzyMatching": False,
                    "handler": "ZBDialog",
                    "data": {
                        "msg": ["别装了..."],
                        "times": 1
                    }
                },
                {
                    "title": "账号登录",
                    "fuzzyMatching": False,
                    "handler": "ListenPassword"
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
            data = data.get(item, defaultValue)
            originData = originData.get(item)
            if originData == None:
                if not passOnNotExists:
                    raise ConfigException(f"Unknown key {item} in {key}")
                else:
                    return defaultValue
            if data == None:
                data = originData
        
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

    def __del__(self):
        # self.save()
        pass

if __name__ == "__main__":
    config = Config(path.path("test_config.json"))
    print(config.get("WindowTitle.Enable"))
    config.set("WindowTitle.Enable", False)
    print(config.get("WindowTitle.Enable"))
    config.save()