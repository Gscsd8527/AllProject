from django.shortcuts import render, HttpResponse
from django.conf import settings
from demo_update.settings import *
import os
# Create your views here.
from django.http import JsonResponse
import requests

def update(request):
    return render(request, 'update/update.html')

def show(request):
    pic = request.FILES['pic']
    picName = os.path.join(MEDIA_ROOT, pic.name)
    with open(picName, 'wb+') as pic1:
        for c in pic.chunks():
            pic1.write(c)
    return HttpResponse(picName)


def OAuth(request):
    ApplicationId = '021725df7af06958fea7e1a2e61e560112b30d010646d3230eb510587296b3fb'
    SecretId = 'dc976ec64f431d17ce5290329410eff55d80064bc7e9848966583c8fc3b15b4e'
    CallbackUrl = 'http://py.yuedusikao.com:8993/'
    if request.method == 'POST':
        pass
    else:
        context = {
            'gitlab_oauth_url':  'https://gitlab.com/login/oauth/authorize?client_id={}'.format(ApplicationId)
        }
        return render(request, 'login.html', context)


def gitlab_login(request):
    ApplicationId = '021725df7af06958fea7e1a2e61e560112b30d010646d3230eb510587296b3fb'
    SecretId = 'dc976ec64f431d17ce5290329410eff55d80064bc7e9848966583c8fc3b15b4e'
    CallbackUrl = 'http://py.yuedusikao.com:8993/'
    data = {
        'client_id': ApplicationId,
        'redirect_uri': CallbackUrl,
        'response_type': 'code',
        # 'secret': SecretId,
        # 'state': SecretId,
    }
    url = 'https://gitlab.com/login/oauth/authorize?'
    for k,v in data.items():
        k_v = k + '=' + v + '&'
        url += k_v
    url = url.strip('&')
    return HttpResponse(url)


