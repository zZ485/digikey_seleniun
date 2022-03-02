#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022-2-25
# @Author  : zZ485
# @Github  : https://github.com/zZ485
# @Software: DigiKey & Arrow Spider
# @File    : arrowSpider.py

import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from SendMail import sendMails


class ArrowSpider:
    driver = None
    goodList = []
    links = []
    sleeptime = 10

    def read_config(self):
        """
        读入config.json文件中的配置

        :param self: 对象自身
        :return: config字典
        """
        with open("config.json") as json_file:
            config = json.load(json_file)
        return config

    def __init__(self):
        config = self.read_config()
        options = Options()

        # 设置请求头
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
        options.add_argument('user-agent={0}'.format(user_agent))

        # 设置代理地址：1270.0.0.1：1080
        # proxy = config['proxies']['http']
        # options.add_argument('--proxy-server=http://' + proxy)
        self.driver = webdriver.Chrome(options=options)

    def getSource(self):
        """
        从GoodList.txt中按行读取所需要查找的芯片系列名，读入对象的goodLists列表中
        """
        # 获取商品列表
        with open('GoodList.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                self.goodList.append(line.strip('\n'))  # 剪切 ’\n‘
            f.close()

    def getLinks(self):
        """
        将得到的芯片系列号组合成用url，将合成后的url放入links成为待访问链接
        """
        for goodName in self.goodList:
            url = 'https://www.arrow.com/en/products/search?&q=' + goodName + '&cat=&r=true'
            self.links.append(url)

    def catchData(self):
        """
        Arrow.com平台爬虫本体
        """
        self.getSource()  # 获取芯片系列

        self.getLinks()  # 组合待爬链接

        # 不停止循环爬取
        while True:
            # 对links列表进行轮询
            for link in self.links:
                try:
                    # 设置刷新等待时间
                    self.driver.set_page_load_timeout(10)
                    self.driver.set_script_timeout(10)

                    self.driver.get(link)
                    time.sleep(self.sleeptime)

                    # 清除访问cookies，防止网站检测
                    self.driver.delete_all_cookies()
                    self.driver.execute_script('window.stop()')

                    try:
                        # 找到网页按照库存降序排序按钮并点击
                        self.driver.find_element(By.XPATH,
                                                 '/html/body/div[1]/div[11]/div[2]/div/div[3]/div/div[1]/table/thead/tr/th[3]').click()

                        time.sleep(self.sleeptime)

                        # 获取商品列表
                        lis = self.driver.find_elements(By.XPATH,
                                                        '/html/body/div[1]/div[11]/div[2]/div/div[3]/div/div[1]/table/tbody')

                        # 对商品列表轮询获取商品标签
                        for li in lis:
                            self.driver.implicitly_wait(3)

                            # 获取标签中商品名称
                            title = li.find_element(By.XPATH,
                                                    '/html/body/div[1]/div[11]/div[2]/div/div[3]/div/div[1]/table/tbody/tr/td[1]/a/span[1]/span[1]').text

                            self.driver.implicitly_wait(3)

                            # 获取标签中商品库存
                            qty = li.find_element(By.XPATH,
                                                  '/html/body/div[1]/div[11]/div[2]/div/div[3]/div/div[1]/table/tbody/tr/td[3]/div[1]/span[1]').text
                            qty = qty.replace(',', '')
                            qty = int(qty)

                            # 判断库存数是否达到发送邮件标准
                            config = self.read_config()
                            if qty > config['numbers']:
                                print('商品名：' + title + ' 达到预定库存数！')
                                temp = sendMails(title, qty)
                                # sendMails.send_mails(temp, title=title, qty=qty, platform='Arrow')
                            print('商品名称：' + title + '\t剩余库存' + str(qty))
                    except Exception as e:
                        print(e)
                        continue

                except Exception as e:
                    print(e)
                    continue
            # 每轮搜索间隔半小时
            time.sleep(1800)
