from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from Utils.auth import JwtToken
from django.contrib.auth import authenticate
from .models import User
from Utils.utils import resp_error_status, resp_success_status


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserRegisterView(APIView):
    """
    用户注册视图
    """
    def post(self, request, format=None):
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        if all([username, password]):
            # 使用  create_user 会自动把密码加密，这样我们再效验的时候可以用 authenticate 来校验是否登录
            user = User.objects.create_user(username=username, password=password)
            user.is_active = True  # 激活
            user.save()

            # 签发token
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            resp = resp_success_status(msg="注册", token=token)
        else:
            resp = resp_error_status(msg="用户名密码漏填")
        return Response(resp)


class UserLogingView(APIView):
    """
    用户登录
    """
    def post(self, request, format=None):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            # 签发token
            payload = jwt_payload_handler(user)  # 这个 payload 返回的值就是 我们在 setting 中 配置的 JWT_RESPONSE_PAYLOAD_HANDLER
            token = jwt_encode_handler(payload)
            print('payload = ', payload)
            print('token = ', token)
            resp = resp_success_status(msg="登录", token=token)

        else:
            resp = resp_error_status(msg="登录失败")
        return Response(resp)


class UserInfoView(APIView):
    """
    用户信息查看
    """
    authentication_classes = (JwtToken,)  # 需要验证当前用户信息

    def get(self, request, format=None):
        username = request.user.username  # request.user 里面是传过来的user
        resp = resp_success_status(msg="响应", username=username)
        return Response(resp)

