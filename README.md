# AntiZTools
反周神器

## 1. 介绍
缘由详见[装逼遭雷劈（四）](https://xzynb.top/blog/%E8%A3%85%E9%80%BC%E9%81%AD%E9%9B%B7%E5%8A%88%EF%BC%884%EF%BC%89/)

## 2. 特性
- 检测窗口标题、弹出弹窗
- 禁用或启用`计算机管理`
- 开机自启
- 托盘图标
- 其他特性尽请体验

## 3. 构建
- 安装依赖`pip install -r requirements.txt`
- 编辑`main.spec`，将`E:\Projects\AntiZTools`换为您的项目地址
- 运行`python res_gen.py`生成`data.py`资源文件（确保`icon.jpg`和`icon_colored.png`在同级目录下）
- 运行`pyinstaller main.spec`构建