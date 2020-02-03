import base64

f = open('E:/html_css/旋转盒子/view.gif', 'rb')  # 二进制方式打开图文件
ls_f = base64.b64encode(f.read())  # 读取文件内容，转换为base64编码
ff = open('C:/Users/ASUS/Desktop/base64.txt', 'w')
ff.write(str(ls_f))
f.close()
ff.close()
print(ls_f)
