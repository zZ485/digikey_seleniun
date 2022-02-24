import time
import re

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from Final.SendMail import sendMails


class DigiKeySpider:

    sleepTime = 5
    links = []
    goodList = []
    pageNum = []
    numbers = 500
    driver = None

    def __init__(self):
        # 不打开浏览器模式
        # option = webdriver.ChromeOptions()
        # option.add_argument('headless')
        # self.driver = webdriver.Chrome(options=option)
        self.driver = webdriver.Chrome()

    def getSource(self):
        # 获取商品列表
        with open('GoodList.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                self.goodList.append(line.strip('\n'))  # 剪切 ’\n‘
            f.close()

    def getLinks(self):
        for goodName in self.goodList:
            self.driver.get('https://www.digikey.cn')
            self.driver.find_element(By.CSS_SELECTOR,
                                '#header > div.header__top > div.header__search > div > div.searchbox-inner > '
                                'div.searchbox-inner-searchtext > input').send_keys(goodName)
            self.driver.find_element(By.CSS_SELECTOR, '#header-search-button').click()
            labels = self.driver.find_elements(By.CSS_SELECTOR,
                                          '#__next > main > div > div > div > '
                                          'div.MuiGrid-root.jss10.MuiGrid-item.MuiGrid-grid-md-9 > div.jss121.jss15 > '
                                          'div.jss120 > div > div > table > tbody > tr')
            time.sleep(self.sleepTime)
            for label in labels:
                title = label.find_element(By.CSS_SELECTOR, 'td:nth-child(2) > span').text
                link = label.find_element(By.CSS_SELECTOR,
                                          '#__next > main > div > div > div > '
                                          'div.MuiGrid-root.jss10.MuiGrid-item.MuiGrid-grid-md-9 > div.jss121.jss15 > '
                                          'div.jss120 > div > div > table > tbody > tr > td:nth-child(1) > span > '
                                          'a').get_attribute('href')
                if title == '集成电路（IC）':
                    self.links.append(link)
            time.sleep(self.sleepTime)

    def catchData(self):

        self.getSource()

        self.getLinks()

        while True:
            try:
                for a in self.links:
                    self.driver.get(a)

                    try:
                        button = self.driver.find_element(By.CSS_SELECTOR,
                                                     '#__next > main > section > div > section >div.MuiGrid-root.MuiGrid-container.MuiGrid-direction-xs-column >div.MuiGrid-root.MuiGrid-container.MuiGrid-item > div >div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-2.MuiGrid-item >div:nth-child(1) > div.jss105 > fieldset > div > label:nth-child(1) > span.MuiButtonBase-root.MuiIconButton-root.jss22.MuiCheckbox-root.jss122.MuiCheckbox-colorSecondary.MuiIconButton-colorSecondary > span > input')
                        button.click()
                        time.sleep(5)
                        leftNum = self.driver.find_element(By.CSS_SELECTOR, '#__next > main > section > div > section > div.MuiGrid-root.MuiGrid-container.MuiGrid-direction-xs-column > div.MuiGrid-root.jss53.MuiGrid-container.MuiGrid-spacing-xs-2.MuiGrid-align-items-xs-center > div:nth-child(2) > span > div > span').text
                        if leftNum == '0':
                            break
                        self.driver.find_element(By.CSS_SELECTOR,
                                            '#__next > main > section > div > section > '
                                            'div.MuiGrid-root.MuiGrid-container.MuiGrid-direction-xs-column > '
                                            'div.MuiGrid-root.jss53.MuiGrid-container.MuiGrid-spacing-xs-2.MuiGrid-align-items-xs'
                                            '-center > div:nth-child(1) > button').click()
                    except NoSuchElementException as e:
                        print(e)
                        break

                    time.sleep(self.sleepTime)

                    print(a)
                    nums = self.driver.find_element(By.CSS_SELECTOR,
                                               '#__next > main > section > div > div.jss49 > div > div:nth-child(3) > div > '
                                               'div:nth-child(1) > div > div:nth-child(1) > div > div:nth-child(2) > span').text
                    pageNum = re.findall("\d+\.?\d*", nums)
                    pageNum = list(map(int, pageNum))
                    print(pageNum[1])

                    time.sleep(self.sleepTime)
                    for i in range(0, pageNum[1]):
                        time.sleep(self.sleepTime)

                        lis = self.driver.find_elements(By.CSS_SELECTOR, '#data-table-0 > tbody > tr')

                        # 对每页每条商品信息遍历
                        for li in lis:
                            # 获取商品名title
                            title = li.find_element(By.CSS_SELECTOR,
                                                    'td:nth-child(2) > div > div.MuiGrid-root > div > a').text

                            # 获取商品库存qty
                            qtyAvailable = li.find_element(By.CSS_SELECTOR, 'td:nth-child(4) > span > div').text
                            qtyAvailable = qtyAvailable.replace(',', '')
                            qty = re.findall("\d+\.?\d*", qtyAvailable)
                            qty = list(map(int, qty))

                            # # 发送邮件
                            if max(qty) > self.numbers:
                                print('商品名：' + title + ' 达到预定库存数！')
                                sendMails.send_mails(title=title, qty=qty, platform= 'DigiKey')

                            print('商品名称：' + title + '\t剩余库存' + str(qty))

                        if pageNum[1] == 1:
                            break

                            buttons = self.driver.find_elements(By.CSS_SELECTOR,
                                                           '#__next > main > section > div > div > div > div > div > div .MuiIconButton-root')
                            button = buttons[0]
                            button.send_keys('\n')
            except Exception as e:
                print(e)
