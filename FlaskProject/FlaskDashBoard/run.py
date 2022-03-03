from flask import Flask, Blueprint, request, g, jsonify
from models import User
from apps.users.views import user_app
from exts import db
import jwt
from Utils.jwt_auth import SALT
from jwt import exceptions
import functools
from Utils.utils import resp_success_status, resp_error_status


app = Flask(__name__)

app.config["debug"] = True
app.config.from_pyfile('setting.py')


db.app = app
db.init_app(app)

# db.create_all()

@app.before_request
def jwt_authentication():
    """
       1.获取请求头Authorization中的token
       2.使用jwt模块进行校验

    无返回值的话默认为None就放行
    有返回值的话
       如果是字符串就直接return 字符串
       如果是字典类型的话 就得把字典格式序列化一下
    """
    token = request.headers.get('Authorization')
    try:
        payload = jwt.decode(token, SALT, algorithms=['HS256'])
        g.username = payload.get("username")
        print(payload)
        print('token认证成功')
    except exceptions.ExpiredSignatureError:  # 'token已失效'
        g.username = 1
        print('token已失效')
        return jsonify(resp_error_status(msg="jwt_authentication token已失效"))
    except jwt.DecodeError:  # 'token认证失败'
        g.username = 2
        print('token认证失败')
        # return "token认证失败"
        return jsonify(resp_error_status(msg="jwt_authentication token认证失败"))
    except jwt.InvalidTokenError:  # '非法的token'
        g.username = 3
        print('非法的token')
        return jsonify(resp_error_status(msg="jwt_authentication 非法的token"))


@app.route("/")
def index():
    return "hello"


if __name__ == '__main__':
    app.register_blueprint(user_app, url_prefix="/user")  # 多层路由注册
    app.run(debug=True)
