#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022-2-25
# @Author  : zZ485
# @Github  : https://github.com/zZ485
# @Software: DigiKey & Arrow Spider
# @File    : MultiSpider.py


import json
from threading import Thread

import Spider
from arrowSpider import ArrowSpider


class MultiSpider:

    threadList = []

    def read_config(self):
        """
        读入config.json文件中的配置

        :param self: 对象自身
        :return: config字典
        """
        with open("config.json") as json_file:
            config = json.load(json_file)
        return config

    def digikeySpider(self):
        """
        创建DigiKey平台爬虫机器人
        """
        spider = Spider.DigiKeySpider()

        spider.catchData()

    def arrowSpider(self):
        """
        创建Arrow平台爬虫机器人
        """
        arrowspider = ArrowSpider()

        arrowspider.catchData()

    def multiProcess(self):
        """
        创建多个DigiKey爬虫机器人进程，每个机器人启动间隔120秒
        """

        config = self.read_config()
        # 设定进程数
        processNumber = config['process_number']

        t1 = Thread(target=self.digikeySpider)
        t1.start()
        t2 = Thread(target=self.arrowSpider)
        t2.start()

        self.threadList.append(t1)
        self.threadList.append(t2)

        for i in range(processNumber):
            for t in self.threadList:
                t.join()


