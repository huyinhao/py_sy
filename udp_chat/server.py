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

# 服务端
import socket


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    addr = ('127.0.0.1', 9999)
    s.bind(addr)
    print('UDP Server on ' + addr[0] + ': ' + str(addr[1]) + '...')

    user = {}  # {addr:name}

    while True:
        try:
            data, addr = s.recvfrom(1024)

            # if not addr in user:
            # 用户刚登录
            if addr not in user:
                for address in user:
                    s.sendto(data + ' 进入聊天室...'.encode(), address)
                user[addr] = data.decode('utf-8')

                continue

            # 用户登录后，发送信息
            message = data.decode('utf-8').split(' ')
            print('message---%s ' % message)
            top = message[0].split(':')
            count = 0

            # to命令表示单播
            if top[1].upper() == 'TO':

                for address in user:
                    if user[address] == message[1] and addr != address:
                        to_data = (top[0] + ':' + message[2]).encode('utf-8')
                        s.sendto(to_data, address)
                    count = count + 1

                continue

            # toall命令表示广播
            if top[1].upper() == 'TOALL':

                for address in user:
                    if addr != address:
                        to_data = (top[0] + '--to--all' + ':' + message[1]).encode('utf-8')
                        s.sendto(to_data, address)

            # 用户退出
            if top[1].upper() == 'EXIT':

                for address in user:
                    if addr != address:
                        s.sendto((top[0] + ' 离开了聊天室...').encode(), address)

            else:
                print('"%s" from %s:%s' %
                      (data.decode('utf-8'), addr[0], addr[1]))

        except ConnectionResetError:
            print('Someone left unexcepted .')


if __name__ == '__main__':
    main()
