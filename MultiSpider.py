#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022-2-25
# @Author  : zZ485
# @Github  : https://github.com/zZ485
# @Software: DigiKey & Arrow Spider
# @File    : MultiSpider.py


import json
from multiprocessing import Process

import Spider
from arrowSpider import ArrowSpider


class MultiSpider:

    processList1 = []
    processList2 = []

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

        for i, j in range(processNumber):
            i = Process(target=self.digikeySpider)
            j = Process(target=self.arrowSpider)

            i.start()
            j.start()
            self.processList.append(i)
            self.processList2.append(j)

            # 每两分钟创建新进程
            i.join(timeout=120)
            j.join(timeout=120)

