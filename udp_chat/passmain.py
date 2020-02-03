#  我真诚地保证：
#  我自己独立地完成了整个程序从分析、设计到编码的所有工作。
#  如果在上述过程中，我遇到了什么困难而求教于人，那么，我将在程序实习报告中
#  详细地列举我所遇到的问题，以及别人给我的提示。
#  在此，我感谢 XXX, …, XXX对我的启发和帮助。下面的报告中，我还会具体地提到
#  他们在各个方法对我的帮助。
#  我的程序里中凡是引用到其他程序或文档之处，
#  例如教材、课堂笔记、网上的源代码以及其他参考书上的代码段,
#  我都已经在程序的注释里很清楚地注明了引用的出处。

#  我从未没抄袭过别人的程序，也没有盗用别人的程序，
#  不管是修改式的抄袭还是原封不动的抄袭。
#  我编写这个程序，从来没有想过要去破坏或妨碍其他计算机系统的正常运转。
#  <胡崟昊>


# 登录和注册
# 获取本地文件中记录的用户名
def getuser():
    file = 'user.txt'
    user_pass = readfile(file)
    data = user_pass.split('\n')
    return data


# 用户是否存在
def exited_username(login_user):
    data = getuser()

    chose_fun(login_user)
    # count = 0
    for i in data:
        a = i.split(':')[0]  # 用户名是否存在

        if login_user == a:
            return 1

    return 0


# 登录，输入密码
def login_password(login_user, count):
    print()
    print('==========%s login=========' % login_user)
    login_pass = input('----------%s input your password----------' % login_user)

    data = getuser()

    chose_fun(login_pass)  # 退出

    for i in data:
        a = i.split(':')[0]
        b = i.split(':')[1]
        if login_user == a:  # 验证密码
            if login_pass == b:
                print('/*********%s login success*********/' % login_user)  # 密码正确，登录成功
                print('/********* %s /*********' % login_user)
                break

            else:  # 密码错误
                print('==========%s password is not correct,please try again==========' % login_user)
                count = count + 1
                if count == 3:
                    # 最多三次输错密码的机会
                    print('==========%s password incorrect too much time,exit==========' % login_user)
                    exit()  # 直接退出

                login_password(login_user, count)  # 重新输入密码
    return 0


# 注册，新建用户名和密码
def signup():
    print()
    print('==========signup=========')

    signup_user = input('----------input your username----------')
    chose_fun(signup_user)  # 退出

    # 判断用户名是否已存在
    if exited_username(signup_user) == 1:
        print('username already exited,re signup')
        signup()

    # 设置密码
    signup_pass1 = input('----------%s input your password----------' % signup_user)
    chose_fun(signup_user)  # 退出
    signup_pass2 = input('----------%s confirm your password----------' % signup_user)
    chose_fun(signup_user)  # 退出
    if signup_pass1 == signup_pass2:
        writefile(signup_user, signup_pass1)  # 写入注册名单

    else:
        print('==========%s passwords incorrect,please reset==========' % signup_user)  # 两次密码输入不正确，重新注册
        signup()

    return signup_user


# 读取注册用户文件
def readfile(file):
    f = open(file, 'r', True, 'utf-8')  # 读取注册名单
    user_pass = ''
    while True:
        line = f.readline()
        user_pass = user_pass + line

        if not line: break
    f.close()
    # print('user'+user_pass)
    # print('end')
    return user_pass


# 写入新注册用户
def writefile(signup_user, signup_pass):
    file = 'user.txt'
    f = open(file, 'a+', True, 'utf-8')
    f.write('\n' + signup_user + ':' + signup_pass)  # 将新用户写入文件
    f.flush()
    f.close()


# 退出程序
def chose_fun(login_user):
    if login_user.upper() == 'EXIT':
        exit(0)


