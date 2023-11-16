import re
from matplotlib import pyplot as plt
import datetime
import numpy as np
newest_day = datetime.datetime(2023, 10, 31)


def fliter(datas):
    size = 3
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


with open('data/qilinkechuangyuan.txt') as lines:  # 一次性读入txt文件，并把内容放在变量lines中
    array = lines.readlines()  # 返回的是一个列表，该列表每一个元素是txt文件的每一行

t = 0
deal_dict = {}
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
            delta = newest_day - day
            digits.append(delta.days)
        else:
            digit_list = re.findall(r"\d+\.?\d*", strs)
            digit = "0"
            if digit_list != []:
                digit = digit_list[0]
            digits.append(float(digit))
    if name in deal_dict:
        deal_dict[name].append(digits)
    else:
        deal_dict[name] = [digits]

    t += 1
    # if(t > 2):
    #     break
data = deal_dict["中海国际社区一期"]
print(len(data))
price = []
day = []
sqr = []
for ite in data:
    sqr = ite[0]
    if(sqr > 85 and sqr < 100):
        price.append(ite[2])
        day.append(ite[3])
    # price.append(ite[2])
    # day.append(ite[3])
last_day = day[-1]
print(last_day)
days = []
for ite in day:
    dd = - ite + last_day
    days.append(dd)

# price = fliter(price)
# day.reverse()
plt.plot(days, price)

half_year = 182.5
num1 = 2020
num2 = 1
for i in range(6):
    if(i % 2 == 0):
        num1 += 1
        num2 = 1
    else:
        num2 = 7
    note = str(num1) + ".0" + str(num2)
    plt.axvline(half_year * i - 31, color='r', linestyle=':')
    plt.text(half_year * i - 31, 24000, note, fontdict={
        'family': 'serif', 'size': 16, 'color': 'blue'}, ha='center', va='center')
plt.show()
