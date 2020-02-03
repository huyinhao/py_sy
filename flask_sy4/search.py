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
#  <胡崟昊> 改成自己的名字


import re
import warnings
from datetime import datetime
from urllib.request import *
from pypinyin import *

warnings.filterwarnings('ignore')  # 忽视一切告警

# 日期，最高温度，最低温度
dates, highs, lows, temperature = [], [], [], []


# 获取'http://lishi.tianqi.com/'的响应
def get_html(city, year, month):
    url = 'http://lishi.tianqi.com/' + city + '/' + str(year) + str(month) + '.html'
    print(url)
    request = Request(url)
    request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64)'
                       + 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36')
    response = urlopen(request)
    # 获取服务器请求
    return response.read().decode('utf-8')


# 获取天气
def get_date(city, year, months):
    for month in months:
        html = get_html(city, year, month)
        text = "".join(html.split())  # 拼接html响应
        print('month ' + month)

        # 获取天气正则表达式（1）
        patten_ul = re.compile('<ulclass="lishitable_contentclearfix">(.*?)</ul>')
        table = re.findall(patten_ul, text)

        # 获取天气正则表达式（2）
        patten2 = re.compile('.html">(.*?);">')
        uls = re.findall(patten2, table[0])

        for ul in uls:
            # 获取天气正则表达式（3）
            patten3 = re.compile('(.*?)</a>')
            date_list = re.findall(patten3, ul)
            # 日期list转为str
            d_time = ''.join(date_list)
            date = datetime.strptime(d_time, '%Y-%m-%d')

            # 获取天气正则表达式（4）
            patten4 = re.compile('</div><divstyle="width:100px">(.*?)</div><divstyle="width')
            temperature_list = re.findall(patten4, ul)

            # 获取天气正则表达式（5）
            patten5 = re.compile('(.*?)</div><div>')
            temperature_str = re.findall(patten5, temperature_list[0])

            try:
                high = int(temperature_str[0])  # 最高温度
                low = int(temperature_str[1])  # 最低温度
            except ValueError:
                print(date, '日期数据出现错误')
            else:
                dates.append(date)

                temperature.append([high, low])
                print(temperature)
    return temperature


def get_city_pinyin(city):
    lazy_city = lazy_pinyin(city)
    city_str = ''
    for c in lazy_city:
        city_str += c
    return city_str



