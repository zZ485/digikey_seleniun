import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from Final.SendMail import sendMails



class ArrowSpider:
    driver = None
    goodList = []
    links = []
    numbers = 500
    sleeptime = 20

    def read_config(self):
        with open("config.json") as json_file:
            config = json.load(json_file)
        return config

    def __init__(self):
        config = self.read_config()
        options = Options()
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
        options.add_argument('user-agent={0}'.format(user_agent))
        proxy = config['proxies']['http']
        options.add_argument('--proxy-server=http://' + proxy)
        self.driver = webdriver.Chrome(options=options)

    def getSource(self):
        # 获取商品列表
        with open('GoodList.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                self.goodList.append(line.strip('\n'))  # 剪切 ’\n‘
            f.close()

    def getLinks(self):
        for goodName in self.goodList:
            url1 = 'https://www.arrow.com/en/products/search?&q=' + goodName + '&cat=&r=true'
            self.links.append(url1)
        print(self.links)

    def catchData(self):
        self.getSource()

        self.getLinks()

        while True:

            for link in self.links:
                try:
                    self.driver.set_page_load_timeout(10)
                    self.driver.set_script_timeout(10)
                    # try:
                    time.sleep(self.sleeptime)
                    self.driver.get(link)
                    self.driver.delete_all_cookies()
                    time.sleep(self.sleeptime)
                    # except:
                    self.driver.execute_script('window.stop()')

                    try:
                        self.driver.find_element(By.XPATH, '/html/body/div[1]/div[11]/div[2]/div/div[3]/div/div[1]/table/thead/tr/th[3]').click()

                        time.sleep(self.sleeptime)

                        lis = self.driver.find_elements(By.XPATH, '/html/body/div[1]/div[11]/div[2]/div/div[3]/div/div[1]/table/tbody')

                        for li in lis:
                            self.driver.implicitly_wait(3)

                            title = li.find_element(By.XPATH, '/html/body/div[1]/div[11]/div[2]/div/div[3]/div/div[1]/table/tbody/tr/td[1]/a/span[1]/span[1]').text

                            self.driver.implicitly_wait(3)

                            qty = li.find_element(By.XPATH, '/html/body/div[1]/div[11]/div[2]/div/div[3]/div/div[1]/table/tbody/tr/td[3]/div[1]/span[1]').text
                            qty = qty.replace(',', '')
                            qty = int(qty)

                            if qty > self.numbers:
                                print('商品名：' + title + ' 达到预定库存数！')
                                sendMails.send_mails(title=title, qty=qty, platform='Arrow')
                            print('商品名称：' + title + '\t剩余库存' + str(qty))
                    except Exception as e:
                        print(e)
                        break

                except Exception as e:
                    print(e)
                    break

