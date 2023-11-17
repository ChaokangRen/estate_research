import re
from matplotlib import pyplot as plt
import datetime
import numpy as np
newest_day = datetime.datetime(2023, 10, 31)


def fliter(datas):
    size = 5
    half_size = round(size/2)
    lens = len(datas)
    data_meaning = []
    for i in range(lens):
        arverage = 0.0
        if i < half_size:
            for j in range(size):
                arverage += datas[i + j]
        elif i > lens - half_size-1:
            for j in range(size):
                arverage += datas[i + j-size]
        else:
            for j in range(size):
                arverage += datas[i + j - half_size]
        arverage /= size
        data_meaning.append(arverage)
    return data_meaning


def get_dict(plate_name):
    with open(plate_name) as lines:  # 一次性读入txt文件，并把内容放在变量lines中
        array = lines.readlines()  # 返回的是一个列表，该列表每一个元素是txt文件的每一行
    t = 0
    plate_dict = {}
    for ite in array:
        tiny = ite.split(',')
        msg = tiny[0].split(':')[1]
        name = msg.split(' ')[1]
        name = name.split('"')[1]
        sqr = msg.split(' ')[3]
        sqr_digit = float(re.findall(r"\d+\.?\d*", sqr)[0])
        digits = [sqr_digit]
        for i in range(5):
            strs = tiny[i+1]
            if(i == 2):
                ymd = strs.split('"')[3].split('.')
                day = datetime.datetime(int(ymd[0]), int(ymd[1]), int(ymd[2]))
                # delta = newest_day - day
                # digits.append(delta.days)
                digits.append(day)
            else:
                digit_list = re.findall(r"\d+\.?\d*", strs)
                digit = "0"
                if digit_list != []:
                    digit = digit_list[0]
                digits.append(float(digit))
        if name in plate_dict:
            plate_dict[name].append(digits)
        else:
            plate_dict[name] = [digits]

        t += 1

        # if(t > 2):
        #     break
    return plate_dict


def plot_community_price(plate_dict, community_name):
    data = plate_dict[community_name]

    price = []
    days = []
    sqr = []
    for ite in data:
        sqr = ite[0]
        if(sqr > 75 and sqr < 115):
            price.append(ite[2])
            days.append(ite[3])

        # price.append(ite[2])
        # days.append(ite[3])

    day_len = len(days)
    day_list = []
    for i in range(day_len):
        if i == 0:
            day_list.append(0)
        else:
            delta = (days[i] - days[0]).days
            day_list.append(delta)
    add_day = -day_list[-1]
    print(add_day)
    for i in range(day_len):
        day_list[i] += add_day

    year = days[-1].year
    mon = days[-1].month
    n_year = days[0].year
    n_mon = days[0].month
    # print(year, mon)
    # print(n_year, n_mon)
    # print((data[0][3] - data[-1][3]).days)

    note_list = []

    ite_year = year
    while ite_year <= n_year:
        gap_day = (datetime.datetime(ite_year, 1, 1) - days[-1]).days
        gap_str = str(ite_year % 100) + '.1'
        note_list.append([gap_day, gap_str])
        gap_day = (datetime.datetime(ite_year, 7, 1) - days[-1]).days
        gap_str = str(ite_year % 100) + '.7'
        note_list.append([gap_day, gap_str])
        ite_year += 1
    print(note_list)
    price = fliter(price)
    plt.plot(day_list, price)

    level = min(price)
    for note in note_list:
        plt.axvline(note[0], color='r', linestyle=':')
        plt.text(note[0], level, note[1], fontdict={
            'family': 'serif', 'size': 16, 'color': 'blue'}, ha='center', va='center')
        mon += 6
        if mon > 12:
            mon -= 12
            year += 1
        i += 1
    plt.show()


if __name__ == '__main__':
    # 抓取数据 参数一：总页数，参数二：区县，可选、不传默认全部
    plate_name = 'data/qilinkechuangyuan.txt'
    # plate_name = 'data/wanshou1.txt'
    plate_dict = get_dict(plate_name)
    community_name = "富力城"
    plot_community_price(plate_dict, community_name)
