# 使用celery
from django.core.mail import send_mail
from celery import Celery
from django.conf import settings

# Django环境的初始化
# 在任务处理者一段加这几句
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailyfresh.settings')
django.setup()

# 创建一个Celery类的实列对象
app = Celery('celery_tasks.tasks', borker='redis://127.0.0.1:6379/2')


# 定义任务函数
@app.task  # 加上装饰器装饰，给函数加上一些信息
def send_register_active_email(to_email, username, token):
    '''发送激活邮件'''
    # 组织邮件信息
    subject = '天天生鲜欢迎信息'
    message = '<h1> {} 欢迎您成为天天生鲜注册会员</h1> 请点击下面链接激活您的账户<br/>' \
              '<a href="http://127.0.0.1:8000/user/active/{}">' \
              'http://127.0.0.1:8000/user/active/{}' \
              '</a>'.format(username, token, token)
    sender = settings.EMAIL_PROM  # 指定发件人
    receiver = [to_email]  # 收件人列表
    html_message = message
    # send_mail(subject, message, sender, receiver) #message转义不了
    message = ''
    send_mail(subject, message, sender, receiver, html_message=html_message)
