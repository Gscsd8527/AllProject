from django.shortcuts import render, HttpResponse
import requests

CLIENT_ID = 'aa87fb3bd529581eac5b'

CLIENT_SECRET = '3ff3e7d7413b27b309aec717fecb04ccb30eef47'

CLIENT_CALLBACK_URL = 'http://127.0.0.1:8000/oauth/'  #填写你的回调地址

# Create your views here.

def auth(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        return HttpResponse('This is Auth')

def github_token(code):
    """
    通过传入的 code 参数，带上client_id、client_secret、和code请求GitHub，以获取access_token
    :param code: 重定向获取到的code参数
    :return: 成功返回acces_token；失败返回None；
    """
    token_url = 'https://github.com/login/oauth/access_token?' \
                'client_id={}&client_secret={}&code={}'
    token_url = token_url.format(CLIENT_ID, CLIENT_SECRET, code)	# 这里的client_id、client_secret修改为自己的真实ID与Secret
    header = {
        'accept': 'application/json'
    }
    res = requests.post(token_url, headers = header)
    if res.status_code == 200:
        res_dict = res.json()
        print(res_dict)
        return res_dict['access_token']
    return None

def github_user(access_token):
    """
    通过传入的access_token，带上access_token参数，向GitHub用户API发送请求以获取用户信息；
    :param access_token: 用于访问API的token
    :return: 成功返回用户信息，失败返回None
    """
    user_url = 'https://api.github.com/user'
    access_token = 'token {}'.format(access_token)
    headers = {
        'accept': 'application/json',
        'Authorization': access_token
    }
    res = requests.get(user_url, headers=headers)
    if res.status_code == 200:
        user_info = res.json()
        print(user_info)
        user_name = user_info.get('name', None)
        return user_info
    return None

def Oauth(request):
    code = request.GET.get('code', None)
    if code:
        access_token = github_token(code)  # 向GitHub发送请求以获取access_token
        if access_token:
            user_info = github_user(access_token)  # 向GitHub用户API发送请求获取信息
            if user_info:
                user_name = user_info.get('name', None)
                return HttpResponse(user_name)

        return HttpResponse('获取token失败，请重试！')

    return HttpResponse('获取code参数失败，请重试！')



