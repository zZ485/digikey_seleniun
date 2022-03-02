#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022-2-25
# @Author  : zZ485
# @Github  : https://github.com/zZ485
# @Software: DigiKey & Arrow Spider
# @File    : Spider.py
import json
import time
import re

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from SendMail import sendMails


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

    def read_config(self):
        """
        读入config.json文件中的配置

        :param self: 对象自身
        :return: config字典
        """
        with open("config.json") as json_file:
            config = json.load(json_file)
        return config

    def catchData(self):
        """
        DigiKey.com平台爬虫本体
        """

        with open('DigiKeyLinks.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                self.links.append(line.strip('\n'))
            f.close()

        print(len(self.links))

        # 不停止循环爬取
        while True:
            # 对links列表轮询
            try:
                for count in range(len(self.links)):
                    self.driver.get(self.links[count])

                    try:
                        # 找到并点击网页菜单栏”现货“多选框按钮
                        button = self.driver.find_element(By.CSS_SELECTOR,
                                                     '#__next > main > section > div > section >div.MuiGrid-root.MuiGrid-container.MuiGrid-direction-xs-column >div.MuiGrid-root.MuiGrid-container.MuiGrid-item > div >div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-2.MuiGrid-item >div:nth-child(1) > div.jss105 > fieldset > div > label:nth-child(1) > span.MuiButtonBase-root.MuiIconButton-root.jss22.MuiCheckbox-root.jss122.MuiCheckbox-colorSecondary.MuiIconButton-colorSecondary > span > input')
                        button.click()
                        time.sleep(5)
                        # 获取有现货的商品数量
                        leftNum = self.driver.find_element(By.CSS_SELECTOR, '#__next > main > section > div > section > div.MuiGrid-root.MuiGrid-container.MuiGrid-direction-xs-column > div.MuiGrid-root.jss53.MuiGrid-container.MuiGrid-spacing-xs-2.MuiGrid-align-items-xs-center > div:nth-child(2) > span > div > span').text

                    except NoSuchElementException as e:
                        print(e)
                        continue

                    if leftNum == '0':
                        continue
                    elif leftNum == '1':
                        try:
                            self.driver.find_element(By.CSS_SELECTOR,
                                                '#__next > main > section > div > section > '
                                                'div.MuiGrid-root.MuiGrid-container.MuiGrid-direction-xs-column > '
                                                'div.MuiGrid-root.jss53.MuiGrid-container.MuiGrid-spacing-xs-2.MuiGrid-align-items-xs'
                                                '-center > div:nth-child(1) > button').click()
                            time.sleep(self.sleepTime)
                            title = self.driver.find_element(By.CSS_SELECTOR, '#__next > main > div > div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-5 > div > div:nth-child(2) > div > table > thead > tr > th > h1').text
                            inStock = self.driver.find_element(By.CSS_SELECTOR, '#__next > main > div > div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-5 > div > div:nth-child(3) > div > div:nth-child(1) > div > div > span').text
                            qty = re.findall("\d+\.?\d*", inStock)
                            qty = list(map(int, qty))
                            if qty[0] > self.numbers:
                                print('商品名：' + title + ' 达到预定库存数！')
                                temp = sendMails(title, qty)
                                # sendMails.send_mails(temp, title=title, qty=qty, platform= 'DigiKey')
                            print('商品名称：' + title + '\t剩余库存' + str(qty))
                            continue
                        except Exception as e:
                            print(e)
                            continue

                    try:
                        # 点击菜单栏底部”全部应用“按钮，刷新页面
                        self.driver.find_element(By.CSS_SELECTOR,
                                            '#__next > main > section > div > section > '
                                            'div.MuiGrid-root.MuiGrid-container.MuiGrid-direction-xs-column > '
                                            'div.MuiGrid-root.jss53.MuiGrid-container.MuiGrid-spacing-xs-2.MuiGrid-align-items-xs'
                                            '-center > div:nth-child(1) > button').click()
                    except NoSuchElementException as e:
                        print(e)
                        continue

                    time.sleep(self.sleepTime)

                    try:
                        # 获取有现货的商品页数
                        nums = self.driver.find_element(By.CSS_SELECTOR,
                                                   '#__next > main > section > div > div.jss49 > div > div:nth-child(3) > div > '
                                                   'div:nth-child(1) > div > div:nth-child(1) > div > div:nth-child(2) > span').text
                        pageNum = re.findall("\d+\.?\d*", nums)
                        pageNum = list(map(int, pageNum))
                    except Exception as e:
                        print(e)
                        continue

                    time.sleep(self.sleepTime)

                    # 对每页商品轮询
                    for i in range(0, pageNum[1]):
                        time.sleep(self.sleepTime)

                        try:
                            lis = self.driver.find_elements(By.CSS_SELECTOR, '#data-table-0 > tbody > tr')
                        except Exception as e:
                            print(e)
                            continue

                        # 对每页每条商品信息遍历
                        for li in lis:
                            try:
                                # 获取商品名title
                                title = li.find_element(By.CSS_SELECTOR,
                                                        'td:nth-child(2) > div > div.MuiGrid-root > div > a').text

                                # 获取商品库存qty
                                qtyAvailable = li.find_element(By.CSS_SELECTOR, 'td:nth-child(4) > span > div').text
                                qtyAvailable = qtyAvailable.replace(',', '')
                                qty = re.findall("\d+\.?\d*", qtyAvailable)
                                qty = list(map(int, qty))
                            except Exception as e:
                                print(e)
                                continue

                            # # 发送邮件
                            config = self.read_config()
                            if max(qty) > config['numbers']:
                                print('商品名：' + title + ' 达到预定库存数！')
                                temp = sendMails(title, qty)
                                # sendMails.send_mails(temp, title=title, qty=qty, platform= 'DigiKey')

                            print('商品名称：' + title + '\t剩余库存' + str(qty))

                        if pageNum[1] == 1:
                            continue

                            # 若页数不为1，找到页面底部”下一页“按钮
                        buttons = self.driver.find_elements(By.CSS_SELECTOR,
                                                       '#__next > main > section > div > div > div > div > div > div .MuiIconButton-root')
                        button = buttons[0]
                        button.send_keys('\n')
                    count = count + 1
                    print(count)
            except Exception as e:
                print(e)

            # 每轮搜索间隔半小时
            # time.sleep(1800)


digi = DigiKeySpider()
digi.catchData()
