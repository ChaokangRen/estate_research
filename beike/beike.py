# 利用BeautifulSoup抓取二手房成交数据

import time
import json
import requests
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


def get_one_page(url):
    try:
        # headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        # }
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.9 Safari/537.36',
            'Cookie': "mediav=%7B%22eid%22%3A%22202234%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22SZ8'vveaCF8%5E%5E9%5ELV8mI%22%2C%22ctn%22%3A%22%22%2C%22vvid%22%3A%22SZ8'vveaCF8%5E%5E9%5ELV8mI%22%2C%22_mvnf%22%3A1%2C%22_mvctn%22%3A0%2C%22_mvck%22%3A0%2C%22_refnf%22%3A1%7D; lianjia_uuid=53133861-997c-48bc-94f9-242b2bba5587; ke_uuid=a50a7e3d87e55ec078e35a4deb393714; _ga=GA1.2.526223651.1671766725; __xsptplus788=788.1.1671784632.1671784632.1%234%7C%7C%7C%7C%7C%23%233OxgY2RsROH1CW0GfqtU5Lbvp_CNPCJN%23; hy_data_2020_id=18852a407ef122-0d654e8ff9d5e7-162d1e0a-2073600-18852a407f015b3; hy_data_2020_js_sdk=%7B%22distinct_id%22%3A%2218852a407ef122-0d654e8ff9d5e7-162d1e0a-2073600-18852a407f015b3%22%2C%22site_id%22%3A341%2C%22user_company%22%3A236%2C%22props%22%3A%7B%7D%2C%22device_id%22%3A%2218852a407ef122-0d654e8ff9d5e7-162d1e0a-2073600-18852a407f015b3%22%7D; crosSdkDT2019DeviceId=11veq8-u6qdpx-g35o0753cjf6jvz-nxyn3ur27; beikeBaseData=%7B%22parentSceneId%22%3A%22%22%7D; lianjia_ssid=4dc56ee5-51ac-49ce-9abf-ffc8d189a9b6; Qs_lvt_200116=1671703910%2C1671766816%2C1671784624%2C1685013698%2C1700032914; Hm_lvt_9152f8221cb6243a53c83b956842be8a=1700032915; mediav=%7B%22eid%22%3A%22202234%22%2C%22ep%22%3A%22%22%2C%22vid%22%3A%22SZ8'vveaCF8%5E%5E9%5ELV8mI%22%2C%22ctn%22%3A%22%22%2C%22vvid%22%3A%22SZ8'vveaCF8%5E%5E9%5ELV8mI%22%2C%22_mvnf%22%3A1%2C%22_mvctn%22%3A0%2C%22_mvck%22%3A0%2C%22_refnf%22%3A0%7D; lianjia_token=2.00100e9e266d6c554901a3b717bc6809c6; lianjia_token_secure=2.00100e9e266d6c554901a3b717bc6809c6; security_ticket=AZbNyaTOFYSHrGWdD52PddzDBI3fOX6i4qtwstO8mt1p+nEJxX6KLDXHAEuAeCoGRD3EFzDKf4z4/PCMAJ3dcO1aqYpt+lrRNQl9l/PEz/HNENJQuDogP2XoU0Smze/PdKH3QGUtzZnIBRkZvJh1putBQldBSf5vHI6csouoILw=; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218505f9f21915d-0a130d965b139-162d1e0a-2073600-18505f9f21a19aa%22%2C%22%24device_id%22%3A%2218505f9f21915d-0a130d965b139-162d1e0a-2073600-18505f9f21a19aa%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; select_city=320100; Qs_pv_200116=3218207330410513000%2C917918460158528500%2C5812362059101024%2C4552284400253276700%2C2712511335684797000; Hm_lpvt_9152f8221cb6243a53c83b956842be8a=1700034018; srcid=eyJ0Ijoie1wiZGF0YVwiOlwiMWViNjc3YjQ2MmIzNDBhMWZhM2RlZDIyY2NmZjk4NTVjMWQ1MzIzNDIxZDhlZmEwZjVlNDNmZjhkYjkwNzIwMmZhNmFhOWYwOGExMmExN2E4NzI3N2MzYzQ4ZGFjNjNhOTY4NjRhNWQ5OTk0ZDMyMzM0ZGJmNjk1M2MwMTVhYTg4NzIzYTU2OWY1MzQ0ZWMxZDVjNTNmMDFhOTBiZTE0ODI1ZDUyYjRkYjhiZjg4YTE3NGJjZjU3YjkyMWI5Njk1YWUyYmMwNWRmMmJhYWU1ODhkMWQ5Y2M4YjVjOWNjYzhkYzEzM2ZiZmJhNjFiMjI2YjkzY2I4YmVhZGRmZjA2MFwiLFwia2V5X2lkXCI6XCIxXCIsXCJzaWduXCI6XCJjNjQ1ZDk3OFwifSIsInIiOiJodHRwczovL25qLmtlLmNvbS9jaGVuZ2ppYW8vIiwib3MiOiJ3ZWIiLCJ2IjoiMC4xIn0="}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_two_page(html):
    soup = BeautifulSoup(html, 'lxml')

    items = soup.find_all(attrs={'class': 'img CLICKDATA maidian-detail'})
    items1 = soup.find_all(attrs={'class': 'CLICKDATA maidian-detail'})
    items2 = soup.find_all(attrs={'class': 'houseInfo'})
    items3 = soup.find_all(attrs={'class': 'positionInfo'})
    items4 = soup.find_all(attrs={'class': 'totalPrice'})
    items5 = soup.find_all(attrs={'class': 'unitPrice'})
    items6 = soup.find_all(attrs={'class': 'dealCycleTxt'})
    items7 = soup.find_all(attrs={'class': 'dealDate'})

    i = 0
    for item in items:
        yield {
            'title': items1[i].text.strip(),  # 标题
            'totalPrice': items4[i].span.text + '万',  # 总价
            'unitPrice': items5[i].span.text + '元/平米',  # 单价
            'dealDate': items7[i].text.strip(),  # 房源成交时间
            'dealPrice': items6[i].span.text,  # 挂牌价
            'dealTime': parse_chengjiao(items6, i),  # 成交周期
            'href': item.attrs['href'],  # 跳转链接
            'image': item.img['data-original'],  # 图片
            # 房源描述
            'houseInfo': items2[i].text.strip() + items3[i].text.strip(),
        }
        i += 1


def parse_chengjiao(items6, i):
    guaTime = ''
    for item in items6[i]:
        strDf = str(item)
        if (strDf.find('成交周期', 0, len(strDf)) > -1):
            guaTime = strDf[6:len(strDf) - 7]
    return guaTime


def write_to_file(content):
    with open('data/deal.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')


def startGetData(page, *district):
    url = 'https://nj.ke.com/chengjiao/'

    addrParam = ''
    for param in district:
        addrParam = str(param)
    if (len(addrParam) > 0):
        url = url + addrParam + '/pg'
    else:
        url = url + 'pg'

    for i in range(page):
        param = url + str(i + 1) + '/'
        html = get_one_page(param)
        for item in parse_two_page(html):
            write_to_file(item)
        time.sleep(1)


if __name__ == '__main__':
    # 抓取数据 参数一：总页数，参数二：区县，可选、不传默认全部
    startGetData(92, 'xianlin2')
    a = 1
