import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()
# driver.get('https://www.digikey.cn/zh/products/filter/%E5%B5%8C%E5%85%A5%E5%BC%8F-%E5%BE%AE%E6%8E%A7%E5%88%B6%E5%99%A8/685?amp%3BWT.z_header=search_go&s=N4IgTCBcDaIMoBUCyBmMAxEBdAvkA')
# driver.find_element(By.CSS_SELECTOR, '#__next > main > section > div > section > '
#                                              'div.MuiGrid-root.MuiGrid-container.MuiGrid-direction-xs-column > '
#                                              'div.MuiGrid-root.MuiGrid-container.MuiGrid-item > div > '
#                                              'div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-2.MuiGrid-item > '
#                                              'div:nth-child(1) > div.jss105 > fieldset > div > label:nth-child(1) > '
#                                              'span.MuiButtonBase-root.MuiIconButton-root.jss22.MuiCheckbox-root.jss122.MuiCheckbox-colorSecondary.MuiIconButton-colorSecondary > span > input') .click()
# time.sleep(3)
#
# driver.find_element(By.CSS_SELECTOR,
#                     '#__next > main > section > div > section > '
#                     'div.MuiGrid-root.MuiGrid-container.MuiGrid-direction-xs-column > '
#                     'div.MuiGrid-root.jss53.MuiGrid-container.MuiGrid-spacing-xs-2.MuiGrid-align-items-xs'
#                     '-center > div:nth-child(1) > button').click()
#
# time.sleep(5)
# ase = driver.find_element(By.CSS_SELECTOR, '#__next > main > section > div > div.jss49 > div > div:nth-child(3) > div > '
#                                     'div:nth-child(1) > div > div:nth-child(1) > div > div:nth-child(2) > span').text
# a = re.findall("\d+\.?\d*", ase)
# a = list(map(int, a))
# print(a[1])
# time.sleep(3)
# s = driver.find_element(By.CSS_SELECTOR, '#__next > main > section > div > section > div.MuiGrid-root.MuiGrid-container.MuiGrid-direction-xs-column > div.MuiGrid-root.jss53.MuiGrid-container.MuiGrid-spacing-xs-2.MuiGrid-align-items-xs-center > div:nth-child(2) > span > div > span').text
# print(s)
driver.get('https://www.digikey.cn/zh/products/filter/%E5%B5%8C%E5%85%A5%E5%BC%8F-%E5%BE%AE%E6%8E%A7%E5%88%B6%E5%99%A8/685?amp%3BWT.z_header=search_go&s=N4IgTCBcDaIM4BcC2BmCBdAvkA')

lis = driver.find_elements(By.CSS_SELECTOR, '#data-table-0 > tbody > tr')
for li in lis:
    title = li.find_element(By.CSS_SELECTOR, 'td:nth-child(2) > div > div.MuiGrid-root > div > a').text
    qtyAvailable = li.find_element(By.CSS_SELECTOR, 'td:nth-child(4) > span > div').text
    qty = re.findall("\d+\.?\d*", qtyAvailable)
    qty = list(map(int, qty))
    print('商品名称：' + title + '\t剩余库存' + str(qty))
buttons = driver.find_elements(By.CSS_SELECTOR, '#__next > main > section > div > div > div > div > div > div .MuiIconButton-root')
button = buttons[0]
button.send_keys('\n')
