# AntiZTools
反周神器

## 1. 介绍
缘由详见[装逼遭雷劈（四）](https://xzynb.top/blog/%E8%A3%85%E9%80%BC%E9%81%AD%E9%9B%B7%E5%8A%88%EF%BC%884%EF%BC%89/)

## 2. 特性
- 检测窗口标题、弹出弹窗、关闭窗口
- 禁用或启用`计算机管理`
- 开机自启
- 托盘图标以及菜单
- 退出/打开主界面需要密码
- 自动清理临时文件
- 调试功能
- 窗口艺术
- 插件支持
- 监听鼠标键盘输入
- 文件DES加密
- 其他特性尽请体验

## 3. 构建
```shell
# 克隆项目
git clone https://github.com/Gingmzmzx/AntiZTools/
cd AntiZTools

# 安装依赖
pip install -r requirements.txt

# 生成资源文件
cd azt
python tools/res_gen.py
cd ..

# 构建
vim build.spec # 修改`pathx`以及exe图标路径
pyinstaller build.spec
```
