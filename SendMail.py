#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022-2-25
# @Author  : zZ485
# @Github  : https://github.com/zZ485
# @Software: DigiKey & Arrow Spider
# @File    : SendMail.py


import json
import smtplib
from email.header import Header
from email.mime.text import MIMEText


class sendMails:

    title = None  # 商品名称
    qty = None  # 商品库存

    def __init__(self, title, qty):
        self.qty = qty
        self.title = title

    def read_config(self):
        """
        读入config.json文件中的配置

        :param self: 对象自身
        :return: config字典
        """
        with open("config.json") as json_file:
            config = json.load(json_file)
        return config

    def send_mails(self, title, qty, platform):
        """
        完成传入的两个数之和

        :param self: 对象自身
        :param title: 获取的商品名称
        :param qty: 获取商品的库存数量
        :param platform: 商品所在平台
        :return: void
        """

        config = self.read_config()

        # 邮件的正文内容
        mail_content = '商品名：' + title + ' 库存为：' + str(qty) + ' 达到预定库存数！'
        # 邮件标题
        mail_title = '商品名：' + title + ' ' + str(platform) + '库存为：' + str(qty) + ' 达到预定库存数！ 请尽快登陆购买。'

        # ssl登录
        smtp = smtplib.SMTP_SSL(config['host_server'])
        # 参数值为1表示开启调试模式，参数值为0关闭调试模式
        smtp.set_debuglevel(1)
        smtp.ehlo(config['host_server'])
        smtp.login(config['sender_addr'], config['pwd'])

        msg = MIMEText(mail_content, "plain", 'utf-8')
        msg["Subject"] = Header(mail_title, 'utf-8')
        msg["From"] = config['sender']
        msg["To"] = config['receiver']
        smtp.sendmail(config['sender'], config['receiver'], msg.as_string())
        smtp.quit()
