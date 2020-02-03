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
import socket
import time

# 骰子
DICE = [
    '''
 _________
|         |
|         |
|    ●    |
|         |
|_________| 

''',
    '''
 _________
|         |
|         |
|  ●   ●  |
|         |
|_________|
 
 ''',
    '''
 _________
|         |
|     ●   |
|    ●    |
|   ●     |
|_________| 

''',
    '''
 _________
|         |
|  ●   ●  |
|         |
|  ●   ●  |
|_________|
 
 ''',
    '''
 _________
|         |
|  ●   ●  |
|    ●    |
|  ●   ●  |
|_________| 

''',
    '''
 _________
|         |
|  ●   ●  |
|  ●   ●  |
|  ●   ●  |
|_________| 

''',

]
cs_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = ('127.0.0.1', 6666)
message = {}
touzi = ['', '一', '二', '三', '四', '五', '六']


# 连接服务器
def start():
    print('▁▂▃▄▅▆▇█', '欢迎体验怎么压都不中的骰宝游戏', '█▇▆▅▄▃▂▁')
    print('♬♬♬♬♬♬♬ 输入服务器地址启动游戏 <RemoteBet IP_address>:')
    mes = input()
    addr = (mes[10:], 6666)
    if mes[:10].lower() == 'RemoteBet '.lower() and addr[0] == '127.0.0.1':

        print('连接服务器ing...')
        cs_socket.connect(addr)

    # addr=('127.0.0.1',6666)
    else:
        print('♬♬♬♬♬♬♬ 连接服务器失败，你输入的IP地址为: %s 请重新输入！' % addr[0])
        start()


# 传输数据
def client_send(player_message):
    coin_info = json.dumps(player_message).encode('utf-8')
    cs_socket.send(coin_info)


# 接受数据
def client_recv():
    recv_data = cs_socket.recv(1024).decode('utf-8')
    return json.loads(recv_data)


# 进入赌场
def inGame(message):
    print('☀'*8, '游戏开始', '☀'*8)
    show_coin()
    t_print('进入赌场，你走进了一张桌子......', 1)
    t_print('庄家唱道：新开盘！预叫头彩！', 2)
    t_print('庄家将两枚玉骰往银盘中一撒。', 1)
    t_print(DICE[int(message['dice1']) - 1], 1.5)
    t_print(DICE[int(message['dice2']) - 1], 1.5)
    t_print('庄家唱道：头彩骰号是%s、%s！' % (touzi[int(message['dice1'])], touzi[int(message['dice2'])]), 1)


# 帮助
def Help():
    # 帮助
    help_me = '''
===========================游戏帮助===========================
ya tc 数量  押头彩（两数顺序及点数均正确）             一赔三十五
ya dc 数量  押大彩（两数点数正确）                    一赔十七
ya kp 数量  押空盘（两数不同且均为偶数)               一赔五
ya qx 数量  押七星（两数之和为七）                    一赔五
ya dd 数量  押单对（两数均为奇数）                    一赔三
ya sx 数量  押散星（两数之和为三、五、九、十一)        一赔二
==============================================================
'''
    print(help_me)


# 显示当前财富
def show_coin():
    print('='*8, '当前coin:%d' % (message['coin']), '='*8)


# 间隔interval秒输出
def t_print(words, interval):
    print(words)
    time.sleep(interval)


# 下注
def Bet(command):
    print('='*8, '下注中...', '='*8, command)
    a, b, c = tuple(command.split(' '))
    assert b in ['tc', 'dc', 'kp', 'qx', 'dd', 'sx']  # 押注的规则不符合就报错,进入异常处理
    if not c.isdigit():  # 不为数字就抛出异常,进入异常处理
        raise ValueError
    if int(c) > message['coin']:  # 押注的数量超出余额
        print('你没有那么多 %s钱币!' % c)
        return -1

    message['money'] = int(c)
    message['function'] = '押注'
    message['type'] = b
    client_send(message)
    ret = client_recv()
    while ret == {}:
        ret = client_recv()
    d1, d2 = ret['dice1'], ret['dice2']
    if ret['bet']:
        if b == 'tc':
            message['coin'] += int(c) * 35
        elif b == 'dc':
            message['coin'] += int(c) * 17
        elif b == 'kp':
            message['coin'] += int(c) * 5
        elif b == 'qx':
            message['coin'] += int(c) * 5
        elif b == 'dd':
            message['coin'] += int(c) * 3
        elif b == 'sx':
            message['coin'] += int(c) * 2
    else:
        message['coin'] -= int(c)

    t_print('庄家将两枚玉骰扔进两个金盅，一手持一盅摇将起来。', 2)
    t_print('庄家将左手的金盅倒扣在银盘上，玉骰滚了出来。', 1)
    t_print(DICE[d1 - 1], 1.5)
    t_print('庄家将右手的金盅倒扣在银盘上，玉骰滚了出来。', 1)
    t_print(DICE[d2 - 1], 1.5)
    rs = '庄赢'
    if d1 + d2 in [3, 5, 9, 11]: rs = '散星'
    if d1 % 2 == 1 and d2 % 2 == 1: rs = '单对'
    if d1 + d2 == 7: rs = '七星'
    if d1 != d2 and d1 % 2 == 0 and d2 % 2 == 0: rs = '空盘'
    if (d1 == message['dice1'] and d2 == message['dice2']) or (
            d1 == message['dice2'] and d2 == message['dice1']): rs = '大彩'
    if d1 == message['dice1'] and d2 == message['dice2']: rs = '头彩'
    t_print('庄家叫道:%s、%s······%s。' % (touzi[d1], touzi[d2], rs), 1.5)
    if ret['bet']:
        t_print('庄家叫道：恭喜这位小哥，赢了%s！' % rs, 1)
    else:
        t_print('没压中，哎呀', 1)


def main():
    global addr, message
    start()
    
    message = {'function': '游戏开始'}
    client_send(message)
    message = client_recv()

    inGame(message)

    while True:
        print('输入你压的值')
        print('查看帮助：help')
        print('查看余额：s')
        print('查看历史记录：h')
        command = input().lower()

        if command.lower() == 'help':
            Help()

        # 查看余额
        elif command.lower() == 's':
            show_coin()

        # 查看上次下注记录
        elif command.lower() == 'h':
            print(message)

        # 下注
        elif command.split(' ')[0] == 'ya':
            try:
                Bet(command)
            except:
                print('输入有误！ 请重新输入！')
        if message['coin'] == 0:
            print('您已经倾家荡产了，下次再来 bye bye')
            message['function'] = 'exit'
            message['type'] = 'broken'
            client_send(message)
            client_recv()
            cs_socket.close()
            break


if __name__ == '__main__':
    main()
