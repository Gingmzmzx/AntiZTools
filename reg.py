import winreg
 
class AutoStarter():
    def __init__(self, app_path, app_name):
        self.app_path = app_path
        self.app_name = app_name
        self.run_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run'

    # 检查是否已经设置了开机自启
    def is_auto_start(self):
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.run_key) as key:
                i = 0
                while True:
                    sub_key_name = winreg.EnumValue(key, i)[0]
                    if sub_key_name == self.app_name:
                        return True
                    i += 1
        except Exception:
            return False
        return False
    
    # 设置开机自启
    def set_auto_start(self):
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.run_key, 0, winreg.KEY_SET_VALUE) as key:
                winreg.SetValueEx(key, self.app_name, 0, winreg.REG_SZ, self.app_path)
                return True
        except OSError as e:
            return False
