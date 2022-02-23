import re
import time
import smtplib
from email.header import Header

from selenium import webdriver
from selenium.webdriver.common.by import By
from email.mime.text import MIMEText


def send_mails(title, qty):
    # 163邮箱smtp服务器
    host_server = 'smtp.163.com'
    # sender_addr为发件人
    sender_addr = 'digikey_bot@163.com'
    # pwd为邮箱的授权码
    pwd = 'ZRNJZUTZMINGEMTP'
    # 发件人的邮箱
    sender = 'digikey_bot@163.com'
    # 收件人邮箱
    receiver = 'aoyue@vip.126.com'

    # 邮件的正文内容
    mail_content = '商品名：' + title + ' 库存为：' + str(qty) + ' 达到预定库存数！'
    # 邮件标题
    mail_title = '商品名：' + title + ' 库存为：' + str(qty) + ' 达到预定库存数！ 请尽快登陆购买。'

    # ssl登录
    smtp = smtplib.SMTP_SSL(host_server)
    # 参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.set_debuglevel(1)
    smtp.ehlo(host_server)
    smtp.login(sender_addr, pwd)

    msg = MIMEText(mail_content, "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender
    msg["To"] = receiver
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()


def main():
    sleepTime = 15
    links = []
    goodList = []
    pageNum = []

    # 不打开浏览器模式
    # option = Options()
    # option.add_argument('--windows-size=1920,1080')
    # option.add_argument('--headless')
    # driver = webdriver.Chrome(chrome_options=option)
    driver = webdriver.Chrome()

    # 获取商品列表
    with open('GoodList.txt', 'r', encoding='utf-8') as f:
        for line in f.readlines():
            goodList.append(line.strip('\n'))  # 剪切 ’\n‘
        f.close()

    for goodName in goodList:
        driver.get('https://www.digikey.cn')
        driver.find_element(By.CSS_SELECTOR,
                            '#header > div.header__top > div.header__search > div > div.searchbox-inner > '
                            'div.searchbox-inner-searchtext > input').send_keys(goodName)
        driver.find_element(By.CSS_SELECTOR, '#header-search-button').click()
        labels = driver.find_elements(By.CSS_SELECTOR,
                                      '#__next > main > div > div > div > '
                                      'div.MuiGrid-root.jss10.MuiGrid-item.MuiGrid-grid-md-9 > div.jss121.jss15 > '
                                      'div.jss120 > div > div > table > tbody > tr')
        time.sleep(sleepTime)
        for label in labels:
            title = label.find_element(By.CSS_SELECTOR, 'td:nth-child(2) > span').text
            link = label.find_element(By.CSS_SELECTOR,
                                      '#__next > main > div > div > div > '
                                      'div.MuiGrid-root.jss10.MuiGrid-item.MuiGrid-grid-md-9 > div.jss121.jss15 > '
                                      'div.jss120 > div > div > table > tbody > tr > td:nth-child(1) > span > '
                                      'a').get_attribute('href')
            if title == '集成电路（IC）':
                links.append(link)
        time.sleep(sleepTime)

    while True:
        for a in links:
            driver.get(a)
            driver.find_element(By.CSS_SELECTOR, '#__next > main > section > div > section > '
                                                 'div.MuiGrid-root.MuiGrid-container.MuiGrid-direction-xs-column > '
                                                 'div.MuiGrid-root.MuiGrid-container.MuiGrid-item > div > '
                                                 'div.MuiGrid-root.MuiGrid-container.MuiGrid-spacing-xs-2.MuiGrid-item > '
                                                 'div:nth-child(1) > div.jss105 > fieldset > div > label:nth-child(1) > '
                                                 'span.MuiButtonBase-root.MuiIconButton-root.jss22.MuiCheckbox-root.jss122.MuiCheckbox-colorSecondary.MuiIconButton-colorSecondary > span > input').click()
            time.sleep(sleepTime)
            leftNum = driver.find_element(By.CSS_SELECTOR, '#__next > main > section > div > section > '
                                                           'div.MuiGrid-root.MuiGrid-container.MuiGrid-direction-xs'
                                                           '-column > '
                                                           'div.MuiGrid-root.jss53.MuiGrid-container.MuiGrid-spacing-xs-2.MuiGrid-align-items-xs-center > div:nth-child(2) > span > div > span').text
            if leftNum == '0':
                break
            driver.find_element(By.CSS_SELECTOR,
                                '#__next > main > section > div > section > '
                                'div.MuiGrid-root.MuiGrid-container.MuiGrid-direction-xs-column > '
                                'div.MuiGrid-root.jss53.MuiGrid-container.MuiGrid-spacing-xs-2.MuiGrid-align-items-xs'
                                '-center > div:nth-child(1) > button').click()

            time.sleep(sleepTime)

            print(a)
            nums = driver.find_element(By.CSS_SELECTOR,
                                       '#__next > main > section > div > div.jss49 > div > div:nth-child(3) > div > '
                                       'div:nth-child(1) > div > div:nth-child(1) > div > div:nth-child(2) > span').text
            pageNum = re.findall("\d+\.?\d*", nums)
            pageNum = list(map(int, pageNum))
            print(pageNum[1])

            time.sleep(sleepTime)
            for i in range(1, pageNum[1]):
                time.sleep(sleepTime)

                lis = driver.find_elements(By.CSS_SELECTOR, '#data-table-0 > tbody > tr')

                # 对每页每条商品信息遍历
                for li in lis:
                    # 获取商品名title
                    title = li.find_element(By.CSS_SELECTOR, 'td:nth-child(2) > div > div.MuiGrid-root > div > a').text

                    # 获取商品库存qty
                    qtyAvailable = li.find_element(By.CSS_SELECTOR, 'td:nth-child(4) > span > div').text
                    qty = re.findall("\d+\.?\d*", qtyAvailable)
                    qty = list(map(int, qty))

                    # # 发送邮件
                    if max(qty) > 500:
                        print('商品名：' + title + ' 达到预定库存数！')
                        send_mails(title=title, qty=qty)

                    print('商品名称：' + title + '\t剩余库存' + str(qty))

                    if pageNum[1] == 1:
                        break

                    buttons = driver.find_elements(By.CSS_SELECTOR, '#__next > main > section > div > div > div > div > div > div .MuiIconButton-root')
                    button = buttons[0]
                    button.send_keys('\n')


if __name__ == "__main__":
    main()
