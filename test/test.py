import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

sleepTime = 60  # 设置睡眠时间(秒)

driver = webdriver.Chrome()

# 获取商品页数
def get_page_num() -> []:
    nums = driver.find_element(By.CSS_SELECTOR, '#__next > main > section > div > div.jss49 > div > div:nth-child(3) > div > div:nth-child(1) > div > div:nth-child(1) > div > div:nth-child(2) > span').text
    pageNum = re.findall("\d+\.?\d*", nums)
    pageNum = list(map(int, pageNum))
    return pageNum


# 对每页遍历
def get_info_from_pages():
    lis = driver.find_elements(By.CSS_SELECTOR, '#data-table-0 > tbody .MuiTableRow-root')

    # 对每页每条商品信息遍历
    for li in lis:
        # 获取商品名title
        title = li.find_element(By.CSS_SELECTOR, '#data-table-0 > tbody .MuiTableRow-root td .jss303 a').text

        # 获取商品库存qty
        qtyAvailable = li.find_element(By.CSS_SELECTOR,
                                       '#data-table-0 > tbody > tr > td:nth-child(4) > span > div').text
        qty = re.findall("\d+\.?\d*", qtyAvailable)
        qty = list(map(int, qty))

        # 发送邮件
        # if qty[0] > 500:

        print('商品名称：' + title + '\t剩余库存' + str(qty))

    driver.find_elements(By.CSS_SELECTOR, '#__next > main > section > div > div.jss49 > div > div:nth-child(3) > div > div:nth-child(1) > div > div:nth-child(2) > div > button:nth-child(6)').click()


def get_info_from_items(pageNum):
    # 商品之间等待10秒
    driver.implicitly_wait(10)
    for i in range(1, pageNum[1]):
        time.sleep(1)
        get_info_from_pages()
