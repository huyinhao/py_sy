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


from flask import Flask, request, render_template
from search import *
app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    # 2011-2018月份
    month_s = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    # 2019月份
    month_2019 = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11']

    city = request.form['city']
    year = request.form['year']

    if int(year) == 2019:
        months = month_2019
    else:
        months = month_s
    # months = ['01']
    city_pinyin = get_city_pinyin(city)
    print(type(city_pinyin))
    temperature_list = get_date(city_pinyin, year, months)  # 日期，最高温度，最低温度
    # temperature_list = [[3, 2], [2, 1], [5, 5], [9, 6],
    #                     [8, 6], [8, 6], [7, 5], [7, 5],
    #                     [5, 5], [7, 6], [9, 6], [8, 5],
    #                     [8, 4], [6, 5], [7, 3], [4, 0],
    #                     [9, 0], [14, 4], [17, 8], [10, 2],
    #                     [8, 2], [12, 1], [14, 2], [16, 1],
    #                     [11, 3], [9, 0], [13, 3], [12, 6],
    #                     [15 6], [21, 7], [10, 3]]

    # encoding=utf-8
    return render_template('search.html', list=temperature_list, city=city, year1=str(year), year2=int(year))


if __name__ == '__main__':
    app.run(debug=True)
