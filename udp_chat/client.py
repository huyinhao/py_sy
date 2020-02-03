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

# 客户端
import socket
import threading
import passmain


def recv(sock, addr):
    # 一个UDP连接在接收消息前必须要让系统知道所占端口也就是需要send一次，否则会报错
    sock.sendto(login_user.encode('utf-8'), addr)
    # 接收服务端发送的信息
    while True:
        data = sock.recv(1024)
        print(data.decode('utf-8'))


def send(sock, addr):
    # 给服务端发送信息
    while True:
        string = input()
        # 格式：用户名：消息
        message = login_user + ':' + string + ' '
        data = message.encode('utf-8')
        sock.sendto(data, addr)
        if string.upper() == 'EXIT':
            break


def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ('127.0.0.1', 9999)

    # 设置daemon=True会标记其为守护线程，如果剩下的线程只有守护线程时，整个python程序都会退出
    # 接收线程
    t_recv = threading.Thread(target=recv, args=(client_socket, server), daemon=True)
    # 发送线程
    t_send = threading.Thread(target=send, args=(client_socket, server))
    t_recv.start()
    t_send.start()
    # 等待发送线程终止
    t_send.join()
    client_socket.close()


if __name__ == '__main__':
    print("-----欢迎来到聊天室,退出聊天室请输入'EXIT'-----")
    print()
    print('==========login=========')
    login_user = input('----------input your username-------')
    count = 0
    if passmain.exited_username(login_user) == 1:  # 用户已存在
        passmain.login_password(login_user, count)  # 输入密码
    else:
        print('%s does not exited,please signup' % login_user)  # 用户不存在，注册
        login_user = passmain.signup()
    print('/*********%s login success*********/' % login_user)
    print('单播 to username message   广播 toall message')
    main()
