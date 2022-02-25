import json
import smtplib
from email.header import Header
from email.mime.text import MIMEText


class sendMails:

    title = None
    qty = None

    def __init__(self, title, qty):
        self.qty = qty
        self.title = title

    def read_config(self):
        with open("config.json") as json_file:
            config = json.load(json_file)
        return config

    def send_mails(self, title, qty, platform):
        # # 163邮箱smtp服务器
        # host_server = 'smtp.163.com'
        # # sender_addr为发件人
        # sender_addr = 'digikey_bot@163.com'
        # # pwd为邮箱的授权码
        # pwd = 'ZRNJZUTZMINGEMTP'
        # # 发件人的邮箱
        # sender = 'digikey_bot@163.com'
        # # 收件人邮箱
        # receiver = 'Lily@aoyuehk.com'

        config = self.read_config()

        # 邮件的正文内容
        mail_content = '商品名：' + title + ' 库存为：' + str(qty) + ' 达到预定库存数！'
        # 邮件标题
        mail_title = '商品名：' + title + ' ' +str(platform) +'库存为：' + str(qty) + ' 达到预定库存数！ 请尽快登陆购买。'

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