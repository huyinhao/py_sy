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

import json
import random
import socket
import threading

socket_list = []
history = []  # 历史记录
coin = 30  # 初始钱币


def service_client(new_socket):
    def sendto_client(play_er):
        # 字典类型直接写入json会报错，先将字典转换成字符串
        new_socket.send(json.dumps(play_er).encode('utf-8'))

    # 接收请求
    while True:
        recv_data = new_socket.recv(1024).decode('utf-8')
        data = json.loads(recv_data)  # 读取数据，将字符串转换为字典
        print(data)
        dice1, dice2 = random.randint(1, 6), random.randint(1, 6)
        # 新开盘
        if data['function'] == '游戏开始':
            player_name = len(history)
            # 转头彩
            player = {'player_name': player_name, 'coin': coin, 'dice1': dice1, 'dice2': dice2}
            history.append({'player_name': player_name, 'money': coin, 'dice1': dice1, 'dice2': dice2})
            sendto_client(player)
        # 下注中
        elif data['function'] == '押注':
            # 押中了
            bet = True
            # 头彩
            if data['type'] == 'tc' and dice1 == data['dice1'] and dice2 == data['dice2']:
                history[data['player_name']]['money'] += data['money'] * 35
            # 大彩
            elif data['type'] == 'dc' and ((dice1 == data['dice1'] and dice2 == data['dice2']) or (
                    dice1 == data['dice2'] and dice2 == data['dice1'])):
                history[data['player_name']]['money'] += data['money'] * 17
            # 空盘
            elif data['type'] == 'kp' and (dice1 != dice2 and dice1 % 2 == 0 and dice2 % 2 == 0):
                history[data['player_name']]['money'] += data['money'] * 5
            # 七星
            elif data['type'] == 'qx' and dice1 + dice2 == 7:
                history[data['player_name']]['money'] += data['money'] * 5
            # 单对
            elif data['type'] == 'dd' and dice1 % 2 == 1 and dice2 % 2 == 1:
                history[data['player_name']]['money'] += data['money'] * 3
            # 散星
            elif data['type'] == 'sx' and dice1 + dice2 in [3, 5, 9, 11]:
                history[data['player_name']]['money'] += data['money'] * 2
            # 没压中
            else:
                history[data['player_name']]['money'] -= data['money']
                bet = False
            sendto_client({'dice1': dice1, 'dice2': dice2, 'bet': bet})
        # 玩家退出
        elif data['function'] == 'exit':
            print('%s号玩家已经倾家荡产了' % data['player_name'])
        else:
            print('信息有误！出错内容：%s')


def server_send(sock, play_er):
    # 字典类型直接写入json会报错，先将字典转换成字符串
    sock.send(json.dumps(play_er).encode('utf-8'))


def server_read(sock):
    try:
        while True:
            message = sock.recv(1024).decode('utf-8')
            data = json.loads(message)  # 读取数据，将字符串转换为字典
            print(data)
            dice1, dice2 = random.randint(1, 6), random.randint(1, 6)
            # 新开盘
            if data['function'] == '游戏开始':
                player_name = len(history)
                # 转头彩
                player = {'player_name': player_name, 'coin': coin, 'dice1': dice1, 'dice2': dice2}
                history.append({'player_name': player_name, 'money': coin, 'dice1': dice1, 'dice2': dice2})
                server_send(sock, player)
            # 下注中
            elif data['function'] == '押注':
                # 押中了
                bet = True
                # 头彩
                if data['type'] == 'tc' and dice1 == data['dice1'] and dice2 == data['dice2']:
                    history[data['player_name']]['money'] += data['money'] * 35
                # 大彩
                elif data['type'] == 'dc' and ((dice1 == data['dice1'] and dice2 == data['dice2']) or (
                        dice1 == data['dice2'] and dice2 == data['dice1'])):
                    history[data['player_name']]['money'] += data['money'] * 17
                # 空盘
                elif data['type'] == 'kp' and (dice1 != dice2 and dice1 % 2 == 0 and dice2 % 2 == 0):
                    history[data['player_name']]['money'] += data['money'] * 5
                # 七星
                elif data['type'] == 'qx' and dice1 + dice2 == 7:
                    history[data['player_name']]['money'] += data['money'] * 5
                # 单对
                elif data['type'] == 'dd' and dice1 % 2 == 1 and dice2 % 2 == 1:
                    history[data['player_name']]['money'] += data['money'] * 3
                # 散星
                elif data['type'] == 'sx' and dice1 + dice2 in [3, 5, 9, 11]:
                    history[data['player_name']]['money'] += data['money'] * 2
                # 没压中
                else:
                    history[data['player_name']]['money'] -= data['money']
                    bet = False
                print({'dice1': dice1, 'dice2': dice2, 'bet': bet})
                server_send(sock, {'dice1': dice1, 'dice2': dice2, 'bet': bet})
                # 玩家退出
            elif data['function'] == 'exit':
                print('%s号玩家已经倾家荡产了' % data['player_name'])
            else:
                print('信息有误！出错内容：%s')
    except:
        print('玩家退出了')


def main():
    sever_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建套接字
    sever_socket.bind(('127.0.0.1', 6666))  # 绑定端口
    sever_socket.listen(128)  # 准备监听

    while True:
        client_socket, client_addr = sever_socket.accept()  # 返回客户端socket和地址
        socket_list.append(client_socket)
        threading.Thread(target=server_read, args=(client_socket,)).start()
        threading.Thread(target=server_send, args=(client_socket, {})).start()


if __name__ == '__main__':
    main()
