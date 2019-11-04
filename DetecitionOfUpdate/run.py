import smtplib
from email.mime.text import MIMEText
import datetime
import time
from config import HOST, SENDER, PWD, logger
from WebSite.Kaggle.kaggle import KaggleUpdate
from WebSite.Zenodo.zenodo import ZenodoUpdate
from WebSite.Harvard.harvard import HarvardUpdate
from WebSite.ScholarMate.scholarmate import scholarmateUpdate



def setHtml(resp_list):
    body_count = """<table style="margin: 0px auto"><tr style="margin: 10px 10px">
        <td><h2>监测站点名称&nbsp;&nbsp;</h2></td>
        <td><h2>监测站点是否更新&nbsp;&nbsp;</h2></td>
        <td><h2>监测站点数据量是否更新&nbsp;&nbsp;</h2></td>
        <td><h2>已入库的数据集&nbsp;&nbsp;</h2></td>
        <td><h2>本次检测到的数据集&nbsp;&nbsp;</h2></td>
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
        <td>{}个</td>
        <td>{}</td>
    </tr>""".format(resp['webName'], update_data['isUpdate'][resp['isUpdate']],
                    update_data['isUpdate'][resp['IsNumsUpdate']], resp['haveAccess'], resp['newNum'])
        body_count += table_str
    body_count += '</table>'
    return body_count


def SeedEmail(resp_list):
    """
    发送邮件
    :return:
    """
    # receiver = ['tan_gscsd@163.com', 'luchangfa@cnic.cn', 'jianglulu@cnic.cn', 'cqlxst@126.com']  # 设置邮件接收人，可以是QQ邮箱
    receiver = ['tan_gscsd@163.com']  # 设置邮件接收人，可以是QQ邮箱
    body = setHtml(resp_list)
    msg = MIMEText(body, 'html')  # 设置正文为符合邮件格式的HTML内容
    msg['subject'] = '检测网站是否更新'
    # 设置邮件标题
    msg['from'] = SENDER
    # 设置发送人
    msg['to'] = ','.join(receiver)
    # 设置接收人
    try:
        s = smtplib.SMTP_SSL(HOST)
        # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL
        s.login(SENDER, PWD)
        # 登陆邮箱
        s.sendmail(SENDER, receiver, msg.as_string())
        # 发送邮件！
        # print('Done.sent email success')
        logger.info('邮件发送成功')
    except smtplib.SMTPException:
        # print('Error.sent email fail')
        logger.info('邮件发送失败')


def getKagge():
    """
    检测Kaggle网站
    :return:
    """
    logger.info('-------查询Kaggle网站--------')
    resp_json = KaggleUpdate()
    # 已经获取的数据量
    resp_json['haveAccess'] = 17803
    if resp_json['newNum'] > 17803:
        resp_json['IsNumsUpdate'] = 1
    return resp_json


def getZenodo():
    """
    检测Zenodo
    :return:
    """
    logger.info('-------查询Zenodo网站--------')
    resp_json = ZenodoUpdate()
    # 已经获取的数据量
    resp_json['haveAccess'] = 17464
    if resp_json['newNum'] > 17464:
        resp_json['IsNumsUpdate'] = 1
    # print('resp_json= ', resp_json)
    return resp_json


def getHarvard():
    """
    检测Harvard
    :return:
    """
    logger.info('-------查询Harvard网站--------')
    resp_json = HarvardUpdate()
    resp_json['haveAccess'] = 629
    if resp_json['newNum'] > 629:
        resp_json['IsNumsUpdate'] = 1
    return resp_json

def getScholarmateUpdate():
    """
    检测Scholarmate
    :return:
    """
    logger.info('-------查询 科研之友 网站--------')
    resp_json = scholarmateUpdate()
    resp_json['haveAccess'] = 533228
    if resp_json['newNum'] > 533228:
        resp_json['IsNumsUpdate'] = 1
    return resp_json



def main():
    resp_list = []
    resp_kaggle = getKagge()
    resp_list.append(resp_kaggle)
    resp_zenodo = getZenodo()
    resp_list.append(resp_zenodo)
    resp_harvard = getHarvard()
    resp_list.append(resp_harvard)
    resp_scholarmate = getScholarmateUpdate()
    resp_list.append(resp_scholarmate)
    SeedEmail(resp_list)




if __name__ == '__main__':
    while True:
        now = datetime.datetime.now()
        today = (datetime.datetime.now() + datetime.timedelta(days=1)).weekday()
        hour = now.strftime('%H')
        logger.info('当前时间为： ' + str(now))
        if hour == '09' and today == 1:
            main()
            logger.info('-------执行程序后休眠中-------')
            time.sleep(3600)

        logger.info('-------未到指定时间，休眠中-------')
        time.sleep(3600)
