from django.shortcuts import render, HttpResponse, redirect, reverse
from django.views.generic import View
from apps.user.models import User
import re
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from django.conf import settings
from django.core.mail import send_mail
from celery_tasks.tasks import send_register_active_email
from django.contrib.auth import authenticate, login
# Create your views here.

# /user/register
class RegisterView(View):
    """注册"""
    def get(self, request):
        # 显示注册页面
        return render(request, 'register.html')

    def post(self, request):
        # 进行注册处理
        # 接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')

        # 进行数据校验
        if not all([username, password, email]):
            # 数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})

        # 检验邮箱
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不正确'})

        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})

        # 校验用户是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None

        if user:
            return render(request, 'register.html', {'errmsg': '用户已存在'})

        # 进行业务处理：进行用户注册
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()

        # 这部分使用celery来发送邮件
        # 发送激活链接：http://127.0.0.1:8000/user/active/id
        # 激活链接中需要包含用户的身份信息，并且要把身份形象加密

        # # 加密用户的身份信息，生成激活TOKEN
        serializer = Serializer(settings.SECRET_KEY, 3600)
        info = {'confirm': user.id}
        token = serializer.dumps(info)
        #
        # # 发邮件
        # subject = '天天生鲜欢迎信息'
        # # message = '邮件正文'
        # print(token)
        # print(type(token))
        token = str(token, 'utf-8')
        # print(token)
        # print(type(token))
        # message = '<h1> {} 欢迎您成为天天生鲜注册会员</h1> 请点击下面链接激活您的账户<br/>' \
        #           '<a href="http://127.0.0.1:8000/user/active/{}">' \
        #           'http://127.0.0.1:8000/user/active/{}' \
        #           '</a>'.format(username, token, token)
        # sender = settings.EMAIL_PROM  # 指定发件人
        # receiver = [email] # 收件人列表
        # html_message = message
        # # send_mail(subject, message, sender, receiver) #message转义不了
        # message = ''
        # send_mail(subject, message, sender, receiver, html_message=html_message)

        # celery发邮件
        # send_register_active_email.delery(email, username, token) # 这个不行，没有delery这个方法
        print('------', email, username, token)
        send_register_active_email(email, username, token)
        return HttpResponse('hello')




class ActiveView(View):
    """
    用户激活
    """
    def get(self, request, token):
        """进行用户激活"""
        # 进行解密，获取要激活的用户信息
        serializer = Serializer(settings.SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取激活用户的ID
            user_id = info['confirm']
            user = User.objects.get(id=user_id)
            user.is_active = 1
            user.save()

            # 跳转到登录页面
            return redirect(reverse('user:login'))
        except SignatureExpired as e:
            # 激活链接已过期
            return HttpResponse('激活链接已过期')

class LoginView(View):
    """登录"""
    def get(self, request):
        '''显示登录页面'''
        # 判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
        # 使用模板
        return render(request, 'login.html', {'username': username, 'checked': checked})
        # return render(request, 'login.html')
    def post(self, request):
        # 接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')

        # 校验数据
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '数据不完整'})

        # 业务处理： 登录校验
        user = authenticate(username=username, password=password)
        if user is not None:
            # 用户名密码正确
            if user.is_active:
                # 用户已激活
                login(request, user)

                # 记住用户名时需要这个
                response = redirect(reverse('goods:index'))

                # 判断是否需要记住用户名
                remember = request.POST.get('remember')
                if remember == 'on':
                    # 记住用户名
                    response.set_cookie('username', username, max_age=24*3600)
                else:
                    # 下次不需要记住
                    response.delete_cookie('username')
                return response

                # 跳转到首页
                # return redirect(reverse('goods:index'))
            else:
                # 用户未激活
                return render(request, 'login.html', {'errmsg': '用户未激活'})
        else:
            # 用户名或密码错误
            return render(request, 'login.html', {'errmsg': '用户名或密码错误'})

        # 返回应答
