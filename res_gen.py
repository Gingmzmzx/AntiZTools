# 打开icon.jpg并将文件内容写入到data.py的icon变量中

with open('icon.jpg', 'rb') as f:
    with open('data.py', 'w') as f2:
        f2.write('icon = ' + repr(f.read()))
