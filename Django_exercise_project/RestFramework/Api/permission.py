class SVIPPremission(object):
    message = "必须是SVIP才能访问"  # 这里的message表示如果不通过权限的时候，错误提示信息

    def has_permission(self, request, view):
        print(request.user)
        if request.user.user_type != 3:
            return False
        return True


class MyPremission(object):
    # 这个权限类表示当用户为SVIP时不可通过
    def has_permission(self, request, view):
        if request.user.user_type == 3:
            return False
        return True


from rest_framework.authentication import BaseAuthentication
from Api.models import UserToken
from rest_framework import exceptions

class MyAuthenticate(BaseAuthentication):
    """
    在setting中 DEFAULT_AUTHENTICATION_CLASSES 配置
    每次请求前 会将 token带过来，根据这个token来查看这个用户是否存在，然后返回这个用户名 和 token 值
    """
    def authenticate(self, request):
        self._authenticator = None
        token = request.query_params.get('token')
        user_object = UserToken.objects.filter(token=token).first()
        if not user_object:
            raise exceptions.AuthenticationFailed("用户认证失败")
        return (user_object.user, user_object.token)


