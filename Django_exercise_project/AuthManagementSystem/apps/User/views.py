from rest_framework.views import APIView
from rest_framework.response import Response
import datetime
from .models import UserInfo, Role
from .serializers import UserInfoSerializers
from Utils.utils import filed_filter, resp_success_status, resp_error_status
from Utils.jwt_auth import create_token
from Utils.auth import JewQueryParamsAuthenticate
from Utils.permission import ChcekPremission


class UserRegisterView(APIView):
    """
    用户注册视图
    """
    def post(self, request, format=None):
        username = request.POST.get('username')
        password = request.POST.get('password')
        real_name = request.POST.get('real_name')
        email = request.POST.get('email')
        if all([username, password, real_name, email]):
            serializers = UserInfoSerializers(data=request.data)
            if serializers.is_valid(raise_exception=True):  # 如果要校验字段，就必须加  raise_exception=True
                user = serializers.save()
                # 注册后里面给一个token
                token = create_token({'user_id': user.id, 'username': username})
                # 如果不传值过来，默认该员工是 普通员工
                role_ = Role.objects.get(title='普通员工')
                user.role.add(role_)
                resp = resp_success_status(msg="注册", token=token)
            else:
                return resp_error_status(msg="数据校验失败")
        else:
            resp = resp_error_status(msg='用户名 密码 真实姓名漏填')
        return Response(resp)


class UserLogingView(APIView):
    """
    用户登录
    """
    def post(self, request, format=None):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if all([username, password]):
            user = UserInfo.objects.filter(username=username, password=password).first()
            if user:
                token = create_token({'user_id': user.id, 'username': username})
                resp = resp_success_status(msg="登录", token=token)
            else:
                resp = resp_error_status(msg="该用户不存在")
        else:
            resp = resp_error_status(msg="用户名 密码 漏填")
        return Response(resp)


class UserInfoView(APIView):
    """
    用户信息查看
    """
    authentication_classes = (JewQueryParamsAuthenticate, )  # 需要验证当前用户信息

    def get(self, request, format=None):
        user_id = request.user['user_id']   # request.user 中包含了我们放入创建token是放入的值，这个值
        user = UserInfo.objects.filter(id=user_id).first()
        username = user.username
        real_name = user.real_name
        email = user.email
        temp_dict = {
            'username': username,
            'real_name': real_name,
            'email': email,
        }
        resp = resp_success_status(msg="", **temp_dict)
        return Response(resp)


class UserInfoUpdateView(APIView):
    """
    用户信息修改
    """
    authentication_classes = (JewQueryParamsAuthenticate,)  # 需要验证当前用户信息

    def post(self, request, format=None):
        user_id = request.user['user_id']  # request.user 中包含了我们放入创建token是放入的值

        username = request.POST.get('username')
        password = request.POST.get('password')
        real_name = request.POST.get('real_name')
        email = request.POST.get('email')

        update_field = {
            'username': username,
            'password': password,
            'real_name': real_name,
            'email': email,
        }
        new_field = filed_filter(update_field)
        new_field['update_time'] = datetime.datetime.now()  # update方式更新数据不会触发更改时间，save方式才会触发
        user = UserInfo.objects.filter(id=user_id).first()
        if user:
            UserInfo.objects.filter(id=user_id).update(**new_field)
            resp = resp_success_status(msg="修改")
        else:
            resp = resp_error_status(msg="用户不存在")
        return Response(resp)


class UserDeleteView(APIView):
    """
    删除用户
    """
    authentication_classes = (JewQueryParamsAuthenticate,)  # 需要验证当前用户信息
    permission_classes = [ChcekPremission, ]  # 不是指定的用户删除不了数据

    def post(self, request, format=None):
        user_id = request.POST.get('id')
        UserInfo.objects.filter(id=user_id).update(**{'is_delete': 1, 'update_time': datetime.datetime.now()})
        resp = resp_success_status(msg="删除")
        return Response(resp)

