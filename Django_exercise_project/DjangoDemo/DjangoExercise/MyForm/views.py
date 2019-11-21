from django.shortcuts import render, HttpResponse, redirect, reverse
from MyForm.models import MyFormModel
from .forms import LoginForm, RegForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

# Create your views here.
def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if not all([id, username, password, email]):
            return HttpResponse('参数不全')
        else:
            user = MyFormModel.objects.filter(username=username, password=password)
            if len(user):
                context = {
                    'username': username,
                }
                return render(request, 'MyForm/index.html', context)
    else:
        return render(request, 'MyForm/login.html')


def loginForm(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        # 判断是否验证登录通过
        if login_form.is_valid():
            # 验证过程写在了forms.py文件中了，所以这里可以不用写
            # #清洗后的数据， 包含了我们所需要的字段信息 cleaned_data是我们forms中清洗后验证通过的数据
            # username = login_from.cleaned_data['username']
            # password = login_from.cleaned_data['password']
            # # 验证用户数据是否存在
            # user = authenticate(request, username=username, password=password)
            # if user is not None:
            #     # 将登录后的数据存在session中
            #     login(request, user)
            #     return render(request, 'MyForm/index.html', {'username': username})
            user = login_form.cleaned_data['user']
            login(request, user)
            return render(request, 'MyForm/index.html', {'username': user.username})
    else:
        login_from = LoginForm()
        context = {
            'login_form': login_from
        }
        return render(request, 'MyForm/login_form.html', context)

# 注册
def register(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 登录用户
            user = authenticate(username=username, password=password)
            login(request, user)
            return render(request, 'MyForm/index.html', {'username': user.username})
    else:
        reg_form = RegForm()
    context = {}
    context['reg_form'] = reg_form
    return render(request, 'MyForm/register.html', context)
