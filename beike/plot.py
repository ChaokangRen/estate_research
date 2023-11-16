import re
from matplotlib import pyplot as plt


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


ymd = "2023.10.30"
with open('deal.txt') as lines:  # 一次性读入txt文件，并把内容放在变量lines中
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
            if(tiny[i+1] == ymd):
                digits.append(t)
            else:
                t = t+1.0
                digits.append(t)
                ymd = tiny[i+1]
        else:
            digit = re.findall(r"\d+\.?\d*", strs)[0]
            digits.append(float(digit))
    if name in deal_dict:
        deal_dict[name].append(digits)
    else:
        deal_dict[name] = [digits]


data = deal_dict["金地湖城艺境"]

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

price = fliter(price)
day.reverse()
plt.plot(day, price)
plt.show()
