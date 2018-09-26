import os
#
# os.system("shutdown -s -t 3600")


import smtplib
from email.mime.text import MIMEText
from email.header import Header


HOST = "smtp.163.com"
sender = "17691097450@163.com"
receivers = ['296862898@qq.com']

def sendemail():
    text = '工作完成啦！您的电脑将在5分钟后自动关闭'
    msg = MIMEText(_text=text, _charset='utf-8')
    msg['From'] = Header('jing163', 'utf-8')
    msg['To'] = receivers[0]
    msg['Subject'] = Header('爬虫通知', 'utf-8')
    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(HOST, 25)
        smtpObj.login(sender, 'jxq296862898')
        smtpObj.sendmail(sender, receivers, msg.as_string())
        smtpObj.quit()
    except smtplib.SMTPException:
        print('Error')



