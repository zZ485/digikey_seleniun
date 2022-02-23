# import requests
# from user_agents import UserAgent
# import json
# import time
#
# goodList = []
# ua = UserAgent()
# sleepTime = 60  # 多少秒检测一次
# headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
#            'Accept-Language': 'zh-cn',
#            'x-currency': 'CNY',
#            'accept-encoding': 'gzip, deflate, br',
#            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
#            }
#
# # 读取txt文件中商品ID，存入列表
# with open('GoodList.txt', 'r', encoding='utf-8') as f:
#     for line in f.readlines():
#         goodList.append(line.strip('\n'))  # 剪切 ’\n‘
#     f.close()
#
# for i in range(len(goodList)):
#     goodId = goodList[i]
#     url = "https://www.digikey.cn/products/api/v4/pricing/" + str(goodId)
#
#     # 发送请求，获取数据
#     try:
#         digiKeyApi = requests.get(url, headers)
#     except TypeError:
#         print('请求被拦截，需要更换IP访问')
#         break
#     goodsDetailJSON = digiKeyApi.text
#     # pythonDictionary = json.loads(goodsDetailJSON)
#     print(digiKeyApi.text)
