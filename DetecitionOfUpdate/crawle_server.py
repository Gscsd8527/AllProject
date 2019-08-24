import logging
import smtplib
from email.mime.text import MIMEText
import datetime
import time
from webSite.kaggle import *

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

def setHtml(resp_list):
    body_count = """<table style="margin: 0px auto"><tr style="margin: 10px 10px">
        <td><h2>网站名称&nbsp;&nbsp;</h2></td>
        <td><h2>网站更新&nbsp;&nbsp;</h2></td>
        <td><h2>数据量更新&nbsp;&nbsp;</h2></td>
        <td><h2>上次数据量&nbsp;&nbsp;</h2></td>
        <td><h2>当前数据量&nbsp;&nbsp;</h2></td>
    </tr>"""
    for resp in resp_list:
        update_data = {
            'isUpdate': {
                0: '否',
                1: '是'
            },
            'IsNumsUpdate': {
                0: '否',
                1: '是'
            },
        }
        table_str = """
    
    <tr>
        <td style="color: red; font-weight:bold">{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
    </tr>""".format(resp['webName'], update_data['isUpdate'][resp['isUpdate']], update_data['isUpdate'][resp['IsNumsUpdate']], resp['lastNum'], resp['newNum'])
        body_count += table_str
    body_count += '</table>'
    return body_count

def SeedEmail(resp_list):
    """
    发送邮件
    :return:
    """
    host = "smtp.163.com"  # 设置发件服务器地址
    sender = '*******'  # 设置发件邮箱，一定要自己注册的邮箱
    pwd = '******'  # 设置发件邮箱的授权码密码，根据163邮箱提示，登录第三方邮件客户端需要授权码
    receiver = ['*****', '******', '******', '*****']  # 设置邮件接收人，可以是QQ邮箱
    body = setHtml(resp_list)
    msg = MIMEText(body, 'html')  # 设置正文为符合邮件格式的HTML内容
    msg['subject'] = '检测网站是否更新'
    # 设置邮件标题
    msg['from'] = sender
    # 设置发送人
    msg['to'] = ','.join(receiver)
    # 设置接收人
    try:
        s = smtplib.SMTP_SSL(host)
        # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL
        s.login(sender, pwd)
        # 登陆邮箱
        s.sendmail(sender, receiver, msg.as_string())
        # 发送邮件！
        # print('Done.sent email success')
        logger.info('邮件发送成功')
    except smtplib.SMTPException:
        # print('Error.sent email fail')
        logger.info('邮件发送失败')


def getKagge():
    logger.info('-------查询Kaggle网站--------')
    resp_json = KaggleUpdate()
    # print('resp_json= ', resp_json)
    return resp_json

def main():
    resp_list = []
    resp_kaggle = getKagge()
    # a = {'isUpdate': 0, 'IsNumsUpdate': 1, 'webName': 'Google', 'lastNum': 111111, 'newNum': 222222}
    # resp_list.append(a)
    resp_list.append(resp_kaggle)
    SeedEmail(resp_list)

if __name__ == '__main__':
    while True:
        now = datetime.datetime.now()
        hour = now.strftime('%H')
        logger.info('当前时间为： ' + str(now))
        if hour == '10':
            main()
            logger.info('-------执行程序后休眠中-------')
            time.sleep(3600)
        logger.info('-------未到指定时间，休眠中-------')
        time.sleep(3600)
