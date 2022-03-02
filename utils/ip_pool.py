import requests
from lxml import etree


def ipPool():
    list = []  # 存放能用的ip
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9"
    }

    url = 'https://www.kuaidaili.com/free/'

    for page in range(1,10):
        response = requests.get(f'https://www.kuaidaili.com/free/inha/{page}/',headers=headers)
        ip_list = etree.HTML(response.text).xpath('//tbody/tr/td[1]/text()')
        address_list = etree.HTML(response.text).xpath('//tbody/tr/td[2]/text()')
        for ip,adr in zip(ip_list,address_list):
            try:
                ips = ip.strip()
                adrs = adr.strip()
                ip_address = ips+':'+adrs
                proxies = {
                    'http': ip_address,
                    'https': ip_address,
                }
                #检测ip是否可用
                response2 = requests.get('https://www.baidu.com/', proxies=proxies, headers=headers, timeout=5)
                if response2.status_code == 200:
                    list.append(ip_address)
            except:
                pass
            else:
                print(ip_address, '这个IP通过了')
    print(list)
    return list
