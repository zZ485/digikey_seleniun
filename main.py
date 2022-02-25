#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022-2-25
# @Author  : zZ485
# @Github  : https://github.com/zZ485
# @Software: DigiKey & Arrow Spider
# @File    : main.py

from MultiSpider import *


def main():
    """
    创建两个平台爬虫对象并运行
    """
    multispider = MultiSpider()
    multispider.multiProcess()


if __name__ == '__main__':
    """
    程序入口
    """
    main()
