from run import app
from flask import request, g
import jwt
from .jwt_auth import SALT
from jwt import exceptions
import functools
from .utils import resp_error_status, resp_success_status


@app.before_request
def jwt_authentication():
    """
       1.获取请求头Authorization中的token
       2.使用jwt模块进行校验
    """
    auth = request.headers.get('Authorization')
    print('auth = ', auth)
    token = auth
    print('token = ', token)
    try:
        payload = jwt.decode(token, SALT, algorithms=['HS256'])
        # g.username = payload.get("username")
        print(payload)
        # return resp_success_status(msg="jwt_authentication token有效", token=token)
    except exceptions.ExpiredSignatureError:  # 'token已失效'
        # g.username = 1
        print('jwt_authentication token已失效')
        # return resp_error_status(msg="jwt_authentication token已失效")
    except jwt.DecodeError:  # 'token认证失败'
        # g.username = 2
        print('jwt_authentication token认证失败')
        # return resp_error_status(msg="jwt_authentication token认证失败")
    except jwt.InvalidTokenError:  # '非法的token'
        # g.username = 3
        print('jwt_authentication 非法的token')
        # return resp_error_status(msg="jwt_authentication 非法的token")


def login_required(f):
    """
    让装饰器装饰的函数属性不会变 -- name属性
    第1种方法,使用functools模块的wraps装饰内部函数
    """
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            if g.username == 1:
                # return {'code': 4001, 'message': 'login_required token已失效'}, 401
                return resp_error_status(msg="login_required token已失效"), 401
            elif g.username == 2:
                # return {'code': 4001, 'message': 'login_required token认证失败'}, 401
                return resp_error_status(msg="login_required token认证失败"), 401
            elif g.username == 2:
                # return {'code': 4001, 'message': 'login_required 非法的token'}, 401
                return resp_error_status(msg="login_required 非法的token"), 401
            else:
                return f(*args, **kwargs)
        except BaseException as e:
            # return {'code': 4001, 'message': 'login_required 请先登录认证.'}, 401
            return resp_error_status(msg="login_required 请先登录认证"), 401

    '第2种方法,在返回内部函数之前,先修改wrapper的name属性'
    # wrapper.__name__ = f.__name__
    return wrapper
