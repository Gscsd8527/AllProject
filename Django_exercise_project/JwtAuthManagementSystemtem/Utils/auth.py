from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework_jwt.authentication import jwt_decode_handler
from rest_framework import exceptions
import jwt

class JwtToken(BaseJSONWebTokenAuthentication):
    def authenticate(self, request):

        # 放置到headers头中,这个字段决定token放哪个位置，这个 参数不能带 HTTP_
        # 小写转为大写，横线“-”转为下划线“_”, 并且加上前缀HTTP, 前端传的headers头的参数名为： auth-token，获取的时候得转换一下
        jwt_token = request.META.get('HTTP_AUTH_TOKEN')

        # 放置到data中
        # method = request._request.method
        # if method == 'GET':
        #     jwt_token = request.query_params.get('token')
        # elif method == 'POST':
        #     jwt_token = request.data.get('token')
        # else:
        #     jwt_token = request.query_params.get('token')
        print(jwt_token)

        if not jwt_token:
            raise exceptions.AuthenticationFailed('token 字段是必须的')
        try:
            payload = jwt_decode_handler(jwt_token)
        except jwt.ExpiredSignature:
            raise exceptions.AuthenticationFailed({'code': 300, 'message': 'token已失效'})
        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed({'code': 300, 'message': 'token认证失败'})
        except jwt.InvalidTokenError:
            raise exceptions.AuthenticationFailed({'code': 300, 'message': '非法的token'})
        user = self.authenticate_credentials(payload)
        return (user, jwt_token)


