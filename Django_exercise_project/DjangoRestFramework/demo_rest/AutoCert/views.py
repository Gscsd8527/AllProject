from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
from AutoCert.models import UserInfo, UserToken
from django.http import HttpResponse
import json

class SVIPPremission(object):
    message = "必须是SVIP才能访问"  # 这里的message表示如果不通过权限的时候，错误提示信息
    def has_permission(self, request, view):
        if request.user.user_type != 3:
            return False
        return True


class MyPremission(object):
    # 这个权限类表示当用户为SVIP时不可通过
    def has_permission(self, request, view):
        if request.user.user_type == 3:
            return False
        return True

def md5(user):
    import hashlib
    import time
    ctime = str(time.time())
    # token加密
    m = hashlib.md5(bytes(user, encoding='utf-8'))
    m.update(bytes(ctime, encoding='utf-8'))
    return m.hexdigest()

class AuthView(APIView):
    def get(self, request, *args, **kwargs):
        ret = {
            'code': 100,
            'message': 'success',
            'name': 'gscsd'
        }
        ret = json.dumps(ret, ensure_ascii=False)
        return HttpResponse(ret)
    def post(self, request, *args, **kwargs):
        resp = {
            'code': 100,
            'msg': None
        }
        try:
            user = request.POST.get('username')
            pwd = request.POST.get('password')
            obj = UserInfo.objects.filter(username=user).first()
            if not obj:
                obj = UserInfo.objects.create(username=user, password=pwd)
                resp['code'] = 100
                resp['msg'] = '创建用户成功'
            token = md5(user)
            UserToken.objects.update_or_create(user=obj, defaults={'token': token})
            resp['token'] = token
        except Exception as e:
            resp['code'] = 101
            resp['msg'] = '请求异常--' + str(e)
        return Response(resp)

class UserInfoView(APIView):
    permission_classes = [SVIPPremission]
    def get(self, request, *args, **kwargs):
        print(request.user)
        return Response('SVIP用户信息')