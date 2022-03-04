from flask import request, jsonify, g
from . import user_app
from models import User
from Utils.utils import resp_error_status, resp_success_status
from Utils.jwt_auth import create_token
from Utils.auth import login_required
from exts import db


@user_app.route('/login/', methods=['GET', 'POST'])
def login():
    """
    用户登录
    :return:
    """
    if request.method == 'GET':
        return jsonify(resp_error_status(msg="拒绝GET请求"))
    else:
        username = request.form.get('username')
        password = request.form.get('password')
        if all([username, password]):
            user = User.query.filter(User.username == username, User.password == password).first()
            if user:
                # 生成一个token
                token = create_token(username=username)
                return jsonify(resp_success_status(msg="登录成功", username=username, password=password, token=token))
            else:
                return jsonify(resp_error_status(msg="用户名密码错误"))
        return jsonify(resp_error_status(msg="用户名密码漏填"))


@user_app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return jsonify(resp_error_status(msg="拒绝GET请求"))
    else:
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        email = request.form.get('email')

        if all([username, password1, password2]):
            if password1 != password2:
                return jsonify(resp_error_status(msg="两次密码不相等，请核对后再填写！"))

            user = User.query.filter(User.username == username).first()
            if user:
                return jsonify(resp_error_status(msg="该用户名已被注册，请更换用户名！"))
            else:
                # user = User(username=username, password=generate_password_hash(password1), email=email)
                user = User(username=username, password=password1, email=email)
                db.session.add(user)
                db.session.commit()
                # 生成一个token
                token = create_token(username=username)
                return jsonify(resp_success_status(msg="注册成功", token=token))

        else:
            return jsonify(resp_error_status(msg="信息漏填"))


@user_app.route('/login_views/', methods=['GET'])
@login_required
def login_views():
    """
    登录的用户来查看消息
    :return:
    """
    username = g.username
    print('username', username)
    return jsonify(resp_success_status(msg="success", data="登录的用户才能访问"))


@user_app.route('/views/', methods=['GET'])
def views():
    """
    不用登录的用户来查看消息
    :return:
    """
    return jsonify(resp_success_status(msg="success", data="不用登录的用户来查看消息"))
