import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from Final.SendMail import sendMails


class ArrowSpider:
    driver = None
    goodList = []
    links = []
    numbers = 500
    sleeptime = 20

    def __init__(self):
        self.driver = webdriver.Chrome()

    def getSource(self):
        # 获取商品列表
        with open('GoodList.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                self.goodList.append(line.strip('\n'))  # 剪切 ’\n‘
            f.close()

    def getLinks(self):
        for goodName in self.goodList:
            url1 = 'https://www.arrow.com/en/products/search?&q=' + goodName + '&sortBy=calculatedQuantity&sortDirection=desc'
            self.links.append(url1)
        print(self.links)

    def catchData(self):
        self.getSource()

        self.getLinks()

        while True:

            for link in self.links:

                self.driver.set_page_load_timeout(10)
                self.driver.set_script_timeout(10)
                try:
                    time.sleep(self.sleeptime)
                    self.driver.get(link)
                    time.sleep(self.sleeptime)
                except:
                    self.driver.execute_script('window.stop()')
                    try:
                        lis = self.driver.find_elements(By.CSS_SELECTOR, '#searchListView > tbody')

                        for li in lis:
                            self.driver.implicitly_wait(3)

                            title = li.find_element(By.CSS_SELECTOR,
                                                    'td.SearchResults-column.SearchResults-column--name > a > span.SearchResults-productName > span:nth-child(1)').text

                            self.driver.implicitly_wait(3)

                            qty = li.find_element(By.CSS_SELECTOR,
                                                  'td.SearchResults-column.SearchResults-column--stock > div.SearchResults-stock-container > span.SearchResults-stock').text
                            qty = int(qty)

                            if qty > self.numbers:
                                print('商品名：' + title + ' 达到预定库存数！')
                                sendMails.send_mails(title=title, qty=qty, platform='Arrow')
                        print('商品名称：' + title + '\t剩余库存' + str(qty))


                    except Exception as e:
                        print(e)
                        break


test = ArrowSpider()
test.catchData()
