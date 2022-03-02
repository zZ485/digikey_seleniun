import time

from selenium import webdriver
from selenium.webdriver.common.by import By

goodList = []
links = []
driver = webdriver.Chrome()

# 获取商品列表
with open('../GoodList.txt', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        goodList.append(line.strip('\n'))  # 剪切 ’\n‘
    f.close()

# for goodName in goodList:
#     driver.get('https://www.digikey.cn')
#     # 找到搜索栏并输入芯片名
#     driver.find_element(By.CSS_SELECTOR,
#                              '#header > div.header__top > div.header__search > div > div.searchbox-inner > '
#                              'div.searchbox-inner-searchtext > input').send_keys(goodName)
#
#     # 点击搜索栏旁的搜索按钮
#     driver.find_element(By.CSS_SELECTOR, '#header-search-button').click()
#
#     # 获取商品分类的标签列表
#     labels = driver.find_elements(By.CSS_SELECTOR,
#                                        '#__next > main > div > div > div > '
#                                        'div.MuiGrid-root.jss10.MuiGrid-item.MuiGrid-grid-md-9 > div.jss121.jss15 > '
#                                        'div.jss120 > div > div > table > tbody > tr')
#     time.sleep(5)
#
#     # 对标签列表轮询，获取标签中可点击链接
#     for label in labels:
#         title = label.find_element(By.CSS_SELECTOR, 'td:nth-child(2) > span').text
#         link = label.find_element(By.CSS_SELECTOR,
#                                   '#__next > main > div > div > div > '
#                                   'div.MuiGrid-root.jss10.MuiGrid-item.MuiGrid-grid-md-9 > div.jss121.jss15 > '
#                                   'div.jss120 > div > div > table > tbody > tr > td:nth-child(1) > span > '
#                                   'a').get_attribute('href')
#         # 判断标签后缀是否为”集成电路（IC）“，将链接放入待访问链接列表
#         if title == '集成电路（IC）':
#             links.append(link)
#     time.sleep(5)
#
# with open('../DigiKeyLinks.txt', 'w', encoding='utf-8') as f:
#     f.writelines(links)
#     f.close()

for goodName in goodList:
    url = 'https://www.arrow.com/en/products/search?&q=' + goodName + '&cat=&r=true'
    driver.get(url)
    time.sleep(10)
    try:
        driver.find_element(By.CSS_SELECTOR, '#productControlsView > h1')
    except Exception as e:
        print(goodName, e)
        continue
