from rest_framework.authentication import BaseAuthentication
import jwt
from jwt import exceptions
from rest_framework.exceptions import AuthenticationFailed

# # 盐
# SALT = 'd%=w@)#q7ro(y=j44rwaf4hi-)h5(*a5$ohsy$3!y&u--atr_q'
# # 或者使用setting配置里面的盐值
# """
from django.conf import settings
SALT = settings.SECRET_KEY
# """


# JWT 认证验证类
class JewQueryParamsAuthenticate(BaseAuthentication):
    def authenticate(self, request):
        """
            1. 切割
            2. 解密第二段/判断是否过期
            3. 验证第三段合法性
            return:

        authenticate 有三种返回值
           1. 抛出异常: AuthenticationFailed 类型（使用这个认证的视图就不在执行了，抛出什么异常就返回什么）
           2. return一个元组（1， 2），表示认证通过，在视图中如果调用request.user就是第一个值，request.auth 就是第二个值
           3. None  什么都不干
        """

        # 区分get 和 post方法来获取 token 值
        method = request._request.method
        if method == 'GET':
            jwt_token = request.query_params.get('token')
        elif method == 'POST':
            jwt_token = request.data.get('token')
        else:
            jwt_token = request.query_params.get('token')

        try:
            payload = jwt.decode(jwt_token, SALT, True)
            print('payload = ', payload)
        except exceptions.ExpiredSignatureError:
            print('token已失效')
            raise AuthenticationFailed({'code': 300, 'message': 'token已失效'})
        except jwt.DecodeError:
            print('token认证失败')
            raise AuthenticationFailed({'code': 300, 'message': 'token认证失败'})
        except jwt.InvalidTokenError:
            print('非法的token')
            raise AuthenticationFailed({'code': 300, 'message': '非法的token'})
        return (payload, jwt_token)



