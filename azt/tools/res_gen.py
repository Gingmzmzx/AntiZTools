# 打开icon.jpg和icon_colored.png并将文件内容写入到data.py的变量中

with open('./resources/icon.jpg', 'rb') as f:
    with open('./resources/data.py', 'w') as f2:
        f2.write('icon = ' + repr(f.read()))

with open("./resources/icon_colored.png", 'rb') as f:
    with open('./resources/data.py', 'a') as f2:
        f2.write('\nicon_colored = ' + repr(f.read()))